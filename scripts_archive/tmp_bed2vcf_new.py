  GNU nano 2.3.1                                                                                                                                                                                                                                                                            File: tmp_bed2vcf_new.py

#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path


def to_int(value) -> int:
    try:
        if value is None or value == "":
            return 0
        return int(value)
    except (TypeError, ValueError):
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return 0


def to_float_str(value) -> str:
    try:
        if value is None or value == "":
            return "0"
        return str(float(value))
    except (TypeError, ValueError):
        return "0"


def to_str(value, default=".") -> str:
    if value is None:
        return default
    s = str(value).strip()
    return s if s else default


def load_ref_dict(ref_tsv_path: Path) -> dict:
    ref_dict = {}

    with open(ref_tsv_path, "r", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if len(row) < 4:
                continue

            chrom = row[0]
            start = row[1]
            end = row[2]
            ref_seq = row[3]

            key = f"{chrom}_{start}_{end}"
            ref_dict[key] = to_str(ref_seq, ".").upper()

    return ref_dict


def get_vcf(evnt_path: Path, ref_tsv_path: Path, out_vcf_tsv_path: Path) -> None:
    ref_dict = load_ref_dict(ref_tsv_path)

    with open(evnt_path, "r", newline="") as fin, open(out_vcf_tsv_path, "w", newline="") as fout:
        reader = csv.DictReader(fin, delimiter="\t")
        writer = csv.writer(fout, delimiter="\t", lineterminator="\n")

        if reader.fieldnames is None:
            raise ValueError("Input .evnt file has no header")

        required_fields = {"Chr", "pos", "to", "LIns", "LDel", "Type", "Reads", "Cover", "id%", "InsSeq"}
        missing = required_fields - set(reader.fieldnames)
        if missing:
            raise ValueError(f"Missing required columns in .evnt: {', '.join(sorted(missing))}")

        for row in reader:
            chrom = to_str(row.get("Chr"), ".")
            pos = to_int(row.get("pos"))
            end_coord = to_int(row.get("to"))
            lins = to_int(row.get("LIns"))
            ldel = to_int(row.get("LDel"))
            event_type = to_str(row.get("Type"), ".").upper()

            ref_key = f"{chrom}_{pos}_{end_coord}"
            ref_seq = ref_dict.get(ref_key)
            if ref_seq is None:
                continue

            ins_seq = to_str(row.get("InsSeq"), ".").upper()

            vcf_format_gt = "./."
            vcf_pos = pos + 1
            vcf_end = end_coord
            vcf_qual = "."
            vcf_filter = "PASS"
            vcf_info_svlen = lins - ldel
            vcf_info_svtype = event_type

            vcf_info_ad = to_int(row.get("Cover"))
            vcf_format_dp = to_int(row.get("Reads"))

            vcf_info_flanks_id_prcnt = to_float_str(row.get("id%"))

            vcf_id = f"{chrom}_{vcf_pos}_{end_coord}_{vcf_info_svtype}_"

            writer.writerow([
                chrom,                      # 0
                vcf_pos,                    # 1
                vcf_id,                     # 2
                ref_seq,                    # 3
                ins_seq,                    # 4
                vcf_qual,                   # 5
                vcf_filter,                 # 6
                vcf_end,                    # 7
                vcf_info_svlen,             # 8
                vcf_info_svtype,            # 9
                vcf_info_ad,                # 10
                vcf_info_flanks_id_prcnt,   # 11
                vcf_format_gt,              # 12
                vcf_format_dp,              # 13
            ])


def main():
    ap = argparse.ArgumentParser(
        description="Create VCF-like TSV from GeneVar evnt + reference TSV"
    )
    ap.add_argument("--evnt", required=True, type=Path, help="Input .evnt")
    ap.add_argument("--ref-tsv", required=True, type=Path, help="bedtools getfasta output TSV")
    ap.add_argument("--out-tsv", required=True, type=Path, help="Output *_as_vcf.tsv")
    args = ap.parse_args()

    get_vcf(
        evnt_path=args.evnt,
        ref_tsv_path=args.ref_tsv,
        out_vcf_tsv_path=args.out_tsv,
    )


if __name__ == "__main__":
    main()

