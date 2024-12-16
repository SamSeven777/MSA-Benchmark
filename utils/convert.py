import os
from Bio import AlignIO

# Function to convert FASTA to Clustal format
def fasta_to_clustal(fasta_file, clustal_file):
    # Read the alignment from the FASTA file
    alignment = AlignIO.read(fasta_file, "fasta")
    
    # Write the alignment to a Clustal format file
    with open(clustal_file, "w") as out_file:
        AlignIO.write(alignment, out_file, "clustal")

files = os.listdir()
for file in files:
    output = file[:-4] + '.aln'
    fasta_to_clustal(file, output)
