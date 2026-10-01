The VCF was not compared directly in its 98.9-million-record form. It was first collapsed with Truvari, restricted to chr1–22+X, and then compared with the filtered Shapeit callset.

## Analysis lineage

```
1kGP...merged.norm.vcf.gz
  98,863,386 records
        │
        ├─ canonical chromosomes chr1–22 + chrX
        └─ Truvari collapse
           -r 500 -p 0.95 -P 0.95 -s 50 -S 100000
                │
                ▼
1kGP...truvari-collapsed.vcf.gz
  82,507,518 records
                │
                ├─ BEDTools coordinate comparison
                ├─ count/overlap figures
                ├─ BED-span length figures
                └─ attempted Truvari benchmark and signed-length analysis
```

Main derived VCFs:

- Input: 1kGP.no.missing.to.ref.len2.merged.norm.vcf.gz
- Retained after collapse: 1kGP.no.missing.to.ref.len2.truvari-collapsed.vcf.gz
- Collapsed-away calls: 1kGP.no.missing.to.ref.len2.truvari-collapsed-calls.vcf.gz
- Shapeit/Korbel comparison callset: shapeit5-phased-callset\_final-vcf.phased.len2.sorted.vcf.gz, containing 164,405 records.

The collapse concatenation script was:

- /home/dkhlebnikov/SV/1KG/concat\_after\_truvari\_korbel\_params.bash

Its successful log is:

- /home/dkhlebnikov/SV/1KG/concat\_truvari\_1kg.21808647.out

The exact per-chromosome collapse command is preserved in logs such as:

- truVarKorParams chr1 log (/home/dkhlebnikov/SV/1KG/truVarKorParams\_1kg.21312953\_1.err)

Caveat: /home/dkhlebnikov/SV/1KG/truvari\_perchr\_array\_korbel\_params.sh no longer contains the historical collapse code; it appears to have been overwritten with concatenation code.

## Main Shapeit comparison

The comparison script was:

- /home/dkhlebnikov/SV/1KG/compare\_fc3\_vs\_korbel.bash:18

Historical inputs are now commented out because the script was later modified for a `>=50 bp` analysis. The completed historical run used:

```
FC3:
  /home/dkhlebnikov/SV/1KG/prepare_fc1/
  1kGP.no.missing.to.ref.len2.truvari-collapsed.vcf.gz

Shapeit/Korbel:
  /home/dkhlebnikov/SV/1KG/prepare_fc1/
  shapeit5-phased-callset_final-vcf.phased.len2.sorted.vcf.gz
```

Each VCF was converted to BED using:

```
CHROM  POS0  END  generated_unique_ID  original_VCF_ID
```

Then `bedtools intersect` classified records using two criteria:

1. Any coordinate overlap of at least 1 bp.
2. Reciprocal coordinate overlap of at least 50% (`-f 0.50 -r`).

This was directional, not one-to-one matching. Therefore, the number of FC3 records overlapping Shapeit and the number of Shapeit records overlapping FC3 can differ.

Successful run log:

- /home/dkhlebnikov/SV/1KG/compare\_fc3\_vs\_korbel.21832176.out

Result directory:

- `/home/dkhlebnikov/SV/1KG/compare_fc3_vs_korbel`

Summary table:

- /home/dkhlebnikov/SV/1KG/compare\_fc3\_vs\_korbel/bedtools\_overlap\_summary.tsv

Results:

| Criterion | FC3 overlapping | Shapeit overlapping |
|---|---:|---:|
| Any ≥1-bp overlap | 2,786,195 / 82,507,518 = 3.3769% | 44,278 / 164,405 = 26.9323% |
| Reciprocal ≥50% | 11,050 / 82,507,518 = 0.0134% | 2,504 / 164,405 = 1.5231% |

## Plotting scripts and figures

### Count and overlap plots

Script:

- /home/dkhlebnikov/SV/1KG/plot\_fc3\_vs\_korbel\_bedtools.py

It reads `bedtools_overlap_summary.tsv` and produces:

- Total variant counts, using a log y-axis.
- Percent with/without any ≥1-bp overlap.
- Percent with/without reciprocal ≥50% overlap.
- A combined three-panel figure.

Preferred newer “clean” figures:

- Combined figure PNG (/home/dkhlebnikov/SV/1KG/compare\_fc3\_vs\_korbel/figures/fc3\_vs\_korbel\_bedtools\_combined\_clean.png)
- Total counts PNG (/home/dkhlebnikov/SV/1KG/compare\_fc3\_vs\_korbel/figures/01\_total\_variant\_counts\_clean.png)
- Any-overlap PNG (/home/dkhlebnikov/SV/1KG/compare\_fc3\_vs\_korbel/figures/02\_overlap\_1bp\_100pct\_clean.png)
- Reciprocal-overlap PNG (/home/dkhlebnikov/SV/1KG/compare\_fc3\_vs\_korbel/figures/03\_reciprocal\_overlap\_50pct\_100pct\_clean.png)

PDF and SVG versions are in:

- `/home/dkhlebnikov/SV/1KG/compare_fc3_vs_korbel/figures`

The earlier versions have the corresponding names without `_clean`; the original plotting job is recorded in:

- /home/dkhlebnikov/SV/1KG/plot\_fc3\_vs\_korbel.21832224.out

### Length-distribution plots

Script:

- /home/dkhlebnikov/SV/1KG/plot\_fc3\_vs\_korbel\_length\_bins.py

Figures:

- Total BED-length distribution (/home/dkhlebnikov/SV/1KG/compare\_fc3\_vs\_korbel/length\_analysis/01\_total\_length\_distribution.png)
- Total length-bin percentages (/home/dkhlebnikov/SV/1KG/compare\_fc3\_vs\_korbel/length\_analysis/02\_total\_length\_bins\_percent.png)
- Length bins by ≥1-bp overlap (/home/dkhlebnikov/SV/1KG/compare\_fc3\_vs\_korbel/length\_analysis/03\_overlap\_1bp\_length\_bins\_percent.png)
- Length bins by reciprocal ≥50% overlap (/home/dkhlebnikov/SV/1KG/compare\_fc3\_vs\_korbel/length\_analysis/04\_reciprocal\_50pct\_length\_bins\_percent.png)

Bins used:

```
[2,10), [10,50), [50,100), [100,500), [500,+inf)
```

Important caveat: these figures use BED interval length, `END - POS0`, not allele-length change `len(ALT)-len(REF)` or `SVLEN`. Insertions can therefore appear as one-base intervals. This explains why approximately 47% of both total BED files have interval length below 2 bp despite the original allele-length filter.

## Incomplete analyses

Two additional analyses were attempted but did not produce complete final results:

- Per-chromosome Truvari benchmark: /home/dkhlebnikov/SV/1KG/compare\_fc3\_vs\_korbel\_truvari\_array.bash
  - Complete for 17 of 23 chromosomes.
  - chr2, chr3, chr7, chr10, chr22, and chrX failed through memory limits or time limits.
  - No valid genome-wide aggregate figure was produced.
- Signed allele-length analysis: /home/dkhlebnikov/SV/1KG/analyze\_fc3\_vs\_korbel\_signed\_lengths.bash
  - Both attempts failed with AWK syntax errors.
  - The resulting TSV files are empty, so no signed-length figures exist.

Also, the current active settings in `compare_fc3_vs_korbel.bash` point to later `>=50 bp` BCF files, not the historical VCFs that generated the completed figures. Re-running it unchanged would not reproduce the results above.
```
  Worked for 4m 3s • 10:40
```
