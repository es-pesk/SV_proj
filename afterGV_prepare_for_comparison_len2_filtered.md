# Provenance report: `1kGP.no.missing.to.ref.len2.merged.norm.fixed_header.noY.sorted.vcf.gz`

Report reconstructed on 2026-10-01 from VCF header provenance, surviving scripts and files, file timestamps, Slurm logs, and `sacct`. Paths are absolute unless a basename is explicitly shown.

## Result

- VCF: `/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.len2.merged.norm.fixed_header.noY.sorted.vcf.gz`
- Tabix index: `/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.len2.merged.norm.fixed_header.noY.sorted.vcf.gz.tbi`
- VCF size and mtime: 8,501,577,396 bytes; 2026-08-16 15:44:24 PDT
- Index size and mtime: 2,656,373 bytes; 2026-08-16 16:10:02 PDT
- Samples: 967
- Records: 90,075,086
- Records by data contig: chr1-chr22 and chrX only. There are no chrY, mitochondrial, alt, random, or unplaced records.
- The header still declares all 195 reference contigs. The `bcftools view -r` operation restricted records but did not prune unused `##contig` declarations.

## Reconstructed workflow

### 0. Upstream sample callsets were normalized and merged

The retained VCF header says that individual GeneVar callsets were normalized against GRCh38 with commands of the form:

```bash
bcftools norm -c s -d exact \
  -f /home/agimelbrant/projects/PrCa/IRX4like/1KG_ONT/1KG_ONT_VIENNA_hg38.fa \
  -Oz \
  /net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/<SAMPLE>/<SAMPLE>.vcf.gz
```

Some per-sample VCFs were themselves concatenations of split chunks. The header retains the concrete HG02013 example, with eight inputs:

`/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02013/split/chunk_{1..8}/HG02013_chunk{1..8}.vcf.gz`

The 967 normalized sample VCFs were merged with `bcftools merge --threads 8 -Oz`. The complete concrete list is embedded in the `##bcftools_mergeCommand` line of the final VCF header. Its path set is:

`/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/<SAMPLE>/<SAMPLE>_norm.vcf.gz`

Merged output:

`/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/1kGP.no.missing.to.ref.vcf.gz`

The header dates this merge to 2026-06-07. This source currently exists and is 6,238,159,545 bytes.

### 1. Split multiallelic records and left-align alleles

Proven command from the VCF header, run 2026-08-04 10:36:

```bash
bcftools norm -m -both \
  -f /home/agimelbrant/projects/PrCa/IRX4like/1KG_ONT/1KG_ONT_VIENNA_hg38.fa \
  --threads 16 -Oz \
  -o /home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.01.split.leftaligned.tmp.vcf.gz \
  /net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/1kGP.no.missing.to.ref.vcf.gz
```

The script then renamed the temporary file to:

`/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.01.split.leftaligned.vcf.gz`

The log reports 73,602,010 input lines, 9,570,213 split lines, and 16,407,898 realignments.

### 2. Keep variants whose REF/ALT length difference is at least 2 bp

Proven command from the header, run 2026-08-04 12:48:

```bash
bcftools view -i 'abs(strlen(REF)-strlen(ALT))>=2' \
  --threads 16 -Oz \
  -o /home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.02.len2.tmp.vcf.gz \
  /home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.01.split.leftaligned.vcf.gz
```

The script then renamed the temporary file to:

`/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.02.len2.vcf.gz`

This removed SNPs and 1-bp indels. The next stage's log reports 99,058,559 records entering exact deduplication.

### 3. Remove exact duplicate records, sort, and index

Proven deduplication command from the header, run 2026-08-04 14:14:

```bash
bcftools norm -d exact --threads 16 -Oz \
  -o /home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.03.len2.deduplicated.tmp.vcf.gz \
  /home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.02.len2.vcf.gz
```

The script renamed that to:

`/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.03.len2.deduplicated.vcf.gz`

It then ran `bcftools sort -m 8G`, using temporary files below:

`/home/dkhlebnikov/SV/1KG/prepare_fc1/bcftools-sort-20935218/sort.XXXXXX*`

The sorted temporary output and index were:

- `/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.len2.merged.norm.tmp.vcf.gz`
- `/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.len2.merged.norm.tmp.vcf.gz.tbi`

They were renamed to the surviving pre-collapse files:

- `/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.len2.merged.norm.vcf.gz`
- `/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.len2.merged.norm.vcf.gz.tbi`

This VCF contains 98,863,386 records, so exact deduplication removed 195,173 records. Slurm job 20935218 completed these preparation stages and then exited 127 because `truvari` was not on `PATH`; that later failure does not invalidate the already-created pre-collapse VCF and index. The three numbered intermediates and the sort directory were intentionally removed and are no longer present.

