import pandas as pd
import sys

# usage:
# python events_to_bed.py input.tsv output.bed

input_file = sys.argv[1]
#output_file = sys.argv[2]
base = input_file.split('.')[0]

df = pd.read_csv(input_file, sep="\t", dtype=str)
df = df[~df["Type"].isin(["no_event", "Error"])].copy()]
df.to_csv(f'{input_file}_filt.evnt')

for col in ["pos", "to", "LDel", "LIns"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

def convert_row(row):
    chrom = row["Chr"]
    pos = row["pos"]
    event_type = row["Type"]
    ref_len = row["Length"] # length of event in ref
    ins_len = row["LIns"] # length of insertion
    ins_seq = row["InsSeq"] if pd.notna(row["InsSeq"]) else "."

    # BED: 0-based start, end-exclusive
    if event_type == "insertion":
        # insertion ets needs 1bp anchor
        start = max(pos - 1, 0)
        end = pos
    else:
        # others
        start = max(pos - 1, 0)
        end = start + max(ref_len, 1)

    return pd.Series({
        "chr": chrom,
        "start": start,
        "end": end,
        "type": event_type,
        "reflen": ref_len,
        "lins": ins_len,
        "insseq": ins_seq
    })

bed_df = df.apply(convert_row, axis=1)

bed_df.to_csv(f'{base}.bed', sep="\t", header=False, index=False)

print(f"Written: {output_file}")

def main():
    ap = argparse.ArgumentParser(description="Create bed from  GeneVar evnt + bedtool")
    ap.add_argument("--evnt", required=True, type=Path, help="Input .evnt")
    ap.add_argument("--out-bed", required=True, type=Path, help="Out .bed")
    #ap.add_argument("--ref-tsv", required=True, type=Path, help="bedtools getfasta output TS>
    #ap.add_argument("--out-evnt", required=True, type=Path, help="Output *_with_ref.evnt")
    #ap.add_argument("--out-", required=True, type=Path, help="Output *_as_vcf.tsv")
    args = ap.parse_args()

    evnt_to_bed(args.evnt, args.out-bed)
if __name__ == "__main__":
    main()
