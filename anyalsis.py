import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Define the folder where the CSV files are"  # Change this to your actual folder path

folder_path = "C:/Users/anya/Downloads/atp_anya/anyacode/"
# Define the files and their corresponding experiment labels
files_info = {
    "E1_cleaned_cued.csv": "E1 Cued",
    "E1_cleaned_uncued.csv": "E1 Uncued",
    "E2_cleaned_cued.csv": "E2 Cued",
    "E2_cleaned_uncued.csv": "E2 Uncued",
    "E3_cleaned_cued.csv": "E3 Cued",
    "E3_cleaned_uncued.csv": "E3 Uncued"
}

# Initialize an empty list to store data
dataframes = []

# Load each file, add an "Experiment" column, and append to the list
for filename, experiment in files_info.items():
    file_path = os.path.join(folder_path, filename)
    df = pd.read_csv(file_path)
    df["Experiment"] = experiment  # Add experiment label
    dataframes.append(df)
#print(df.columns)  # Check the actual column names
#print(df.columns.tolist())  # Print column names clearly

# Combine all data into a single DataFrame
df = pd.concat(dataframes, ignore_index=True)

# Rename incorrect column names
df.rename(columns={
    "response_time": "ReactionTime", 
    "location": "Eccentricity"
}, inplace=True)

# Check if renaming worked
print(df.columns)  

# Step 2: Group Trials
grouped_df = df.groupby(["Experiment", "Emotion", "Validity", "Eccentricity"])["ReactionTime"].mean().reset_index()

#print(df["Experiment"].unique())  # Check unique values in 'Experiment'
#print(df["Emotion"].unique())     # Check unique values in 'Emotion'
#print(df["Validity"].unique())    # Check unique values in 'Validity'
#print(df["Eccentricity"].unique()) # Check unique values in 'Eccentricity'

# Step 3: Plot Reaction Time for all experiments
sns.set(style="whitegrid")

fig, axes = plt.subplots(3, 2, figsize=(14, 12), sharey=True)

# Get unique experiments
experiments = grouped_df["Experiment"].unique()

# Iterate over each experiment and create subplots
for i, experiment in enumerate(["E1", "E2", "E3"]):
    df_cued = grouped_df[grouped_df["Experiment"] == f"{experiment} Cued"]
    df_uncued = grouped_df[grouped_df["Experiment"] == f"{experiment} Uncued"]


    # Cued Trials Plot
    sns.barplot(ax=axes[i, 0], data=df_cued, x="Emotion", y="ReactionTime", hue="Eccentricity")
    axes[i, 0].set_title(f"Reaction Time - {experiment} Cued Trials")
    axes[i, 0].set_ylabel("Avg Reaction Time (ms)")
    axes[i, 0].set_xlabel("Emotion")

    # Uncued Trials Plot
    sns.barplot(ax=axes[i, 1], data=df_uncued, x="Emotion", y="ReactionTime", hue="Eccentricity")
    axes[i, 1].set_title(f"Reaction Time - {experiment} Uncued Trials")
    axes[i, 1].set_ylabel("")
    axes[i, 1].set_xlabel("Emotion")

# Check data count for each condition
for experiment in ["E1", "E2", "E3"]:
    for cue in ["Cued", "Uncued"]:
        df_subset = grouped_df[grouped_df["Experiment"] == f"{experiment} {cue}"]
        print(f"{experiment} {cue}: {len(df_subset)} rows")
print(grouped_df[["Experiment", "Emotion", "Validity", "ReactionTime"]].isna().sum())
print(grouped_df["Validity"].unique())

# for key, grp in grouped_df.groupby(["Eccentricity"]):
#     plt.plot(grp["Eccentricity"], grp["ReactionTime"], marker="o", linestyle="-", label=f"{key}°")  # Ensure label is set


# plt.legend(title="Eccentricity (°)", loc="upper right")
# plt.tight_layout()
# plt.show()


# Create figure with 2 subplots
fig, axes = plt.subplots(1, 2, figsize=(15, 6), sharey=True)

# Plot for Cued Trials
sns.lineplot(data=df[df['Validity'] == 'Cued'], 
             x='Eccentricity', y='ReactionTime', 
             hue='Emotion', marker='o', ax=axes[0])
axes[0].set_title("Reaction Time for Cued Trials")
axes[0].set_xlabel("Eccentricity (degrees)")
axes[0].set_ylabel("Average Reaction Time (s)")

# Plot for Uncued Trials
sns.lineplot(data=df[df['Validity'] == 'Uncued'], 
             x='Eccentricity', y='ReactionTime', 
             hue='Emotion', marker='o', ax=axes[1])
axes[1].set_title("Reaction Time for Uncued Trials")
axes[1].set_xlabel("Eccentricity (degrees)")
axes[1].legend(title="Emotion")

# Adjust layout
plt.tight_layout()
plt.show()