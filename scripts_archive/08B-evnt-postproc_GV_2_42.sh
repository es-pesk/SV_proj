#!/bin/bash
#SBATCH --job-name=08-GV_postproc
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=20G
#SBATCH --output=./logs/08-GV-postproc_%a.out
#SBATCH --error=./logs/08-GV-postproc_%a.err
#SBATCH --array=1-57

source ~/miniforge3/etc/profile.d/conda.sh
mamba activate SVproj

module load bedtools2
module load bcftools
bed2vcf="./tools/bedgovcf"

file=$(sed -n "${SLURM_ARRAY_TASK_ID}p" bam_list.txt)
libnum=$(basename "$file" | cut -f 1 -d'.')
subdir=$(basename $(dirname "$file"))
vcf_outdir="vcf_out/${subdir}"
norm_vcf_outdir="vcf_norm/${subdir}"

mkdir -p ${vcf_outdir}
mkdir -p ${norm_vcf_outdir}


yaml="./08-bedgovcf_GV_2_42.yaml"
ref="ref/GRCh38.p14.filtered.fa"

tmp_bed="${libnum}.${subdir}.bed"
ref_tsv="${libnum}.${subdir}.ref.fa.tsv"
vcf_like="${libnum}.${subdir}.VCFlike.tsv"
vcf_like_srt="${libnum}.${subdir}.VCFlike.srt.tsv"
vcf_out="${vcf_outdir}/${libnum}.vcf"
vcf_norm="${norm_vcf_outdir}/${libnum}_norm.vcf"

echo "Processing ${libnum} from ${subdir}..."


python evnt2bed_new.py \
  --evnt gv_out/${subdir}/${libnum}.F50A20.evnt \
  --out-bed "$tmp_bed"

bedtools getfasta -fi "$ref" -bed "$tmp_bed" -bedOut -tab > "$ref_tsv"

python tmp_bed2vcf_new.py \
  --evnt gv_out/${subdir}/${libnum}.F50A20_filt.evnt \
  --ref-tsv ${ref_tsv} \
  --out-tsv ${vcf_like}

sort -k1,1V -k2,2n ${vcf_like} > ${vcf_like_srt}
"$bed2vcf" --bed ${vcf_like_srt} --config ${yaml} --fai ${ref}.fai > ${vcf_out}

bgzip $vcf_out -o ${vcf_out}.gz

tabix -f -p vcf ${vcf_out}.gz

rm -f ${ref_tsv} ${vcf_like} ${vcf_like_srt}

bcftools norm -f "$ref" "${vcf_out}.gz" -Oz -o "${vcf_norm%.vcf}.norm.vcf.gz"
tabix -f -p vcf "${vcf_norm%.vcf}.norm.vcf.gz"
