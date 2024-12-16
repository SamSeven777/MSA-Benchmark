import os
import pandas as pd

csv_path = "result/accuracy/"

files = {
    "bb_ref.csv": "ref",
    "clustalw.csv": "clustalw",
    "muscle.csv": "muscle",
    "t-coffee.csv": "t-coffee"
}

merged_df = None

for file, prefix in files.items():
    # Read the CSV file
    df = pd.read_csv(os.path.join(csv_path, file))
    # Rename the columns except for the 'Dataset' column
    df = df.rename(columns={
        "SP_score": f"{prefix}_sp",
        "CS_score": f"{prefix}_cs"
    })
    
    # Merge with the existing dataframe
    if merged_df is None:
        merged_df = df
    else:
        merged_df = pd.merge(merged_df, df, on="Dataset", how="outer")

merged_df.to_csv(os.path.join(csv_path, "merged.csv"), index=False)