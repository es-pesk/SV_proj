# SVLEN inconsistency: origin, propagation, and impact on Truvari collapse

Report date: 2026-10-01 (America/Los_Angeles)

## Executive conclusion

The incorrect `INFO/SVLEN` values were already present in the per-sample VCFs
created by the historical Flycatcher pipeline. They were not introduced by the
cohort merge, the later normalization/filtering workflow, or Truvari collapse.

The first confirmed point at which an invalid value exists is Flycatcher Step 4,
the GeneVar `.evnt`-to-VCF conversion performed by `parse-genvar`. The historical
converter calculated `SVLEN` from the numeric GeneVar fields `LIns-LDel`, while it
constructed REF and ALT from independently selected sequence fields. It did not
require these two representations to agree.

The converter's same-position deduplication made this especially unsafe: it could
select maximum `LIns` and `LDel` values independently from the first available
insertion/deletion sequences in a group. Consequently, a VCF record could contain
an SVLEN derived from one event and an ALT sequence derived from another.

The original `.evnt` file for the traced sample was deleted after processing.
Therefore, for an individual record it is no longer possible to distinguish with
absolute certainty between:

1. GeneVar itself reporting an `LIns` inconsistent with `InsSeq`; and
2. `parse-genvar` same-position deduplication combining numeric lengths and
   sequences from different events.

In either case, the defect entered the VCF lineage at the `parse-genvar` boundary.
The converter should have calculated final SVLEN from the final emitted REF/ALT
alleles and rejected inconsistent inputs.

The problem affects Truvari collapse because the version used, Truvari 5.4.0,
prefers `INFO/SVLEN` over REF/ALT when determining variant size. It uses that size
for minimum/maximum-size filtering, 95% size-similarity matching, size-based
candidate clustering, and comparison ordering. The existing collapsed callset
therefore cannot be assumed to represent collapse decisions based on actual allele
lengths.

## Definitions

For the sequence-resolved, biallelic records under discussion, the VCF header
defines:

```text
signed SVLEN = len(ALT) - len(REF)
absolute allele-length change = abs(len(ALT) - len(REF))
```

The historical sample VCF header describes `SVLEN` as:

```text
Length difference between REF and ALT alleles
```

A record is inconsistent when its stored signed `INFO/SVLEN` differs from
`len(ALT)-len(REF)`.

## Representative record traced through the pipeline

The audit traced this record:

```text
CHROM:POS = chr1:10462
sample    = HG02332
ID        = chr1_10462_10486_REPLACE_
SVTYPE    = REPLACE
REF       = TAACCCTCGCGGTACCCTCAGCCGG  (25 bases)
ALT       = CGCGGTGCCCCC                 (12 bases)
stored SVLEN = 1
correct SVLEN = 12 - 25 = -13
genotype      = 1/1
```

The stored and correct values differ in both magnitude and sign.

### Trace result

| Stage | File or operation | Stored SVLEN | Finding |
|---|---|---:|---|
| Primary data | HG02332 CRAM | N/A | No VCF SVLEN exists yet |
| Flycatcher Step 4 | `HG02332.vcf.gz` | 1 | Already incorrect |
| Per-sample normalization | `HG02332_norm.vcf.gz` | 1 | Preserved |
| Cohort merge | `1kGP.no.missing.to.ref.vcf.gz` | 1 | Preserved |
| Split/left-align and length filter | preparation workflow | 1 | Preserved |
| Pre-Truvari canonical-contig VCF | `...noY.sorted.vcf.gz` | 1 | Preserved |
| Truvari per-chromosome input | `chr1.input.vcf.gz` | 1 | Preserved |
| Truvari collapsed output | `chr1.collapsed.vcf.gz` and concatenated VCF | 1 | Preserved |

This trace rules out the cohort merge, later bcftools processing, and Truvari as
the creator of this example's bad annotation.

## Confirmed origin in the historical Flycatcher workflow

The HG02332 array log records the following sequence:

```text
Step 1: cigar-seg
Step 2: generate-grp
Step 3: GeneVar 2.42
Step 4: parse-genvar
Step 5: bcftools norm
```

For HG02332, Step 4 reported:

```text
events retained: 356576
deduplication: 356576 -> 331665 events (24911 merged)
VCF: 330037 records written
```

The incorrect record exists in the Step 4 output before Step 5 normalization.

### Historical converter logic

The historical `parse-genvar` implementation constructed the output fields from
different sources:

```text
REF    = reference sequence spanning the selected LDel
ALT    = GeneVar InsSeq
SVLEN  = GeneVar LIns - GeneVar LDel
```

The relevant implementation is in:

`/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/generateGRP/src/parse_genvar.rs`

At the same-position deduplication step, it independently selected:

