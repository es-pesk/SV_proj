import argparse
import pysam
from tqdm import tqdm
from bisect import bisect_left


def slice_ref_window_no_rc(read: pysam.AlignedSegment,
                           ref_left: int, ref_right: int,
                           AL: int, AR: int, 
                           allow_indel_size: int=3, allow_indel_count: int = 1):
    if read.is_unmapped:
        print('Unmapped')
        return (None, None, "")
    seq_read = read.query_sequence
    if not seq_read:
        print('not_seq')
        return (None, None, "")

    ref_pos = read.reference_start
    read_pos = 0

    left_cov = 0
    right_cov = 0
    left_int = (ref_left, min(ref_left + AL, ref_right))
    right_int = (max(ref_left, ref_right - AR), ref_right)

    parts = []
    # считаем колво инделей в якорях если они разрешены
    indel_cnt_left = 0
    indel_cnt_right = 0

    for op, length in (read.cigartuples or []):
        if op in (0, 7, 8):  # M, =, X
            rs_ref = ref_pos
            re_ref = ref_pos + length

            # вклад в якоря
            a, b = left_int
            if re_ref > a and rs_ref < b:
                left_cov += max(0, min(re_ref, b) - max(rs_ref, a))
            a, b = right_int
            if re_ref > a and rs_ref < b:
                right_cov += max(0, min(re_ref, b) - max(rs_ref, a))

            # пересечение с окном
            a, b = ref_left, ref_right
            if re_ref > a and rs_ref < b:
                left_cut = max(0, a - rs_ref)
                right_cut = max(0, re_ref - b)
                ql = read_pos + left_cut
                qr = (read_pos + length) - right_cut
                if ql < qr:
                    parts.append((ql, qr))
                else:
                    print('not overlapping window')

            ref_pos += length
            read_pos += length
        

        
        elif op == 1:  # I
            
            # если вставка попадает в якоря — выкидываем рид
            if (left_int[0] <= ref_pos < left_int[1]) or (right_int[0] <= ref_pos < right_int[1]):
                    if length > allow_indel_size: #если  allow_indel_size = 0 это условие в любос лсучае выполняется
                        print('indel in anchor')
                        return (None, None, "")
                    if left_int[0] <= ref_pos < left_int[1]:
                        indel_cnt_left +=1
                        if length or indel_cnt_left > allow_indel_count:
                            print('over left allow_indel_count')
                            return (None, None, "")
                    if right_int[0] <= ref_pos < right_int[1]:
                        indel_cnt_right +=1
                        if length or indel_cnt_right > allow_indel_count:
                            print('over right allow_indel_count')
                            return (None, None, "")            
            if ref_left <= ref_pos < ref_right:
                parts.append((read_pos, read_pos + length))
            read_pos += length

        elif op in (2, 3):  # D, N
            rs_ref = ref_pos
            re_ref = ref_pos + length
            # пересечение с левым якорем?
            if re_ref > left_int[0] and rs_ref < left_int[1]:
                if length > allow_indel_size:
                    print('over right allow_indel_size 2')
                    return (None, None, "")
                indel_cnt_left += 1
                if indel_cnt_left > allow_indel_count:
                    print('over left allow_indel_count 2')
                    return(None, None, "")
            # пересечение с правым якорем?
            if re_ref > right_int[0] and rs_ref < right_int[1]:
                if length > allow_indel_size:
                   print('over right allow_indel_size 2')
                   return (None, None, "")
                indel_cnt_right += 1
                if indel_cnt_right > allow_indel_count:
                    print('over right allow_indel_count 2')
                    return(None, None, "")
            ref_pos += length

        elif op == 4: # S
            read_pos += length
        elif op == 5: # H
            print('op 5')
            pass

    if not parts:
        print('not parts')
        return (None, None, "")

    if (left_cov < AL) or (right_cov < AR):
        print('(left_cov < AL) or (right_cov < AR)')
        return (None, None, "")

    # слить стыкующиеся куски
    merged = []
    a, b = parts[0]
    for x, y in parts[1:]:
        if x == b:
            b = y
        else:
            merged.append((a, b))
            a, b = x, y
    merged.append((a, b))

    r0 = merged[0][0]
    r1 = merged[-1][1]
    seq = "".join(seq_read[x:y] for x, y in merged)
    return (r0, r1, seq)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bam", required=True, help="BAM sorted + .bai")
    ap.add_argument("--bed", required=True, help="BED: chr start end [gt and etc]")
    ap.add_argument("--out-grp", required=True, help="output - .grp")
    ap.add_argument("--flank", type=int, default=50, help="ref flank size)")
    ap.add_argument("--anchor", type=int, default=None, help="AL=AR, anchor (aligned to ref area without indels, mismatches acseptable) def = flank")

    ap.add_argument("--allow_indel_size", type=int, default=0, help="Max-size of allowed indels in anchors, def = 0 или 3 я подумаю")
    ap.add_argument("--allow_indel_count", type=int, default=0, help="Max count of allowed indels in each anchor, def = 1")    
    
    args = ap.parse_args()

    FLANK = int(args.flank)
    ANCH = int(args.anchor) if args.anchor is not None else FLANK

    # 1.Читаем весь BED и готовим интервалы 
    # intervals_all -  список в порядке строк BED
    # каждый элемент списка -  dict с полями и списком rows для результата
    intervals_all = []
    chrom_to_indices = {}

    with open(args.bed) as bed_f:
        for line in bed_f:
            if not line.strip() or line.startswith("#"):
                continue
            toks = line.split()
            if len(toks) < 3:
                continue

            chrom, s, e = toks[:3]
            core_start = int(s)
            core_end   = int(e)
            if len(toks) == 7 :
                var_id = f"{chrom}:{s}:{e}:{toks[6]}"
            else:
                var_id = f"{chrom}:{s}:{e}"
            if len(toks) > 4:
                gt = toks[4]
            else:
                gt = "./."

            win_left  = max(0, core_start - FLANK)
            win_right = core_end + FLANK

            idx = len(intervals_all)
            intervals_all.append({
                "chrom": chrom,
                "core_start": core_start,
                "core_end": core_end,
                "var_id": var_id,
                "gt": gt,
                "win_left": win_left,
                "win_right": win_right,
                "rows": []  # сюда будем складывать строки про риды
            })
            chrom_to_indices.setdefault(chrom, []).append(idx)

    bam = pysam.AlignmentFile(args.bam, "rb")

    # 2.Обрабатываем по хромосомам, один fetch на хромосому 
    for chrom, idx_list in chrom_to_indices.items():
        # индексы интервалов этой хромосомы
        # сортируем по win_left
        idx_list_sorted = sorted(idx_list, key=lambda i: intervals_all[i]["win_left"])
        win_lefts = [intervals_all[i]["win_left"] for i in idx_list_sorted]

        min_win_left  = min(intervals_all[i]["win_left"]  for i in idx_list)
        max_win_right = max(intervals_all[i]["win_right"] for i in idx_list)

        # один fetch на хромосому (точнее, на диапазон всех окон)
        for read in tqdm(
            bam.fetch(chrom, min_win_left, max_win_right),
            desc=f"{chrom}: reading BAM"
        ):
            if read.is_unmapped or read.is_secondary or read.is_supplementary or read.mapping_quality < 1:
                continue

            rs = read.reference_start
            re = read.reference_end

            # оставляем интервалы, окно которых полностью покрыто ридоа
            # в варианте без bisect  было rs <= win_left и re >= win_right, поэтому тут 
            # win_left >= rs, win_right <= re
            # поэтому берём только интервалы с win_left >= rs.
            pos = bisect_left(win_lefts, rs)

            # пробегаем интервалы, пока их win_left не вышел за пределы рида
            for k in range(pos, len(idx_list_sorted)): 
                iv_idx = idx_list_sorted[k]
                iv = intervals_all[iv_idx]
                wl = iv["win_left"]
                wr = iv["win_right"]

                if wl > re:
                    break


                # проверка покрытия окна:
                # без bisect было:
                # if read.reference_start > win_left or read.reference_end < win_right: continue
                if rs > wl or re < wr:
                    continue

                _, _, seq = slice_ref_window_no_rc(
                    read,
                    ref_left=wl,
                    ref_right=wr,
                    AL=ANCH,
                    AR=ANCH
                )
                if not seq:
                    continue

                strand = "+"
                row = f"{iv['var_id']}${iv['gt']}${read.query_name} {strand}{seq}"
                iv["rows"].append(row)

    # 3.Пишем результат в исходном порядке bed-а
    skipped_log = args.bed + "_skipped_grp.log"
    log_f = open(skipped_log, "w")
    with open(args.out_grp, "w") as out:
        for iv in intervals_all:
            rows = iv["rows"]
            if not rows:
                log_f.write(f"{iv['chrom']}\t{iv['core_start']}\t{iv['core_end']}\t{iv['var_id']}\t{iv['gt']}\n")
                continue

        #for iv in intervals_all:
        #    rows = iv["rows"]
        #    if not rows:
        #        continue
            chrom = iv["chrom"]
            win_left = iv["win_left"]
            win_right = iv["win_right"]

            print(f"> {chrom} {win_left} {win_right}", file=out)
            out.write("\n".join(rows) + "\n")
            print("//", file=out)

    print(f"Output: {args.out_grp}")


if __name__ == "__main__":
    main()
