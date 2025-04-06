import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as pl
import seaborn as sns

########################### part1 : merging data ###################
bfold= "C:/Users/Anya/Projects/ATP_Project/D1-16" 
#this is for my base folder Or the directory name where i extracted the zip file
# in my experiment the alloted folder was D1-16
#also as there were 10 particiants in D1-16 but one particilpant's data of E3 folder was missing i.e. ASR was not present so i have only 9 folders now in D1-16 so i had done analysis for them. I mailed the TA about this too. 

emoblo= {"E1": "Happy", "E2": "Angry", "E3": "Neutral"}
#emoblo is a dict where i have kept the block name E1,E2,E3 as key and the emotion as value (Happy, Angry, Neutral) as given in the asignment guidelines.

allmerge= {block: {"Cued": [], "Uncued": []} for block in emoblo.keys()}
#allmerge is for storing merged data of 9 participants blockwise and for condition wise too. it's a dictionary as well.

# Get all participant folders inside the base directory
ppt = [p for p in os.listdir(bfold) if os.path.isdir(os.path.join(bfold, p))] #this is participants (ppt) to get their folders inside the big folder.


#now i've put loop to go ver particpants then blocks and then runs to fetch all the csv files data.
for part in ppt:
    part_path = os.path.join(bfold, part)  # Path of participant's folder
    #print(f"Processing participant: {participant}") # this is put for debug purpose i dont want to delete it.

    
    for bl, emo in emoblo.items(): #for loop over blocks and their emotions
        bl_path = os.path.join(part_path, bl)  # for the path of blockfolder

        # here i've just given empty list for cued/valid and uncued/invalid traisls.
        cued_dlist = []
        uncued_dlist = []

        # for loop to go over the folder indide e1,e2,e3 i.e. 1 and 2, i've just named them run
        for run in ["1", "2"]:
            run_path = os.path.join(bl, run)

            
            cued_file = os.path.join(run_path, "target_cued.csv") #here i have given the path of cued and uncued files as per the name setting or format follwed int the asignemnt guidelines
            uncued_file = os.path.join(run_path, "target_uncued.csv")

        
            if os.path.exists(cued_file): #if loop to check if file exits or not. if it doesn't then it will not go inside the loop.
                cued_data = pd.read_csv(cued_file)
                cued_data["Participant"] = ppt  # Add participant 
                cued_data["Emotion"] = emo  # Add emo label
                cued_data["Validity"] = "Cued"  # tag asvalid trials
                cued_dlist.append(cued_data)

            
            if os.path.exists(uncued_file): #similarly for the uncued file
                uncued_data = pd.read_csv(uncued_file)
                uncued_data["Participant"] = part
                uncued_data["Emotion"] = emo
                uncued_data["Validity"] = "Uncued"  # tag as invalid trials
                uncued_dlist.append(uncued_data)

        # this line is for merge 1 and 2 for the current block open for a particular partciipant.
        if cued_dlist:
            merged_cued = pd.concat(cued_dlist, ignore_index=True)
            allmerge[bl]["Cued"].append(merged_cued)

        if uncued_dlist: # same for uncued too.
            merged_uncued = pd.concat(uncued_dlist, ignore_index=True)
            allmerge[bl]["Uncued"].append(merged_uncued)

##print("\n data merging! done!!!!!") # this is for debug purpose but i want to keep it.
#######CORREECT TILL HERE WORKS!!!!!!!!!!!!!!!!!!!

# Now loop to save final merged data
for bl, emotion in emoblo.items():
    # Merge cued data for all participants
    if allmerge[bl]["Cued"]:
        final_cued = pd.concat(allmerge[bl]["Cued"], ignore_index=True)
        if not final_cued.empty:
            final_cued.to_csv(f"{bl}_final_merged_cued.csv", index=False)
            print(f"Saved: {bl}_final_merged_cued.csv")
        else:
            print(f"No data to save for {bl} Cued.")

    # Merge uncued data for all participants
    if allmerge[bl]["Uncued"]:
        final_uncued = pd.concat(allmerge[bl]["Uncued"], ignore_index=True)
        if not final_uncued.empty:
            final_uncued.to_csv(f"{bl}_final_merged_uncued.csv", index=False)
            print(f"Saved: {bl}_final_merged_uncued.csv")
        else:
            print(f"No data to save for {bl} Uncued.")

# List files in the current directory after merging
print("Files in the current directory after merging:")
print(os.listdir('.'))

print("\nFinal merged data saved. Yes, it works finally!")

#################### part 2: now extracting cols/ slicing csv ##################

# fnction to extract relevant columns
def slicer(file_path):
    df = pd.read_csv(file_path)  # read the file path to slice/extract
    selected_col = ["response_time", "location", "cue_location"]

    # check if 't87' is in the columns exists
    if "t87" not in df.columns:
        raise ValueError("Can't find column named 't87'. Check CSV file.")
    
    pupil_dcol = df.columns[df.columns.get_loc("t87"):]  # get columns from 't87' onwards now
    f_col = selected_col + list(pupil_dcol)  # combine seelected columns
    df_filt = df[f_col]  # filter the data keep only selected columns
    return df_filt

# using forloop through each block e1,e2,e3 and process all collected cued,uncued data
for bl in emoblo.keys():
    for validity in ["Cued", "Uncued"]:
        file_name = f"{bl}_final_merged_{validity.lower()}.csv"
        
        try:
            extracted_df = slicer(file_name)
            extracted_df.to_csv(f"{bl}-clean-{validity.lower()}.csv", index=False) #save it to csv
            print(f"Extracted + Saved the file: {bl}-clean-{validity.lower()}.csv")
        
        except Exception as ehhh:
            print(f"Error {file_name}: {ehhh}")

##################### merge + slice code ends #######################