```text
total_ldel = maximum LDel in the group
total_lins = maximum LIns in the group
del_seq    = first nonempty DelSeq in the group
ins_seq    = first nonempty InsSeq in the group
```

It then wrote:

```rust
let svlen = ev.lins - ev.ldel;
rec.set_alleles(&[ref_seq.as_bytes(), alt_seq.as_bytes()])?;
rec.push_info_integer(b"SVLEN", &[svlen])?;
```

No validation required `SVLEN == len(ALT)-len(REF)`.

For the traced record, the output fields imply approximately:

```text
LDel = 25
LIns = 26
emitted InsSeq length = 12
```

Thus the converter wrote `26-25 = 1`, while its emitted allele strings require
`12-25 = -13`.

## What is confirmed and what remains uncertain

### Confirmed

- The bad value is present in the Flycatcher-created per-sample VCF before
  per-sample `bcftools norm`.
- The historical converter derived SVLEN from numeric `LIns/LDel`, not from the
  final REF/ALT strings.
- Its deduplication could mix maxima and sequences from different same-position
  events.
- The subsequent pipeline preserved the traced bad value.
- Truvari 5.4.0 used stored SVLEN as its preferred size source.

### Not recoverable from surviving files

The intermediate HG02332 `.evnt`, filtered `.evnt`, and `.grp` files no longer
exist. Therefore, the exact upstream cause for each individual record cannot be
separated into "GeneVar emitted internally inconsistent columns" versus
"parse-genvar combined consistent events inconsistently."

This uncertainty does not change the remediation: final VCF annotations must be
derived from and validated against the final emitted alleles.

## Sample-level measurement

The HG02332 sample was audited before and after per-sample normalization:

| File | Records | Stored SVLEN different from REF/ALT difference | Stored `abs(SVLEN)<2` while actual change is at least 2 |
|---|---:|---:|---:|
| `HG02332.vcf.gz` | 330,037 | 170,905 (51.7836%) | 188 |
| `HG02332_norm.vcf.gz` | 329,987 | 170,878 (51.7833%) | 188 |

The 188 directly relevant sub-2 mismatches in both files were:

| SVTYPE | Count |
|---|---:|
| REPLACE | 175 |
| INSERTION | 13 |

The unchanged count before and after normalization demonstrates that per-sample
`bcftools norm` did not introduce this error class in HG02332.

The broader mismatch count includes systematic allele-representation differences,
especially for deletions, and should not be interpreted as 170,905 independent
catastrophic calls. Nevertheless, the VCF header's stated SVLEN definition is not
being satisfied, and the sub-2 discrepancies are unambiguous for the failed length
analysis.

## Propagation through the preparation workflow

The later preparation workflow performed the following operations:

1. Normalize individual sample callsets.
2. Merge 967 normalized sample VCFs.
3. Split multiallelic records and left-align alleles.
4. Filter on direct REF/ALT length difference of at least 2 bp.
5. Remove exact duplicates and sort.
6. Repair header contig declarations.
7. Retain chr1-chr22 and chrX.
8. Run per-chromosome Truvari collapse and concatenate results.

The direct REF/ALT filter correctly allowed the traced record because its actual
absolute allele-length change is 13 bp. Its stale `SVLEN=1` was not repaired by
that filter or by later steps.

The complete preparation provenance is documented in:

`/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.len2.merged.norm.fixed_header.noY.sorted.provenance.md`

## Impact on Truvari collapse

The final FC3 collapsed catalog was generated with Truvari 5.4.0 and parameters:

```bash
truvari collapse \
  -r 500 \
  -p 0.95 \
  -P 0.95 \
  -s 50 \
  -S 100000
```

In this Truvari version, `VariantRecord.var_size()` first reads `INFO/SVLEN` and
uses REF/ALT only when a usable SVLEN is absent. The stored value therefore
affected:

1. **Minimum/maximum size filtering.** With `--sizemin 50`, a true variant of at
   least 50 bp carrying a stored SVLEN below 50 was excluded from collapse
   comparisons. Filtered records were still written unchanged to the retained
   output, explaining why short stored values remain in the collapsed VCF.
2. **Size similarity.** `--pctsize 0.95` required the stored sizes to be at least
   95% similar. Incorrect values could reject biologically equivalent calls.
3. **Candidate sub-clustering.** Truvari divided dense chunks into size-compatible
   groups using the same stored sizes. Incorrectly separated records might never
   have been compared.
4. **Ordering and short-circuiting.** Stored sizes influenced call ordering and
   when candidate scanning stopped.

The expected dominant bias is under-collapsing: true duplicate representations
can remain as separate records because bad sizes excluded them or made them appear
size-incompatible. False collapsing is also possible when different alleles share
similar incorrect sizes. The 95% sequence-similarity threshold reduces some false
matches for sequence-resolved records, but it cannot repair size filtering or
candidate partitioning that happened first.

