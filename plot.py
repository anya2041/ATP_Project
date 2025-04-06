import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as pl
import seaborn as sns


################# now use the merge+slice as clean data and process it to get the plots #############

f_path = "C:/Users/Anya/Downloads/D1-16/" #path ofr cleaned csv files generated 

# Define the files and their corresponding experiment labels
files_info = {
    "E1-clean-cued.csv": "E1 Cued",
    "E1-clean-uncued.csv": "E1 Uncued",
    "E2-clean-cued.csv": "E2 Cued",
    "E2-clean-uncued.csv": "E2 Uncued",
    "E3-clean-cued.csv": "E3 Cued",
    "E3-clean-uncued.csv": "E3 Uncued"
}

data_frame = []  #a list to store dataframes
# for looop through each file and read it into a dataframe
for filename, experiment in files_info.items():
    file_path = os.path.join(f_path, filename)
    df_part = pd.read_csv(file_path)
    df_part["Experiment"] = experiment  #add experiment column to the dataframe
    data_frame.append(df_part)

#this is for combining all the dataframes into one
# Concatenate command to merge into single/one frame 
df = pd.concat(data_frame, ignore_index=True)

# renaming columns for being easily understandable
# "response_time" -> "ReactionTime" and "location" -> "Eccentricity"
df.rename(columns={"response_time": "Reaction_Time", "location": "Eccentricity"}, inplace=True)

# here making a funct to process pupil diameter data and then create its csv
def propd(df):
    pupil_columns = [col for col in df.columns if col.startswith("t")] # this is important as 't' starting cols should be identified to extract
    #the dataset contains multiple time points i.e. pupil diameter at different times flattening converts the big and wide format into a long format where each time point becomes a separate row. 
    plotd= [] #    # here to do above thing i create an empty list to store the flattened data
    #loop through each row of the dframe
    for _, row in df.iterrows():
        for time_point, value in enumerate(row[pupil_columns]): #for each time pointi.e.column starting with t,  i extract the pupil diameter value
            plotd.append({
                "Participant": row["Participant"], #add col named particpant
                "Emotion": row["Emotion"], # and so on... cols
                "Validity": row["Validity"],
                "Experiment": row["Experiment"],
                "Eccentricity": row["Eccentricity"],
                "Time Point": time_point * 8,  #  8 ms intervals applied so convert into ms
                "Pupil Diameter": value
            })
    
    # Create a DataFrame from the flattened data
    plot_df = pd.DataFrame(plotd) #here pd.dataframe as return bcoz it gives me the averaged pupil dia as data
    
    return plot_df

# callinf the func to process pupil dia
process_pupil_df = propd(df)

# here save the processed file to csv format
process_pupil_df.to_csv("processed_pupil_diameter_data.csv", index=False)
print("the processed pupil diameter data is saved to 'processed-pupil-diadata.csv'.") ####################reminder i need to submit this file as csv

# here group the RT data by mean grp wise
group_rt = (
    df.groupby(["Experiment", "Emotion", "Validity", "Eccentricity"])["Reaction_Time"]
    .mean()
    .reset_index() # this is imp to reset the index after grouping i.e i get clean dframe
)
print("\nGrouped Reaction Time Data:")
print(group_rt.head())

#group pupil diameter data for plot using mean , parameters would be time point, emo, validity and pupil dia --> earlier i did for mean RT now, here i do it for pupil dia mean
agg_plot_df = process_pupil_df.groupby(["Time Point", "Emotion", "Validity"])["Pupil Diameter"].mean().reset_index()

#this line is for separateifg the uncued and cued trials for plot
cued_df = agg_plot_df[agg_plot_df["Validity"] == "Cued"]
uncued_df = agg_plot_df[agg_plot_df["Validity"] == "Uncued"]


########plotting part anya################################################### 
neon_colors = [
    "#FF007F",  # neon Pink
    "#00FFFF",  # electricblue
    "#39FF14",  # neon green
    "#FFA500",  # neon orange
    "#FFD700"   # gold
]
sns.set(style="ticks") # this is a seaborn plot style
#plot 1 : avg  pupil dia over time############
fig, axes = pl.subplots(1, 2, figsize=(20, 6), sharey=True)  # Create 2 subplots side by side (Cued/Uncued)
#cued one
sns.lineplot(
    data=cued_df,
    x="Time Point",
    y="Pupil Diameter",
    hue="Emotion",
    markers=True,
    palette=neon_colors, 
    ax=axes[0]
)
axes[0].set_title('Average Pupil Diameter Over Time (Cued Trials)')
axes[0].set_xlabel('Time Point (ms)')
axes[0].set_ylabel('Average Pupil Diameter')
axes[0].legend(title='Emotion')
axes[0].grid()

