
BAM2BED SAM2BAM: measles.*
------------------------------
measles.sam, measles.sam and measles.bed were created as follows using a
paired-end data set of 120 reads.


::

    bwa mem -t 4 -R "@RG\tID:1\tSM:1\tPL:illumina" -T 30 measles.fa 1_R1_.fastq.gz 1_R2_.fastq.gz  > measles.sam
    samtools view -Sbh measles.sam > measles.bam
    samtools sort -o measles.sorted.bam measles.bam


FastQ2FastA
---------------------------

test_fastq_1.fastq  and test_fasta_1.fasta : 2 reads