The failed corrected plotting run found 157,842 retained FC3 records with stored
`abs(INFO/SVLEN)<2` among 82,507,518 collapsed records (0.191306%). These are only
the immediately visible failures; records with stored values above 2 can still
have materially wrong sizes.

Consequently, recalculating SVLEN only after collapse would correct annotations and
plots, but would not correct the historical collapse decisions.

## Recommended correction

The rigorous correction should start from the pre-Truvari, canonical-contig VCF:

`/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.len2.merged.norm.fixed_header.noY.sorted.vcf.gz`

Recommended procedure:

1. Preserve the existing input and collapsed VCFs as immutable provenance.
2. For every sequence-resolved biallelic record, set signed
   `SVLEN=len(ALT)-len(REF)`.
3. Treat symbolic alleles separately; they require reliable event metadata rather
   than string-length calculation.
4. Validate every corrected sequence-resolved record against REF/ALT.
5. Confirm that END is consistent with the emitted REF/reference span.
6. Index the corrected pre-collapse VCF.
7. Rerun the same per-chromosome Truvari 5.4.0 collapse parameters.
8. Concatenate and index a new corrected collapsed callset in a new directory.
9. Compare old and corrected input/output counts, representatives, collapse-group
   membership, and genotype consolidation.
10. Rerun the FC3-versus-Shapeit plots using REF/ALT-derived allele length.

The newer Flycatcher implementation already follows the appropriate design. It
can reject disagreement between GeneVar `LIns` and `InsSeq`, derives final SVLEN
from final REF/ALT, retains original numeric values as `ORIG_LINS` and
`ORIG_LDEL`, and provides an explicit SVLEN validation check.

## Related paths

### Traced source and job evidence

- HG02332 sample VCF before normalization:
  `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02332/HG02332.vcf.gz`
- HG02332 normalized VCF:
  `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/HG02332/HG02332_norm.vcf.gz`
- HG02332 Flycatcher job log:
  `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/logs/fc-1kgp_15894688_383.log`
- Historical cohort array script:
  `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/scripts/archived/run-pipeline.sh`
- Historical converter source:
  `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/generateGRP/src/parse_genvar.rs`

### Cohort and Truvari inputs/outputs

- Upstream merged cohort VCF:
  `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/1kGP-results/1kGP.no.missing.to.ref.vcf.gz`
- Pre-Truvari canonical-contig VCF:
  `/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.len2.merged.norm.fixed_header.noY.sorted.vcf.gz`
- Chr1 Truvari input:
  `/home/dkhlebnikov/SV/1KG/prepare_fc1/truvari_perchr_korbel_params/chr1.input.vcf.gz`
- Chr1 retained collapsed output:
  `/home/dkhlebnikov/SV/1KG/prepare_fc1/truvari_perchr_korbel_params/chr1.collapsed.vcf.gz`
- Final concatenated collapsed output:
  `/home/dkhlebnikov/SV/1KG/prepare_fc1/1kGP.no.missing.to.ref.len2.truvari-collapsed.vcf.gz`
- Chr1 Truvari command/version log:
  `/home/dkhlebnikov/SV/1KG/truVarKorParams_1kg.21312953_1.err`

### Truvari implementation used

- Size selection and REF/ALT fallback:
  `/home/dkhlebnikov/miniforge3/envs/cigar-plots/lib/python3.11/site-packages/truvari/variant_record.py`
- Collapse implementation:
  `/home/dkhlebnikov/miniforge3/envs/cigar-plots/lib/python3.11/site-packages/truvari/collapse.py`
- Matching/filtering implementation:
  `/home/dkhlebnikov/miniforge3/envs/cigar-plots/lib/python3.11/site-packages/truvari/matching.py`

### Current corrected Flycatcher design

- Current event-to-VCF logic:
  `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/Flycatcher/src/evnt.rs`
- Current validation logic:
  `/net/seq/data/projects/sasha/claude-code-sandbox/workspace/flycatcher/daniil/Flycatcher/src/validate.rs`

### Existing analysis report

- Plotting bugfix and failed-run report:
  `/home/dkhlebnikov/SV/1KG/prepare_fc1/fc3_vs_shapeit_allele_length_fixed/BUGFIX_RUN_REPORT.md`

## Final assessment

The SVLEN problem is a historical VCF-construction defect at the GeneVar-to-VCF
conversion boundary. It was observable before normalization and then propagated
unchanged through the downstream cohort workflow. Because Truvari used those
stored values for collapse filtering and matching, the existing collapsed catalog
should be treated as affected. A defensible correction requires repairing and
validating SVLEN before rerunning Truvari collapse.