#uncued one
sns.lineplot(
    data=uncued_df,
    x="Time Point",
    y="Pupil Diameter",
    hue="Emotion",
    markers=True,
    palette=neon_colors, 
    ax=axes[1]
)
axes[1].set_title('Average Pupil Diameter Over Time (Uncued Trials)')
axes[1].set_xlabel('Time Point (ms)')
axes[1].legend(title='Emotion')
axes[1].grid()

pl.tight_layout()
pl.savefig('pd-finalplot.png')  
pl.show()

#plot2 : RT #####################
fig, axes = pl.subplots(1, 2, figsize=(15, 6), sharey=True)

#cued one
sns.lineplot(
    data=group_rt[group_rt["Validity"] == "Cued"],
    x="Eccentricity",
    y="Reaction_Time",
    hue="Emotion",
    style="Emotion", 
    markers=True,
    palette=neon_colors,  
    ax=axes[0]
)
axes[0].set_title("Reaction Time for Cued Trials")
axes[0].set_xlabel("Eccentricity (degrees)")
axes[0].set_ylabel("Average Reaction Time (ms)")  
axes[0].legend(title="Emotion", loc="upper left")
axes[0].grid()

#uncued one
sns.lineplot(
    data=group_rt[group_rt["Validity"] == "Uncued"],
    x="Eccentricity",
    y="Reaction_Time",
    hue="Emotion",
    style="Emotion",  
    markers=True,
    palette=neon_colors,
    ax=axes[1]
)
axes[1].set_title("Reaction Time for Uncued Trials")
axes[1].set_xlabel("Eccentricity (degrees)")
axes[1].legend(title="Emotion", loc="upper left")
axes[1].grid()

pl.tight_layout()
pl.savefig('reactiontime-finalplot_.png')  
pl.show()

######plot no3. supporting plot median RT vs plot2/avg/mean RT########################
# group rt median wise
group_rt_median = (
    df.groupby(["Experiment", "Emotion", "Validity", "Eccentricity"])["Reaction_Time"]
    .median()  
    .reset_index()
)
# grp rt mean wise
group_rt_mean = (
    df.groupby(["Experiment", "Emotion", "Validity", "Eccentricity"])["Reaction_Time"]
    .mean()  
    .reset_index()
)

#code plot here#########################
fig, axes = pl.subplots(1, 2, figsize=(15, 6), sharey=True)

#cued one median here
sns.lineplot(
    data=group_rt_median[group_rt_median["Validity"] == "Cued"],
    x="Eccentricity",
    y="Reaction_Time",
    hue="Emotion",
    marker="o",
    palette=neon_colors, 
    ax=axes[0]
)
axes[0].set_title("Median Reaction Time for Cued")
axes[0].set_xlabel("Eccentricity degrees")
axes[0].set_ylabel("Median Reaction Time in ms")  
axes[0].legend(title="Emotion")
axes[0].grid()

#uncued one median
sns.lineplot(
    data=group_rt_median[group_rt_median["Validity"] == "Uncued"],
    x="Eccentricity",
    y="Reaction_Time",
    hue="Emotion",
    marker="o",
    palette=neon_colors,  
    ax=axes[1]
)
axes[1].set_title("Median Reaction Time for Uncued")
axes[1].set_xlabel("Eccentricity degrees")
axes[1].legend(title="Emotion")
axes[1].grid()

pl.tight_layout()
pl.savefig('rt_medianplot.png')  
pl.show()

#contd plot will come same as plot 2 but im repeating it again
fig, axes = pl.subplots(1, 2, figsize=(15, 6), sharey=True)

#cued one mean
sns.lineplot(
    data=group_rt_mean[group_rt_mean["Validity"] == "Cued"],
    x="Eccentricity",
    y="Reaction_Time",
    hue="Emotion",
    marker="o",
    palette=neon_colors, 
    ax=axes[0]
)
axes[0].set_title("Average Reaction Time for Cued Trials")
axes[0].set_xlabel("Eccentricity (degrees)")
axes[0].set_ylabel("Average Reaction Time (ms)")  # Correct units from seconds to milliseconds
axes[0].legend(title="Emotion")
axes[0].grid()

#uncued one mean
sns.lineplot(
    data=group_rt_mean[group_rt_mean["Validity"] == "Uncued"],
    x="Eccentricity",
    y="Reaction_Time",
    hue="Emotion",
    marker="o",
    palette=neon_colors, 
    ax=axes[1]
)
axes[1].set_title("Average Reaction Time for Uncued Trials")
axes[1].set_xlabel("Eccentricity (degrees)")
axes[1].legend(title="Emotion")
axes[1].grid()

pl.tight_layout()
pl.savefig('rt_averageplot.png')
pl.show()
