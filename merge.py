import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as pl
import seaborn as sns

########################### part 1:merging data ###################
bfold = "C:/Users/Anya/Projects/ATP_Project/D1-16"
out_dir = "C:/Users/Anya/Projects/ATP_Project"
#this is for my base folder Or the directory name where i extracted the zip file
# in my experiment the alloted folder was D1-16
#also as there were 10 particiants in D1-16 but one particilpant's data of E3 folder was missing i.e. ASR was not present so i have only 9 folders now in D1-16 so i had done analysis for them. I mailed the TA about this too. 
#out_dir is the output directory where i want to save the final merged csv files. because whenever i extract folder and run merge.py and if it doesnt have out_dir then error is shown ,specifically RWR error(read-write error) which means merging happens and slicer function clash, i realised this later. so, 

emoblo = {"E1": "Happy", "E2": "Angry", "E3": "Neutral"}
#emoblo is a dict where i have kept the block name E1,E2,E3 as key and the emotion as value (Happy, Angry, Neutral) as given in the asignment guidelines.

allmerge = {block: {"Cued": [], "Uncued": []} for block in emoblo.keys()}
#allmerge is for storing merged data of 9 participants blockwise and for condition wise too. it's a dictionary as well.

ppt = [p for p in os.listdir(bfold) if os.path.isdir(os.path.join(bfold, p))] #this is participants (ppt) to get their folders inside the big folder.

for part in ppt:
    part_path = os.path.join(bfold, part) # Path of participant's folder
    #print(f"Processing participant: {participant}") # this is put for debug purpose i dont want to delete it.
    
    for bl, emo in emoblo.items(): #for loop over blocks and their emotions
        bl_path = os.path.join(part_path, bl) 
        cued_dlist = [] # here i've just given empty list for cued/valid and uncued/invalid traisls
        uncued_dlist = []

        for run in ["1", "2"]:   # for loop to go over the folder indide e1,e2,e3 i.e. 1 and 2, i've just named them run
            run_path = os.path.join(bl_path, run)
            cued_file = os.path.join(run_path, "target_cued.csv")
            uncued_file = os.path.join(run_path, "target_uncued.csv")

            if os.path.exists(cued_file):
                cued_data = pd.read_csv(cued_file)  #if loop to check if file exits or not. if it doesn't then it will not go inside the loop.
                cued_data["Participant"] = part  
                cued_data["Emotion"] = emo
                cued_data["Validity"] = "Cued"
                cued_dlist.append(cued_data)

            if os.path.exists(uncued_file): #similarly for the uncued file
                uncued_data = pd.read_csv(uncued_file)
                uncued_data["Participant"] = part
                uncued_data["Emotion"] = emo
                uncued_data["Validity"] = "Uncued"
                uncued_dlist.append(uncued_data)
                
        # this line is for merge 1 and 2 for the current block open for a particular partciipant.

        if cued_dlist: #for cued
            merged_cued = pd.concat(cued_dlist, ignore_index=True)
            allmerge[bl]["Cued"].append(merged_cued)

        if uncued_dlist: #similarly for uncued
            merged_uncued = pd.concat(uncued_dlist, ignore_index=True)
            allmerge[bl]["Uncued"].append(merged_uncued)

print("\nData merging complete!") # this is for debug purpose but i want to keep it.
#######CORREECT TILL HERE WORKS!!!!!!!!!!!!!!!!!!!

#now looping to save final merged data
for bl, emotion in emoblo.items():
    if allmerge[bl]["Cued"]:
        final_cued = pd.concat(allmerge[bl]["Cued"], ignore_index=True)
        final_cued_path = os.path.join(out_dir, f"{bl}_final_merged_cued.csv")
        final_cued.to_csv(final_cued_path, index=False)
        print(f"Saved: {final_cued_path}")

    if allmerge[bl]["Uncued"]:
        final_uncued = pd.concat(allmerge[bl]["Uncued"], ignore_index=True)
        final_uncued_path = os.path.join(out_dir, f"{bl}_final_merged_uncued.csv")
        final_uncued.to_csv(final_uncued_path, index=False)
        print(f"Saved: {final_uncued_path}")

print("\nFinal merged data saved. Yes, it works finally!")

#################### pt2:extracting col/slicing csv ##################
# fnction to extract relevant columns
def slicer(file_path):
    df = pd.read_csv(file_path)
    selected_col = ["response_time", "location", "cue_location"]

    if "t87" not in df.columns: # check if 't87' is in the columns exists
        raise ValueError("Can't find column named 't87'. Check CSV file.")
    
    pupil_dcol = df.columns[df.columns.get_loc("t87"):]  # get cols from 't87' onwards now
    f_col = selected_col + list(pupil_dcol) # combine selected cols with pupil diameter cols now
    df_filt = df[f_col] # filter the dataframe to keep only selected cols
    return df_filt

#  using forloop through each block e1,e2,e3 and process all collected cued,uncued data
for bl in emoblo.keys():
    for validity in ["Cued", "Uncued"]:
        file_name = os.path.join(out_dir, f"{bl}_final_merged_{validity}.csv")
        
        try:
            extracted_df = slicer(file_name)
            extracted_output_file = os.path.join(out_dir, f"{bl}-clean-{validity}.csv")
            extracted_df.to_csv(extracted_output_file, index=False)
            print(f"Extracted + Saved the file: {extracted_output_file}")
        
        except Exception as e:
            print(f"Error processing {file_name}: {e}")

####################merge+slice code ends #######################