### 4. Repair contig header lines

The header was replaced using the FASTA index:

```bash
bcftools reheader \
  -f /home/agimelbrant/projects/PrCa/IRX4like/1KG_ONT/1KG_ONT_VIENNA_hg38.fa.fai \
  -o /home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.len2.merged.norm.fixed_header.vcf.gz \
  /home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.len2.merged.norm.vcf.gz
```

This retained 195 contig declarations and added their `length=` values. It did not alter the record count (98,863,386).

Slurm job 21127420 wrote the repaired VCF and then failed on the malformed final line of the script (`"${FIXED"`). Slurm job 21127471 subsequently created the surviving index with:

```bash
tabix -f -p vcf /home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.len2.merged.norm.fixed_header.vcf.gz
```

Outputs:

- `/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.len2.merged.norm.fixed_header.vcf.gz`
- `/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.len2.merged.norm.fixed_header.vcf.gz.tbi`

### 5. Retain canonical autosomes plus chrX; remove chrY and all other contigs

Proven command from the header, started by Slurm job 21304709 on 2026-08-16 10:43:

```bash
bcftools view \
  -r chr1,chr2,chr3,chr4,chr5,chr6,chr7,chr8,chr9,chr10,chr11,chr12,chr13,chr14,chr15,chr16,chr17,chr18,chr19,chr20,chr21,chr22,chrX \
  --threads 6 -Oz \
  -o /home/dkhlebnikov/SV/1KG/1kGP.no.missing.to.ref.len2.merged.norm.fixed_header.noY.vcf.gz \
  /home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.len2.merged.norm.fixed_header.vcf.gz
```

Surviving output:

`/home/dkhlebnikov/SV/1KG/1kGP.no.missing.to.ref.len2.merged.norm.fixed_header.noY.vcf.gz`

The selection removed 8,788,300 records: 2,732,063 chrY records plus 6,056,237 records on mitochondrial/alt/random/unplaced contigs. It retained 90,075,086 records. Job 21304709 was later cancelled while attempting subsequent work, but the noY VCF had already completed at 12:09.

### 6. Sort, BGZF-compress, index, and relocate the result

Slurm job 21304842 ran the active portion of `filter_length_korbel.sh`:

```bash
bcftools sort --max-mem 48G -Oz \
  -o /home/dkhlebnikov/SV/1KG/1kGP.no.missing.to.ref.len2.merged.norm.fixed_header.noY.sorted.vcf.gz \
  /home/dkhlebnikov/SV/1KG/1kGP.no.missing.to.ref.len2.merged.norm.fixed_header.noY.vcf.gz

tabix -p vcf \
  /home/dkhlebnikov/SV/1KG/1kGP.no.missing.to.ref.len2.merged.norm.fixed_header.noY.sorted.vcf.gz
```

The sort log records temporary storage at:

`/tmp/slurm.21304842/bcftools.eOgf56`

The job ran 2026-08-16 12:56:01–16:10:02 and completed successfully. The VCF finished at 15:44:24 and the index at 16:10:02. The script's literal output paths in `/home/dkhlebnikov/SV/1KG` no longer exist. The VCF and index now have those same completion mtimes in `/home/dkhlebnikov/SV/1KG/prepare_fc1`, showing that they were moved after creation without changing their contents or mtimes. No surviving script or log records that relocation command, so the move is a high-confidence inference rather than a directly recorded command.

## Scripts and execution evidence

### Preparation

- Script: `/home/dkhlebnikov/SV/1KG/prepare_collapse_fc3.bash`
- Current-lineage stdout: `/home/dkhlebnikov/SV/1KG/prepare_collapse_1kg.20935218.out`
- Current-lineage stderr: `/home/dkhlebnikov/SV/1KG/prepare_collapse_1kg.20935218.err`
- Earlier equivalent attempt in the parent work directory: `/home/dkhlebnikov/SV/1KG/prepare_collapse_1kg.20928038.out`
- Earlier equivalent attempt stderr: `/home/dkhlebnikov/SV/1KG/prepare_collapse_1kg.20928038.err`

The current script was modified on 2026-08-14, after job 20935218 ran. It presently names an absent `1kGP.no.missing.to.ref.fixed.vcf.gz`; the final VCF header proves that the actual 2026-08-04 input was `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/1kGP.no.missing.to.ref.vcf.gz`.

### Header repair and indexing

