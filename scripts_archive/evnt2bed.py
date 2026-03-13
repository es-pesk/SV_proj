import pandas as pd
import sys

# usage:
# python events_to_bed.py input.tsv output.bed

input_file = sys.argv[1]
output_file = sys.argv[2]

df = pd.read_csv(input_file, sep="\t", dtype=str)

for col in ["pos", "Length", "LIns"]:
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

bed_df.to_csv(output_file, sep="\t", header=False, index=False)

print(f"Written: {output_file}")
