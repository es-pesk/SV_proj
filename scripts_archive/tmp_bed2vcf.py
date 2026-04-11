#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd


#def parse_gt(x) -> str:
#    if pd.isna(x):
#        return "."
#    s = str(x).strip()
#    if s in ("[]", ""):
#        return "."
#    if s.startswith("[") and s.endswith("]"):
#        s = s[1:-1]
#    first = s.split(",")[0]
#    parts = first.split("$")
#    return parts[1] if len(parts) >= 2 else "."


def get_vcf(evnt_path: Path,
            ref_tsv_path: Path,
            out_evnt_path: Path,
            out_vcf_tsv_path: Path) -> None:

    evnt = pd.read_csv(evnt_path, sep="\t")
    # mb replace RefSeq with DelSeq - compare what is better
    #ref = pd.read_csv(ref_tsv_path, sep="\t", names=["chr", "start", "end", "Ref_Seq"])
    #ref["new_id"] = ref.apply(lambda x: f"{x['chr']}_{x['start']}_{x['end']}", axis=1)

    #evnt["new_id"] = evnt.apply(
    #    lambda x: f"{x['Chr']}_{x['pos']}_{x['to']}", axis=1)

    #evnt = pd.merge(evnt, ref[["new_id", "Ref_Seq"]], how="inner", on="new_id")

    evnt["VCF_FORMAT_GT"] = './.' #evnt["Reads"].apply(parse_gt)
    evnt["VCF_POS"] = evnt["pos"] + 1
    evnt["VCF_END"] = evnt["to"]
    evnt["VCF_QUAL"] = "."
    evnt["VCF_FILTER"] = "PASS"
    evnt["VCF_INFO_SVLEN"] = evnt["LIns"] - evnt["LDel"]
    evnt["VCF_INFO_SVTYPE"] = evnt["Type"].astype(str).str.upper()
    evnt["VCF_INFO_AD"] = evnt["Reads"]
    evnt["VCF_FORMAT_DP"] = evnt["Cover"]
    evnt["VCF_INFO_FLANKS_ID_PRCNT"] = evnt["id%"]

    evnt["VCF_ID"] = (evnt["Chr"].astype(str) + "_" +
        evnt["VCF_POS"].astype(str) + "_" +
        evnt["to"].astype(str) + "_" +
        evnt["VCF_INFO_SVTYPE"] + "_")

    vcf_like = evnt[["Chr", "VCF_POS", "VCF_ID", "DelSeq", "InsSeq",
        "VCF_QUAL", "VCF_FILTER", "VCF_END", "VCF_INFO_SVLEN",
        "VCF_INFO_SVTYPE","VCF_INFO_AD", "VCF_INFO_FLANKS_ID_PRCNT" ,
        "VCF_FORMAT_GT",  "VCF_FORMAT_DP" ]].copy()
    vcf_like.to_csv(out_vcf_tsv_path, sep="\t", index=False, header=False)


def main():
    ap = argparse.ArgumentParser(description="Create VCF-like TSV from GeneVar evnt + bedtools ref.")
    ap.add_argument("--evnt", required=True, type=Path, help="Input .evnt")
    ap.add_argument("--ref-tsv", required=True, type=Path, help="bedtools getfasta output TSV")
    ap.add_argument("--out-evnt", required=True, type=Path, help="Output *_with_ref.evnt")
    ap.add_argument("--out-tsv", required=True, type=Path, help="Output *_as_vcf.tsv")
    args = ap.parse_args()

    get_vcf(evnt_path=args.evnt,
        ref_tsv_path=args.ref_tsv,
        out_evnt_path=args.out_evnt,
        out_vcf_tsv_path=args.out_tsv,)

if __name__ == "__main__":
    main()