- Reheader script: `/home/dkhlebnikov/SV/1KG/fix_fc3_header.sh`
- Reheader stdout: `/home/dkhlebnikov/SV/1KG/fix_header_fc3.21127420.out`
- Reheader stderr: `/home/dkhlebnikov/SV/1KG/fix_header_fc3..21127420.err`
- Index script: `/home/dkhlebnikov/SV/1KG/prepare_fc1/index_fixed.bash`
- Index stdout: `/home/dkhlebnikov/SV/1KG/prepare_fc1/tabix_fixed.21127471.out`
- Index stderr: `/home/dkhlebnikov/SV/1KG/prepare_fc1/tabix_fixed.21127471.err`

### Canonical-contig filtering and final sort

- Script: `/home/dkhlebnikov/SV/1KG/filter_length_korbel.sh`
- Failed preliminary logs: `/home/dkhlebnikov/SV/1KG/filter_korbel.21304113.out`, `/home/dkhlebnikov/SV/1KG/filter_korbel.21304113.err`, `/home/dkhlebnikov/SV/1KG/filter_korbel.21304114.out`, `/home/dkhlebnikov/SV/1KG/filter_korbel.21304114.err`
- Filtering job logs: `/home/dkhlebnikov/SV/1KG/filter_korbel.21304709.out`, `/home/dkhlebnikov/SV/1KG/filter_korbel.21304709.err`
- Successful final-sort logs: `/home/dkhlebnikov/SV/1KG/filter_korbel.21304842.out`, `/home/dkhlebnikov/SV/1KG/filter_korbel.21304842.err`

## Reference and tool paths

- GRCh38 FASTA: `/home/agimelbrant/projects/PrCa/IRX4like/1KG_ONT/1KG_ONT_VIENNA_hg38.fa`
- FASTA index used by `bcftools reheader`: `/home/agimelbrant/projects/PrCa/IRX4like/1KG_ONT/1KG_ONT_VIENNA_hg38.fa.fai`
- Currently resolved `bcftools`: `/home/dkhlebnikov/tools/bin/bcftools`
- Currently resolved `tabix`: `/home/dkhlebnikov/tools/bin/tabix`
- Currently resolved `bgzip`: `/home/dkhlebnikov/tools/bin/bgzip`

The VCF header identifies bcftools 1.20/htslib 1.20 for the merge and August preparation steps. An older per-sample normalization header line identifies bcftools 1.13/htslib 1.13. The absolute executable paths used at runtime were not captured, so the three tool paths above describe the current environment, not necessarily the historical executables.

## Complete path inventory by role

The operationally related paths are all listed above. For completeness, the large upstream sample collections are represented without omission by these parameterized path sets:

- Raw per-sample input: `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/<SAMPLE>/<SAMPLE>.vcf.gz`
- Normalized per-sample input to merge: `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/<SAMPLE>/<SAMPLE>_norm.vcf.gz`
- Optional per-sample chunks: `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/<SAMPLE>/split/chunk_<N>/<SAMPLE>_chunk<N>.vcf.gz`

The exact 967 sample names and all 986 concrete absolute path tokens retained from upstream commands can be recovered losslessly from the target itself with:

```bash
bcftools view --no-version -h \
  /home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.len2.merged.norm.fixed_header.noY.sorted.vcf.gz \
| grep '^##bcftools_.*Command=' \
| grep -oE '/[A-Za-z0-9_.+/-]+' \
| sort -u
```

This header is the authoritative exhaustive list for upstream sample paths; duplicating its 967-entry merge argument in prose would make the report harder to audit.

## Exhaustive paths embedded in VCF provenance

The following 986 unique absolute paths are copied from the retained `##bcftools_*Command` header records. This expands the parameterized upstream sets above and includes every per-sample merge input recorded by the VCF.

