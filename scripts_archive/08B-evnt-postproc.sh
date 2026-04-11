#!/bin/bash
#SBATCH --job-name=08-GV_postproc
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=20G
#SBATCH --output=./logs/08-GV-postproc_%a.out
#SBATCH --error=./logs/08-GV-postproc_%a.err
#SBATCH --array=1-57


module load bedtools2
bed2vcf="./tools/bedgovcf"

file=$(sed -n "${SLURM_ARRAY_TASK_ID}p" bam_list.txt)
libnum=$(basename "$file" | cut -f 1 -d'.')
subdir=$(basename $(dirname "$file"))
vcf_outdir="vcf_out/${subdir}"

mkdir -p ${vcf_outdir}
echo "Processing ${libnum} from ${subdir}..."


# parse GeneVar evnt, create bed
awk -F'\t' -v OFS='\t' '
NR==1 {
    for (i=1;i<=NF;i++) h[$i]=i
    next
}
$h["Type"]!="no_event" && $h["Type"]!="Error" {
    Pos_G = $h["Pos_G"]
    Length = $h["Length"]
    End_G = Pos_G + Length + 1 
    print $h["Chr"], Pos_G, End_G
}
' gv_out/${subdir}/${libnum}.F50A20.evnt > ${libnum}.${subdir}.bed


# get fasta for reference
bedtools getfasta -fi ref/GRCh38.p14.filtered.fa \
    -bed ${libnum}.${subdir}.bed -bedOut \
    -tab > ${libnum}.${subdir}.ref.fa.tsv

# Join reference back to events
awk -F'\t' -v OFS='\t' '
FNR==NR {
    key = $1"_"$2"_"$3;
    ref[key] = $4;
    next;
}
NR==1 {
    for (i=1;i<=NF;i++) h[$i]=i
    print \
      "Chr","Pos_G","End_G","Length","Type","L_Ins", \
      "Ref_Seq","Ins_Seq","AV_Score","Support","Reads"
    next
}
$h["Type"]!="no_event" && $h["Type"]!="Error" {
    Pos_G = $h["Pos_G"]
    Length = $h["Length"]
    End_G = Pos_G + Length +1

    key = $h["Chr"]"_"Pos_G"_"End_G
    RefSeq = (key in ref ? ref[key] : "")

    print \
      $h["Chr"], Pos_G + 1, End_G, Length, $h["Type"], \
      $h["L_Ins"], RefSeq, $h["Ins_Seq"], \
      $h["AV_Score"], $h["Support"], $h["Reads"]
}
' ${libnum}.${subdir}.ref.fa.tsv gv_out/${subdir}/${libnum}.F50A20.evnt > ${libnum}.${subdir}.evnt


# vcf-like tab-separated file
awk -F'\t' -v OFS='\t' '
function parse_gt(x,   y) {
    if (x=="" || x=="[]" ) return "."
    gsub(/[\[\]]/, "", x)
    split(x, y, ",")
    split(y[1], y, "\\$")
    return y[2]
}
NR==1 { next }
{
    Chr=$1
    pad=$2
    Pos=$3
    End=$4
    Length=$5
    Type=toupper($6)
    LIns=$7
    Ref=$8
    Alt=$9
    AV=$10
    Support=$11
    Reads=$12

    SVLEN = LIns - Length
    ID = Chr"_"Pos"_"End"_"Type"_"

    print Chr, Pos, ID, Ref, Alt, ".", "PASS", \
          End, SVLEN, Type, Support, AV, \
          parse_gt(Reads), Support
}
' ${libnum}.${subdir}.evnt | sort -k1,1V -k2,2n \
    > ${libnum}.${subdir}.VCFlike.srt.tsv

${bed2vcf} --bed ${libnum}.${subdir}.VCFlike.srt.tsv \
    --config ./08-bedgovcf.yaml \
    --fai ref/GRCh38.p14.filtered.fa.fai \
    > ${vcf_outdir}/${libnum}.vcf

bgzip ${vcf_outdir}/${libnum}.vcf -o ${vcf_outdir}/${libnum}.vcf.gz
tabix -f -p vcf ${vcf_outdir}/${libnum}.vcf.gz

rm ${libnum}.${subdir}.bed ${libnum}.${subdir}.ref.fa.tsv
rm ${libnum}.${subdir}.evnt ${libnum}.${subdir}.VCFlike.srt.tsv
