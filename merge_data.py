import os
import pandas as pd

# Define the base directory where all participant folders are stored
base_dir = "C:/Users/Anya/Downloads/atp_anya/D1-16"  # Change this to your actual dataset path

# Define blocks corresponding to emotions
emotion_blocks = {"E1": "Happy", "E2": "Angry", "E3": "Neutral"}

# Create a dictionary to store merged data for all participants
all_merged_data = {block: {"Cued": [], "Uncued": []} for block in emotion_blocks.keys()}

# Get all participant folders inside the base directory
participants = [p for p in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, p))]

# Loop through each participant
for participant in participants:
    participant_path = os.path.join(base_dir, participant)
    print(f"Processing participant: {participant}")

    # Loop through each block (E1, E2, E3)
    for block, emotion in emotion_blocks.items():
        block_path = os.path.join(participant_path, block)

        # Initialize lists to store Run 1 and Run 2 data
        cued_data_list = []
        uncued_data_list = []

        # Iterate over Run 1 and Run 2
        for run in ["1", "2"]:
            run_path = os.path.join(block_path, run)

            # Define file paths
            cued_file = os.path.join(run_path, "target_cued.csv")
            uncued_file = os.path.join(run_path, "target_uncued.csv")

            # Load cued data if file exists
            if os.path.exists(cued_file):
                cued_data = pd.read_csv(cued_file)
                cued_data["Participant"] = participant  # Add participant ID
                cued_data["Emotion"] = emotion  # Add emotion label
                cued_data["Validity"] = "Cued"  # Mark as valid trials
                cued_data_list.append(cued_data)

            # Load uncued data if file exists
            if os.path.exists(uncued_file):
                uncued_data = pd.read_csv(uncued_file)
                uncued_data["Participant"] = participant
                uncued_data["Emotion"] = emotion
                uncued_data["Validity"] = "Uncued"  # Mark as invalid trials
                uncued_data_list.append(uncued_data)

        # Merge Run 1 and Run 2 for the current block (for this participant)
        if cued_data_list:
            merged_cued = pd.concat(cued_data_list, ignore_index=True)
            all_merged_data[block]["Cued"].append(merged_cued)

        if uncued_data_list:
            merged_uncued = pd.concat(uncued_data_list, ignore_index=True)
            all_merged_data[block]["Uncued"].append(merged_uncued)

print("\n Data merging complete for all participants!")

# Save final merged datasets
for block, emotion in emotion_blocks.items():
    # Merge cued data across all participants
    if all_merged_data[block]["Cued"]:
        final_cued = pd.concat(all_merged_data[block]["Cued"], ignore_index=True)
        final_cued.to_csv(f"{block}_final_merged_cued.csv", index=False)

    # Merge uncued data across all participants
    if all_merged_data[block]["Uncued"]:
        final_uncued = pd.concat(all_merged_data[block]["Uncued"], ignore_index=True)
        final_uncued.to_csv(f"{block}_final_merged_uncued.csv", index=False)

print("\n Final merged datasets saved successfully!")

# Function to extract relevant columns
def extract_columns(file_path):
    # Load the dataset
    df = pd.read_csv(file_path)
    
    # Display column names (for debugging)
    print(f"\nColumns in {file_path}:\n", df.columns.tolist())
    
    # Use correct column names based on your data
    selected_columns = ["response_time", "location", "cue_location"]  # Fix column names
    pupil_data_columns = df.columns[87:]  # Extract pupil diameter (from column 87 onwards)

    # Combine all selected columns
    final_columns = selected_columns + list(pupil_data_columns)

    # Filter dataset
    df_filtered = df[final_columns]

    return df_filtered

# Loop through each block (E1, E2, E3) and process cued & uncued data
for block in emotion_blocks.keys():
    for validity in ["cued", "uncued"]:
        file_name = f"{block}_final_merged_{validity}.csv"
        
        try:
            # Extract relevant data
            extracted_df = extract_columns(file_name)
            
            # Save cleaned dataset
            extracted_df.to_csv(f"{block}_cleaned_{validity}.csv", index=False)
            print(f"Extracted & saved: {block}_cleaned_{validity}.csv")
        
        except Exception as e:
            print(f"Error processing {file_name}: {e}")