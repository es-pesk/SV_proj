#!/usr/bin/env python3
import argparse
from bisect import bisect_left

import pysam
from tqdm import tqdm


def add_ref_overlap(cov: int, seg_start: int, seg_end: int, int_start: int, int_end: int) -> int:
    if seg_end > int_start and seg_start < int_end:
        cov += max(0, min(seg_end, int_end) - max(seg_start, int_start))
    return cov


def slice_ref_window_no_rc(
    read: pysam.AlignedSegment,
    ref_left: int,
    ref_right: int,
    AL: int,
    AR: int,
):
    """
    Возвращает (r0, r1, seq) для окна [ref_left, ref_right),
    если рид покрывает оба якоря.

    Разрешено:
      - insertion в якорях
      - deletion в якорях

    Не разрешено:
      - полное отсутствие фланка / неполное покрытие якоря
      - skipped region (N) как замена якорного покрытия
    """
    if read.is_unmapped:
        return (None, None, "")

    seq_read = read.query_sequence
    if not seq_read:
        return (None, None, "")

    if read.reference_start is None or read.reference_end is None:
        return (None, None, "")

    ref_pos = read.reference_start
    read_pos = 0

    left_cov = 0
    right_cov = 0

    left_int = (ref_left, min(ref_left + AL, ref_right))
    right_int = (max(ref_left, ref_right - AR), ref_right)

    parts = []

    for op, length in (read.cigartuples or []):
        # M, =, X
        if op in (0, 7, 8):
            rs_ref = ref_pos
            re_ref = ref_pos + length

            left_cov = add_ref_overlap(left_cov, rs_ref, re_ref, left_int[0], left_int[1])
            right_cov = add_ref_overlap(right_cov, rs_ref, re_ref, right_int[0], right_int[1])

            # Вклад в извлекаемую последовательность внутри окна
            if re_ref > ref_left and rs_ref < ref_right:
                left_cut = max(0, ref_left - rs_ref)
                right_cut = max(0, re_ref - ref_right)
                ql = read_pos + left_cut
                qr = (read_pos + length) - right_cut
                if ql < qr:
                    parts.append((ql, qr))

            ref_pos += length
            read_pos += length

        # I: вставка в риде, ref не двигается
        elif op == 1:
            # Если insertion якорная или внутри окна — не запрещаем
            # Если точка вставки лежит в окне, bases включаем в seq
            if ref_left <= ref_pos < ref_right:
                parts.append((read_pos, read_pos + length))
            read_pos += length

        # D: deletion по reference, read не двигается
        elif op == 2:
            rs_ref = ref_pos
            re_ref = ref_pos + length

            # ВАЖНО: deletion тоже засчитываем в покрытие якорей,
            # чтобы разрешить делеции в якорях
            left_cov = add_ref_overlap(left_cov, rs_ref, re_ref, left_int[0], left_int[1])
            right_cov = add_ref_overlap(right_cov, rs_ref, re_ref, right_int[0], right_int[1])

            ref_pos += length

        # N: skipped region, не считаем допустимым anchor coverage
        elif op == 3:
            ref_pos += length

        # S: soft clip
        elif op == 4:
            read_pos += length

        # H: hard clip
        elif op == 5:
            pass

        # P: padding
        elif op == 6:
            pass

        else:
            # На всякий случай игнорируем экзотические CIGAR op
            pass

    if not parts:
        return (None, None, "")

    # Якоря должны быть полностью покрыты по reference path.
    # Это разрешает D в якоре, но не разрешает полное отсутствие фланка.
    if left_cov < AL or right_cov < AR:
        return (None, None, "")

    # Склеиваем стыкующиеся куски
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
    ap.add_argument("--out-grp", required=True, help="output .grp")
    ap.add_argument("--flank", type=int, default=50, help="reference flank size")
    ap.add_argument(
        "--anchor",
        type=int,
        default=None,
        help="AL=AR anchor size; default = flank",
    )
    args = ap.parse_args()

    FLANK = int(args.flank)
    ANCH = int(args.anchor) if args.anchor is not None else FLANK

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
            core_end = int(e)

            if len(toks) == 7:
                var_id = f"{chrom}:{s}:{e}:{toks[6]}"
            else:
                var_id = f"{chrom}:{s}:{e}"

            gt = toks[4] if len(toks) > 4 else "./."

            win_left = max(0, core_start - FLANK)
            win_right = core_end + FLANK

            idx = len(intervals_all)
            intervals_all.append(
                {
                    "chrom": chrom,
                    "core_start": core_start,
                    "core_end": core_end,
                    "var_id": var_id,
                    "gt": gt,
                    "win_left": win_left,
                    "win_right": win_right,
                    "rows": [],
                }
            )
            chrom_to_indices.setdefault(chrom, []).append(idx)

    bam = pysam.AlignmentFile(args.bam, "rb")

    for chrom, idx_list in chrom_to_indices.items():
        idx_list_sorted = sorted(idx_list, key=lambda i: intervals_all[i]["win_left"])
        win_lefts = [intervals_all[i]["win_left"] for i in idx_list_sorted]

        min_win_left = min(intervals_all[i]["win_left"] for i in idx_list)
        max_win_right = max(intervals_all[i]["win_right"] for i in idx_list)

        for read in tqdm(
            bam.fetch(chrom, min_win_left, max_win_right),
            desc=f"{chrom}: reading BAM",
        ):
            if (
                read.is_unmapped
                or read.is_secondary
                or read.is_supplementary
                or read.mapping_quality < 1
            ):
                continue

            if read.reference_start is None or read.reference_end is None:
                continue

            rs = read.reference_start
            re = read.reference_end

            pos = bisect_left(win_lefts, rs)

            for k in range(pos, len(idx_list_sorted)):
                iv_idx = idx_list_sorted[k]
                iv = intervals_all[iv_idx]
                wl = iv["win_left"]
                wr = iv["win_right"]

                if wl > re:
                    break

                # Окно должно быть покрыто ридом по координатам
                if rs > wl or re < wr:
                    continue

                _, _, seq = slice_ref_window_no_rc(
                    read,
                    ref_left=wl,
                    ref_right=wr,
                    AL=ANCH,
                    AR=ANCH,
                )
                if not seq:
                    continue

                strand = "+"
                row = f"{iv['var_id']}${iv['gt']}${read.query_name} {strand}{seq}"
                iv["rows"].append(row)

    skipped_log = args.bed + "_skipped_grp.log"
    with open(skipped_log, "w") as log_f, open(args.out_grp, "w") as out:
        for iv in intervals_all:
            rows = iv["rows"]
            if not rows:
                log_f.write(
                    f"{iv['chrom']}\t{iv['core_start']}\t{iv['core_end']}\t{iv['var_id']}\t{iv['gt']}\n"
                )
                continue

            chrom = iv["chrom"]
            win_left = iv["win_left"]
            win_right = iv["win_right"]

            print(f"> {chrom} {win_left} {win_right}", file=out)
            out.write("\n".join(rows) + "\n")
            print("//", file=out)

    bam.close()
    print(f"Output: {args.out_grp}")


if __name__ == "__main__":
    main()