- `/home/agimelbrant/projects/PrCa/IRX4like/1KG_ONT/1KG_ONT_VIENNA_hg38.fa`
- `/home/dkhlebnikov/SV/1KG/1kGP.no.missing.to.ref.len2.merged.norm.fixed_header.noY.vcf.gz`
- `/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.01.split.leftaligned.tmp.vcf.gz`
- `/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.01.split.leftaligned.vcf.gz`
- `/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.02.len2.tmp.vcf.gz`
- `/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.02.len2.vcf.gz`
- `/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.03.len2.deduplicated.tmp.vcf.gz`
- `/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.len2.merged.norm.fixed_header.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/1kGP.no.missing.to.ref.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00096/HG00096.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00096/HG00096_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00099/HG00099_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00100/HG00100_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00101/HG00101_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00103/HG00103_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00106/HG00106_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00107/HG00107_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00111/HG00111_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00114/HG00114_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00117/HG00117_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00120/HG00120_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00123/HG00123_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00125/HG00125_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00128/HG00128_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00129/HG00129_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00130/HG00130_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00131/HG00131_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00133/HG00133_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00137/HG00137_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00139/HG00139_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00141/HG00141_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00146/HG00146_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00148/HG00148_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00149/HG00149_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00157/HG00157_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00158/HG00158_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00159/HG00159_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00171/HG00171_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00173/HG00173_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00188/HG00188_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00190/HG00190_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00235/HG00235_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00242/HG00242_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00243/HG00243_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00252/HG00252_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00254/HG00254_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00255/HG00255_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00258/HG00258_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00261/HG00261_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00268/HG00268_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00269/HG00269_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00271/HG00271_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00273/HG00273_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00274/HG00274_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00278/HG00278_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00282/HG00282_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00284/HG00284_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00311/HG00311_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00313/HG00313_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00315/HG00315_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00321/HG00321_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00323/HG00323_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00324/HG00324_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00325/HG00325_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00334/HG00334_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00335/HG00335_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00336/HG00336_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00338/HG00338_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00342/HG00342_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00346/HG00346_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00349/HG00349_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00357/HG00357_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00360/HG00360_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00361/HG00361_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00365/HG00365_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00367/HG00367_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00368/HG00368_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00378/HG00378_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00381/HG00381_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00404/HG00404_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00407/HG00407_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00409/HG00409_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00418/HG00418_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00419/HG00419_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00420/HG00420_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00427/HG00427_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00436/HG00436_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00442/HG00442_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00443/HG00443_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00446/HG00446_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00449/HG00449_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00452/HG00452_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00464/HG00464_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00472/HG00472_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00475/HG00475_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00479/HG00479_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00513/HG00513_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00530/HG00530_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00537/HG00537_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00551/HG00551_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00565/HG00565_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00566/HG00566_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00583/HG00583_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00584/HG00584_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00589/HG00589_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00596/HG00596_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00607/HG00607_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00608/HG00608_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00610/HG00610_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00619/HG00619_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00622/HG00622_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00626/HG00626_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00632/HG00632_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00634/HG00634_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00637/HG00637_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00641/HG00641_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00650/HG00650_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00651/HG00651_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00657/HG00657_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00684/HG00684_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00692/HG00692_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00702/HG00702_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00717/HG00717_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00731/HG00731_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00736/HG00736_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00737/HG00737_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00739/HG00739_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00740/HG00740_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00759/HG00759_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00766/HG00766_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00844/HG00844_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00881/HG00881_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG00982/HG00982_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01028/HG01028_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01047/HG01047_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01048/HG01048_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01054/HG01054_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01055/HG01055_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01058/HG01058_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01060/HG01060_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01066/HG01066_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01072/HG01072_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01073/HG01073_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01085/HG01085_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01086/HG01086_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01089/HG01089_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01101/HG01101_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01102/HG01102_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01104/HG01104_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01107/HG01107_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01108/HG01108_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01119/HG01119_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01121/HG01121_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01124/HG01124_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01130/HG01130_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01131/HG01131_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01133/HG01133_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01134/HG01134_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01136/HG01136_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01137/HG01137_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01142/HG01142_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01148/HG01148_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01167/HG01167_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01168/HG01168_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01174/HG01174_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01187/HG01187_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01188/HG01188_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01197/HG01197_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01198/HG01198_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01241/HG01241_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01242/HG01242_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01256/HG01256_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01257/HG01257_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01258/HG01258_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01259/HG01259_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01269/HG01269_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01275/HG01275_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01278/HG01278_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01284/HG01284_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01286/HG01286_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01302/HG01302_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01308/HG01308_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01311/HG01311_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01341/HG01341_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01344/HG01344_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01345/HG01345_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01347/HG01347_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01348/HG01348_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01356/HG01356_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01362/HG01362_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01366/HG01366_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01375/HG01375_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01377/HG01377_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01384/HG01384_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01389/HG01389_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01390/HG01390_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01392/HG01392_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01396/HG01396_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01398/HG01398_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01412/HG01412_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01447/HG01447_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01455/HG01455_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01464/HG01464_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01465/HG01465_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01474/HG01474_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01479/HG01479_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01489/HG01489_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01492/HG01492_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01494/HG01494_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01500/HG01500_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01504/HG01504_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01506/HG01506_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01507/HG01507_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01509/HG01509_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01512/HG01512_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01513/HG01513_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01518/HG01518_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01519/HG01519_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01525/HG01525_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01527/HG01527_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01530/HG01530_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01550/HG01550_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01551/HG01551_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01566/HG01566_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01571/HG01571_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01572/HG01572_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01577/HG01577_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01578/HG01578_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01583/HG01583_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01586/HG01586_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01589/HG01589_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01595/HG01595_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01596/HG01596_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01597/HG01597_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01598/HG01598_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01600/HG01600_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01602/HG01602_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01605/HG01605_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01606/HG01606_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01608/HG01608_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01612/HG01612_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01617/HG01617_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01626/HG01626_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01630/HG01630_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01673/HG01673_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01676/HG01676_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01678/HG01678_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01680/HG01680_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01684/HG01684_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01694/HG01694_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01699/HG01699_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01700/HG01700_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01756/HG01756_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01765/HG01765_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01766/HG01766_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01773/HG01773_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01776/HG01776_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01779/HG01779_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01786/HG01786_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01789/HG01789_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01791/HG01791_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01794/HG01794_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01796/HG01796_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01798/HG01798_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01800/HG01800_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01805/HG01805_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01806/HG01806_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01807/HG01807_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01809/HG01809_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01813/HG01813_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01815/HG01815_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01817/HG01817_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01840/HG01840_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01846/HG01846_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01851/HG01851_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01853/HG01853_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01859/HG01859_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01863/HG01863_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01865/HG01865_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01866/HG01866_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01870/HG01870_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01871/HG01871_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01872/HG01872_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01873/HG01873_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01879/HG01879_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01880/HG01880_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01883/HG01883_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01890/HG01890_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01894/HG01894_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01896/HG01896_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01915/HG01915_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01917/HG01917_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01918/HG01918_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01923/HG01923_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01932/HG01932_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01933/HG01933_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01935/HG01935_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01939/HG01939_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01942/HG01942_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01945/HG01945_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01947/HG01947_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01948/HG01948_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01950/HG01950_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01951/HG01951_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01953/HG01953_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01961/HG01961_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01965/HG01965_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01967/HG01967_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01971/HG01971_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01977/HG01977_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01982/HG01982_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01983/HG01983_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01985/HG01985_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01988/HG01988_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01990/HG01990_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01991/HG01991_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01992/HG01992_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG01997/HG01997_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02003/HG02003_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02006/HG02006_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02009/HG02009_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02010/HG02010_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02012/HG02012_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02013/HG02013.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02013/HG02013_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02013/split/chunk_1/HG02013_chunk1.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02013/split/chunk_2/HG02013_chunk2.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02013/split/chunk_3/HG02013_chunk3.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02013/split/chunk_4/HG02013_chunk4.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02013/split/chunk_5/HG02013_chunk5.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02013/split/chunk_6/HG02013_chunk6.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02013/split/chunk_7/HG02013_chunk7.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02013/split/chunk_8/HG02013_chunk8.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02014/HG02014_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02016/HG02016_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02017/HG02017_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02020/HG02020_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02031/HG02031_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02053/HG02053_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02058/HG02058_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02060/HG02060_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02064/HG02064_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02067/HG02067_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02069/HG02069_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02072/HG02072_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02079/HG02079_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02081/HG02081_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02082/HG02082_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02087/HG02087_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02089/HG02089_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02095/HG02095_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02105/HG02105_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02107/HG02107_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02111/HG02111_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02116/HG02116_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02121/HG02121_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02128/HG02128_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02130/HG02130_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02133/HG02133_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02136/HG02136_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02137/HG02137_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02138/HG02138_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02139/HG02139_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02143/HG02143_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02144/HG02144_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02146/HG02146_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02152/HG02152_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02153/HG02153_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02154/HG02154_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02155/HG02155_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02156/HG02156_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02164/HG02164_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02165/HG02165_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02178/HG02178_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02180/HG02180_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02182/HG02182_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02184/HG02184_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02223/HG02223_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02224/HG02224_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02231/HG02231_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02238/HG02238_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02239/HG02239_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02250/HG02250_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02253/HG02253_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02265/HG02265_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02266/HG02266_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02271/HG02271_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02274/HG02274_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02275/HG02275_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02277/HG02277_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02283/HG02283_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02284/HG02284_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02285/HG02285_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02291/HG02291_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02292/HG02292_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02307/HG02307_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02308/HG02308_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02309/HG02309_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02314/HG02314_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02318/HG02318_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02325/HG02325_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02332/HG02332_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02337/HG02337_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02364/HG02364_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02367/HG02367_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02382/HG02382_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02384/HG02384_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02390/HG02390_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02402/HG02402_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02410/HG02410_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02420/HG02420_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02429/HG02429_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02442/HG02442_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02445/HG02445_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02455/HG02455_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02477/HG02477_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02485/HG02485_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02490/HG02490_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02493/HG02493_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02494/HG02494_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02496/HG02496_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02521/HG02521_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02522/HG02522_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02524/HG02524_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02545/HG02545_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02546/HG02546_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02554/HG02554_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02558/HG02558_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02561/HG02561_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02562/HG02562_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02568/HG02568_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02573/HG02573_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02577/HG02577_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02580/HG02580_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02582/HG02582_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02585/HG02585_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02588/HG02588_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02595/HG02595_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02597/HG02597_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02600/HG02600_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02604/HG02604_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02611/HG02611_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02634/HG02634_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02635/HG02635_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02643/HG02643_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02657/HG02657_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02661/HG02661_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02678/HG02678_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02679/HG02679_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02681/HG02681_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02684/HG02684_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02685/HG02685_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02687/HG02687_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02688/HG02688_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02690/HG02690_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02691/HG02691_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02697/HG02697_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02703/HG02703_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02715/HG02715_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02721/HG02721_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02724/HG02724_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02727/HG02727_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02728/HG02728_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02737/HG02737_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02768/HG02768_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02771/HG02771_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02789/HG02789_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02793/HG02793_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02805/HG02805_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02836/HG02836_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02895/HG02895_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02922/HG02922_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02938/HG02938_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02943/HG02943_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02944/HG02944_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02953/HG02953_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02970/HG02970_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02971/HG02971_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02976/HG02976_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02982/HG02982_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02983/HG02983_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03009/HG03009_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03015/HG03015_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03016/HG03016_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03019/HG03019_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03024/HG03024_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03028/HG03028_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03039/HG03039_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03048/HG03048_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03052/HG03052_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03057/HG03057_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03058/HG03058_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03060/HG03060_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03066/HG03066_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03073/HG03073_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03074/HG03074_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03077/HG03077_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03081/HG03081_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03085/HG03085_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03086/HG03086_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03091/HG03091_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03097/HG03097_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03100/HG03100_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03103/HG03103_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03105/HG03105_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03108/HG03108_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03109/HG03109_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03111/HG03111_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03112/HG03112_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03114/HG03114_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03115/HG03115_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03117/HG03117_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03124/HG03124_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03127/HG03127_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03130/HG03130_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03132/HG03132_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03133/HG03133_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03159/HG03159_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03163/HG03163_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03172/HG03172_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03189/HG03189_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03193/HG03193_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03198/HG03198_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03199/HG03199_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03212/HG03212_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03228/HG03228_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03238/HG03238_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03240/HG03240_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03241/HG03241_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03247/HG03247_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03258/HG03258_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03265/HG03265_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03300/HG03300_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03301/HG03301_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03303/HG03303_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03307/HG03307_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03311/HG03311_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03342/HG03342_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03372/HG03372_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03373/HG03373_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03388/HG03388_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03391/HG03391_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03394/HG03394_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03397/HG03397_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03410/HG03410_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03437/HG03437_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03439/HG03439_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03442/HG03442_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03449/HG03449_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03455/HG03455_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03457/HG03457_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03461/HG03461_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03470/HG03470_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03473/HG03473_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03476/HG03476_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03484/HG03484_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03485/HG03485_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03499/HG03499_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03511/HG03511_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03517/HG03517_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03518/HG03518_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03521/HG03521_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03539/HG03539_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03548/HG03548_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03577/HG03577_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03582/HG03582_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03593/HG03593_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03595/HG03595_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03598/HG03598_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03600/HG03600_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03604/HG03604_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03607/HG03607_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03633/HG03633_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03639/HG03639_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03640/HG03640_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03644/HG03644_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03645/HG03645_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03650/HG03650_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03672/HG03672_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03673/HG03673_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03681/HG03681_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03686/HG03686_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03687/HG03687_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03689/HG03689_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03690/HG03690_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03695/HG03695_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03697/HG03697_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03703/HG03703_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03705/HG03705_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03708/HG03708_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03709/HG03709_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03711/HG03711_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03714/HG03714_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03721/HG03721_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03722/HG03722_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03727/HG03727_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03729/HG03729_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03730/HG03730_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03740/HG03740_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03741/HG03741_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03742/HG03742_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03746/HG03746_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03753/HG03753_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03756/HG03756_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03760/HG03760_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03761/HG03761_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03780/HG03780_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03781/HG03781_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03784/HG03784_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03786/HG03786_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03792/HG03792_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03793/HG03793_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03794/HG03794_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03797/HG03797_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03800/HG03800_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03802/HG03802_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03803/HG03803_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03805/HG03805_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03809/HG03809_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03812/HG03812_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03816/HG03816_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03821/HG03821_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03824/HG03824_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03830/HG03830_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03836/HG03836_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03837/HG03837_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03838/HG03838_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03844/HG03844_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03848/HG03848_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03854/HG03854_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03856/HG03856_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03862/HG03862_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03863/HG03863_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03869/HG03869_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03870/HG03870_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03871/HG03871_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03872/HG03872_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03882/HG03882_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03886/HG03886_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03888/HG03888_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03890/HG03890_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03894/HG03894_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03895/HG03895_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03900/HG03900_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03904/HG03904_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03916/HG03916_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03925/HG03925_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03928/HG03928_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03929/HG03929_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03931/HG03931_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03940/HG03940_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03941/HG03941_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03947/HG03947_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03963/HG03963_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03965/HG03965_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03968/HG03968_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03973/HG03973_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03976/HG03976_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03977/HG03977_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03990/HG03990_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG03999/HG03999_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04006/HG04006_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04014/HG04014_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04015/HG04015_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04017/HG04017_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04018/HG04018_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04020/HG04020_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04022/HG04022_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04025/HG04025_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04039/HG04039_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04062/HG04062_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04070/HG04070_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04099/HG04099_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04118/HG04118_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04131/HG04131_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04132/HG04132_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04140/HG04140_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04146/HG04146_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04147/HG04147_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04149/HG04149_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04156/HG04156_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04177/HG04177_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04180/HG04180_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04183/HG04183_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04186/HG04186_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04191/HG04191_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04192/HG04192_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04194/HG04194_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04198/HG04198_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04200/HG04200_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04210/HG04210_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG04227/HG04227_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA06989/NA06989_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA07014/NA07014_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA07019/NA07019_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA07048/NA07048_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA07348/NA07348_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA10835/NA10835_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA10839/NA10839_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA10842/NA10842_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA10843/NA10843_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA10851/NA10851_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA10852/NA10852_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA10856/NA10856_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA10857/NA10857_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA10859/NA10859_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA10861/NA10861_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA12335/NA12335_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA12336/NA12336_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA12376/NA12376_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA12386/NA12386_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA12766/NA12766_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA12801/NA12801_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA12802/NA12802_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA12877/NA12877_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA12878/NA12878_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA12889/NA12889_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA12890/NA12890_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA12891/NA12891_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA12892/NA12892_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18498/NA18498_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18499/NA18499_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18502/NA18502_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18504/NA18504_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18510/NA18510_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18516/NA18516_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18520/NA18520_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18523/NA18523_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18525/NA18525_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18526/NA18526_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18528/NA18528_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18530/NA18530_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18532/NA18532_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18537/NA18537_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18538/NA18538_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18539/NA18539_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18544/NA18544_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18546/NA18546_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18552/NA18552_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18553/NA18553_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18555/NA18555_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18565/NA18565_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18566/NA18566_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18567/NA18567_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18570/NA18570_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18571/NA18571_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18577/NA18577_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18579/NA18579_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18591/NA18591_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18592/NA18592_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18595/NA18595_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18599/NA18599_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18603/NA18603_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18605/NA18605_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18612/NA18612_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18616/NA18616_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18621/NA18621_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18623/NA18623_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18625/NA18625_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18632/NA18632_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18637/NA18637_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18639/NA18639_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18642/NA18642_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18853/NA18853_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18859/NA18859_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18862/NA18862_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18867/NA18867_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18868/NA18868_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18873/NA18873_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18874/NA18874_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18912/NA18912_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18913/NA18913_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18940/NA18940_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18941/NA18941_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18942/NA18942_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18944/NA18944_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18946/NA18946_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18947/NA18947_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18953/NA18953_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18956/NA18956_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18960/NA18960_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18965/NA18965_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18966/NA18966_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18968/NA18968_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18969/NA18969_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18971/NA18971_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18972/NA18972_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18974/NA18974_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18977/NA18977_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18980/NA18980_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18981/NA18981_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18983/NA18983_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18988/NA18988_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA18989/NA18989_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19001/NA19001_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19003/NA19003_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19011/NA19011_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19012/NA19012_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19017/NA19017_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19019/NA19019_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19024/NA19024_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19027/NA19027_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19028/NA19028_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19031/NA19031_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19037/NA19037_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19043/NA19043_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19055/NA19055_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19059/NA19059_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19068/NA19068_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19070/NA19070_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19080/NA19080_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19086/NA19086_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19096/NA19096_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19101/NA19101_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19113/NA19113_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19114/NA19114_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19118/NA19118_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19119/NA19119_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19122/NA19122_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19127/NA19127_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19128/NA19128_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19129/NA19129_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19137/NA19137_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19144/NA19144_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19146/NA19146_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19147/NA19147_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19153/NA19153_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19189/NA19189_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19197/NA19197_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19207/NA19207_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19238/NA19238_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19307/NA19307_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19310/NA19310_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19315/NA19315_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19319/NA19319_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19327/NA19327_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19328/NA19328_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19331/NA19331_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19338/NA19338_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19347/NA19347_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19350/NA19350_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19351/NA19351_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19355/NA19355_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19383/NA19383_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19385/NA19385_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19391/NA19391_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19393/NA19393_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19397/NA19397_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19399/NA19399_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19403/NA19403_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19439/NA19439_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19449/NA19449_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19463/NA19463_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19472/NA19472_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19651/NA19651_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19652/NA19652_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19654/NA19654_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19655/NA19655_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19657/NA19657_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19658/NA19658_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19660/NA19660_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19661/NA19661_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19663/NA19663_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19664/NA19664_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19669/NA19669_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19675/NA19675_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19676/NA19676_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19679/NA19679_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19700/NA19700_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19701/NA19701_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19703/NA19703_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19707/NA19707_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19711/NA19711_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19717/NA19717_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19720/NA19720_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19723/NA19723_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19728/NA19728_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19729/NA19729_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19734/NA19734_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19735/NA19735_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19740/NA19740_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19747/NA19747_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19749/NA19749_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19750/NA19750_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19758/NA19758_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19759/NA19759_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19762/NA19762_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19770/NA19770_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19774/NA19774_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19782/NA19782_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19786/NA19786_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19789/NA19789_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19818/NA19818_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19819/NA19819_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19828/NA19828_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19834/NA19834_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19835/NA19835_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19900/NA19900_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19901/NA19901_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19904/NA19904_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19908/NA19908_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19909/NA19909_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19916/NA19916_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA19921/NA19921_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20127/NA20127_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20276/NA20276_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20278/NA20278_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20281/NA20281_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20289/NA20289_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20294/NA20294_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20298/NA20298_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20314/NA20314_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20332/NA20332_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20334/NA20334_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20342/NA20342_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20346/NA20346_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20348/NA20348_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20356/NA20356_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20357/NA20357_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20359/NA20359_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20503/NA20503_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20504/NA20504_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20505/NA20505_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20514/NA20514_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20520/NA20520_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20525/NA20525_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20530/NA20530_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20531/NA20531_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20532/NA20532_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20534/NA20534_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20536/NA20536_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20538/NA20538_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20539/NA20539_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20540/NA20540_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20585/NA20585_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20587/NA20587_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20588/NA20588_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20753/NA20753_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20757/NA20757_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20761/NA20761_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20762/NA20762_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20764/NA20764_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20769/NA20769_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20775/NA20775_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20778/NA20778_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20785/NA20785_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20787/NA20787_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20795/NA20795_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20801/NA20801_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20805/NA20805_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20810/NA20810_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20813/NA20813_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20822/NA20822_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20846/NA20846_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20847/NA20847_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20852/NA20852_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20853/NA20853_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20858/NA20858_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20861/NA20861_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20863/NA20863_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20866/NA20866_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20867/NA20867_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20876/NA20876_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20885/NA20885_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20888/NA20888_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20890/NA20890_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20896/NA20896_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20899/NA20899_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20900/NA20900_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA20901/NA20901_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA21098/NA21098_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA21099/NA21099_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA21101/NA21101_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA21102/NA21102_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA21103/NA21103_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA21110/NA21110_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA21111/NA21111_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA21113/NA21113_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA21114/NA21114_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA21117/NA21117_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA21118/NA21118_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA21120/NA21120_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA21124/NA21124_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA21126/NA21126_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA21127/NA21127_norm.vcf.gz`
- `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/NA21142/NA21142_norm.vcf.gz`

## Confidence and caveats

- High confidence: steps 1–3 and 5, because their exact commands and dates are embedded in the VCF header and agree with surviving scripts/logs.
- High confidence: step 4, because the before/after headers show exactly the added contig lengths, the output timestamp matches job 21127420, and job 21127471 records the follow-up indexing.
- High confidence: step 6 sorting/indexing, because script paths, Slurm timing, output mtimes, and the bcftools temporary-directory message agree.
- Inferred: the final move from `/home/dkhlebnikov/SV/1KG` to `/home/dkhlebnikov/SV/1KG/prepare_fc1`; no command record survives.
- The names `merged.norm` and `noY` are shorthand. The former resulted from split/left-align, length filtering, exact deduplication, and sorting; the latter removed chrY **and** all noncanonical contigs.
