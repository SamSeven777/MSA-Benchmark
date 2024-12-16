# MSA-Benchmark
Code for CS466 Project

This repository contains code and results for benchmarking multiple sequence alignment (MSA) tools: **ClustalW**, **T-Coffee**, and **MUSCLE**. The benchmark evaluates their accuracy, runtime, and memory usage using BAliBASE reference datasets and COVID-19 RNA sequence families.

## Usage Instructions

Use `alignment.py` to generate alignments for the datasets.

Use `merge_csv.py` to merge csv file for tools and datasets.

Use `convert.py` to convert `.afa` FASTA file from MUSCLE to Clustal `.aln` file.

Use `accuracy.py` to compute SP and CS scores for the generated alignments.

Open `visual.ipynb` in Jupyter Notebook to visualize accuracy, runtime, and memory usage.

## Results Overview

The benchmark results are summarized as follows:

- Accuracy: Evaluated using SP (Sum-of-Pairs) and CS (Column Score) metrics.
- Performance: Measured in runtime and memory usage.
  
## Dependencies

The following tools and Python libraries are required:

-   MSA Tools:
    -    ClustalW
    -   T-Coffee
    -   MUSCLE
-   Python Libraries:
    -   Biopython
    -   pandas
    -   matplotlib
    -   numpy
    -   psutil
    -   subprocess
    -   csv
    -   os

## Acknowledgments

- BAliBASE: The benchmarking datasets are sourced from the official website.
- Rfam: COVID-19 RNA sequences are obtained from the Rfam database.