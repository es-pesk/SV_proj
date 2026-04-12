#!/bin/bash

ref="ref/GRCh38.p14.filtered.fa"
yaml="./08-bedgovcf_GV_2_42.yaml"
bed2vcf="./tools/bedgovcf"


python evnt2bed_new.py --evnt ./GeneVar_2_42_linux/example_res/NA12878.F50A20.example.evnt  --out-bed ./GeneVar_2_42_linux/example_res/NA12878.F50A20.example.bed

bedtools getfasta -fi "$ref" -bed ./GeneVar_2_42_linux/example_res/NA12878.F50A20.example.bed  -bedOut -tab > ./GeneVar_2_42_linux/example_res/NA12878.F50A20.example.with_ref.bed

python tmp_bed2vcf_new.py --evnt ./GeneVar_2_42_linux/example_res/NA12878.F50A20.example_filt.evnt --ref-tsv ./GeneVar_2_42_linux/example_res/NA12878.F50A20.example.with_ref.bed  --out-tsv ./GeneVar_2_42_linux/example_res/NA12878.F50A20.example.vcf_like.tsv


sort -k1,1V -k2,2n ./GeneVar_2_42_linux/example_res/NA12878.F50A20.example.vcf_like.tsv  > ./GeneVar_2_42_linux/example_res/NA12878.F50A20.example.vcf_like.sort.tsv
"$bed2vcf" --bed ./GeneVar_2_42_linux/example_res/NA12878.F50A20.example.vcf_like.sort.tsv --config ${yaml} --fai ${ref}.fai > ./GeneVar_2_42_linux/example_res/NA12878.F50A20.example.vcf

bgzip ./GeneVar_2_42_linux/example_res/NA12878.F50A20.example.vcf -o ./GeneVar_2_42_linux/example_res/NA12878.F50A20.example.vcf.gz

tabix -f -p vcf ./GeneVar_2_42_linux/example_res/NA12878.F50A20.example.vcf.gz


#bcftools norm -f "$ref" -m -any ./GeneVar_2_42_linux/example_res/NA12878.F50A20.example.vcf.gz -Oz -o ./GeneVar_2_42_linux/example_res/NA12878.F50A20.example.norm.vcf.gz
#tabix -f -p vcf ./GeneVar_2_42_linux/example_res/NA12878.F50A20.example.norm.vcf.gz

bcftools norm -f "$ref" ./GeneVar_2_42_linux/example_res/NA12878.F50A20.example.vcf.gz -Oz -o ./GeneVar_2_42_linux/example_res/NA12878.F50A20.example.norm.vcf.gz
tabix -f -p vcf ./GeneVar_2_42_linux/example_res/NA12878.F50A20.example.norm.vcf.gz










