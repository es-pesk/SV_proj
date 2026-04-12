#!/usr/bin/env python3

import argparse
from pathlib import Path
import pandas as pd
import numpy as np


def evnt_to_bed(evnt_path: Path, out_bed: Path) -> None:
    input_file = str(evnt_path)
    base = input_file.rsplit(".evnt", 1)[0]

    df = pd.read_csv(input_file, sep="\t")

    df = df[~df["Type"].isin(["no_event", "Error*"])].copy()
    df.to_csv(f"{base}_filt.evnt", sep="\t", index=False)

    for col in ["pos", "to", "LDel", "LIns"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(np.int64)

    df["start"] = (df["pos"] - 1).clip(lower=0)

    is_insertion = df["Type"].eq("insertion")

    df["end"] = np.where(
        is_insertion,
        df["pos"],
        np.maximum(df["to"], df["start"] + np.maximum(df["LDel"], 1))
    )

    bed_true = df[["Chr", "start", "end"]]
    bed_true.to_csv(out_bed, sep="\t", header=False, index=False)

    print(f"Written: {out_bed}")
    print(f"Written: {base}_filt.evnt")


def main():
    ap = argparse.ArgumentParser(description="Create BED from GeneVar .evnt")
    ap.add_argument("--evnt", required=True, type=Path, help="Input .evnt")
    ap.add_argument("--out-bed", required=True, type=Path, help="Output .bed")
    args = ap.parse_args()

    evnt_to_bed(args.evnt, args.out_bed)


if __name__ == "__main__":
    main()
