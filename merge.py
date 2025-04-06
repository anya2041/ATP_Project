import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as pl
import seaborn as sns

########################### Part 1: Merging Data ###################
bfold = "C:/Users/Anya/Projects/ATP_Project/D1-16"
output_dir = "C:/Users/Anya/Projects/ATP_Project"

emoblo = {"E1": "Happy", "E2": "Angry", "E3": "Neutral"}
allmerge = {block: {"Cued": [], "Uncued": []} for block in emoblo.keys()}

# Get all participant folders inside the base directory
ppt = [p for p in os.listdir(bfold) if os.path.isdir(os.path.join(bfold, p))]

for part in ppt:
    part_path = os.path.join(bfold, part)
    
    for bl, emo in emoblo.items():
        bl_path = os.path.join(part_path, bl)
        cued_dlist = []
        uncued_dlist = []

        for run in ["1", "2"]:
            run_path = os.path.join(bl_path, run)
            cued_file = os.path.join(run_path, "target_cued.csv")
            uncued_file = os.path.join(run_path, "target_uncued.csv")

            if os.path.exists(cued_file):
                cued_data = pd.read_csv(cued_file)
                cued_data["Participant"] = part  # Fix participant assignment
                cued_data["Emotion"] = emo
                cued_data["Validity"] = "Cued"
                cued_dlist.append(cued_data)

            if os.path.exists(uncued_file):
                uncued_data = pd.read_csv(uncued_file)
                uncued_data["Participant"] = part
                uncued_data["Emotion"] = emo
                uncued_data["Validity"] = "Uncued"
                uncued_dlist.append(uncued_data)

        if cued_dlist:
            merged_cued = pd.concat(cued_dlist, ignore_index=True)
            allmerge[bl]["Cued"].append(merged_cued)

        if uncued_dlist:
            merged_uncued = pd.concat(uncued_dlist, ignore_index=True)
            allmerge[bl]["Uncued"].append(merged_uncued)

print("\nData merging complete!")

# Save final merged data with absolute paths
for bl, emotion in emoblo.items():
    if allmerge[bl]["Cued"]:
        final_cued = pd.concat(allmerge[bl]["Cued"], ignore_index=True)
        final_cued_path = os.path.join(output_dir, f"{bl}_final_merged_cued.csv")
        final_cued.to_csv(final_cued_path, index=False)
        print(f"Saved: {final_cued_path}")

    if allmerge[bl]["Uncued"]:
        final_uncued = pd.concat(allmerge[bl]["Uncued"], ignore_index=True)
        final_uncued_path = os.path.join(output_dir, f"{bl}_final_merged_uncued.csv")
        final_uncued.to_csv(final_uncued_path, index=False)
        print(f"Saved: {final_uncued_path}")

print("\nFinal merged data saved. Yes, it works finally!")

#################### Part 2: Extracting Columns/Slicing CSV ##################

def slicer(file_path):
    df = pd.read_csv(file_path)
    selected_col = ["response_time", "location", "cue_location"]

    if "t87" not in df.columns:
        raise ValueError("Can't find column named 't87'. Check CSV file.")
    
    pupil_dcol = df.columns[df.columns.get_loc("t87"):]
    f_col = selected_col + list(pupil_dcol)
    df_filt = df[f_col]
    return df_filt

# Process each block and condition
for bl in emoblo.keys():
    for validity in ["Cued", "Uncued"]:
        file_name = os.path.join(output_dir, f"{bl}_final_merged_{validity}.csv")
        
        try:
            extracted_df = slicer(file_name)
            extracted_output_file = os.path.join(output_dir, f"{bl}-clean-{validity}.csv")
            extracted_df.to_csv(extracted_output_file, index=False)
            print(f"Extracted + Saved the file: {extracted_output_file}")
        
        except Exception as e:
            print(f"Error processing {file_name}: {e}")

##################### Merge + Slice Code Ends #######################