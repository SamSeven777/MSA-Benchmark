import os
import csv

from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment

# Function to calculate SP score
def sum_of_pairs_score(alignment: MultipleSeqAlignment) -> int:
    # Convert the alignment into a list of sequences
    seqs = [str(record.seq) for record in alignment]
    
    sp_score = 0
    num_seqs = len(seqs)
    
    # Compare each pair of sequences
    for i in range(num_seqs):
        for j in range(i + 1, num_seqs):
            seq1 = seqs[i]
            seq2 = seqs[j]
            
            # Compare the sequences column by column
            pair_score = sum(1 for a, b in zip(seq1, seq2) if a == b and a != '-')
            sp_score += pair_score
            
    return sp_score

# Function to calculate CS score
def column_score(alignment: MultipleSeqAlignment) -> int:
    # Convert the alignment into a list of sequences
    seqs = [str(record.seq) for record in alignment]
    
    cs_score = 0
    num_seqs = len(seqs)
    num_columns = len(seqs[0])
    
    # Compare each column (position) across all sequences
    for i in range(num_columns):
        column = [seq[i] for seq in seqs]
        
        # Check if all non-gap characters in the column are the same
        if len(set(column) - {'-'}) == 1:
            cs_score += 1
            
    return cs_score

def calculate_scores(clustal_file):
    # Read the Clustal format alignment
    alignment = AlignIO.read(clustal_file, "clustal")
    
    # Calculate SP and CS scores
    sp_score = sum_of_pairs_score(alignment)
    cs_score = column_score(alignment)
    
    return sp_score, cs_score

def calculate_scores_msf(msf_file):
    alignment = AlignIO.read(msf_file, "msf")
    
    sp_score = sum_of_pairs_score(alignment)
    cs_score = column_score(alignment)
    
    return sp_score, cs_score

def record_ac(tool):
    files = os.listdir(f"result/aligned/{tool}")
    with open(f"result/accuracy/{tool}.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Dataset", "SP_score", "CS_score"])
        for file in files:
            sp, cs = calculate_scores(f"result/aligned/{tool}/{file}")
            name = file.split('_')[1]
            writer.writerow([name[:-4], sp, cs])

for tool_name in ["clustalw", "muscle", "t-coffee"]:
    record_ac(tool_name)
'''
bb_path= "dataset/BAliBASE_R1-5/bb3_release"
bb_ref = ['RV11', 'RV12', 'RV20', 'RV30', 'RV40', 'RV50']

with open("result/accuracy/bb_ref.csv", 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Dataset', 'SP_score', 'CS_score'])
    for ref in bb_ref:
        path = os.path.join(bb_path, ref)
        files = os.listdir(path)
        for file in files:
            if file[-3:] == 'msf':
                sp, cs = calculate_scores_msf(os.path.join(path, file))
                writer.writerow([file[:-4], sp, cs])\
'''