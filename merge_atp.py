import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Base path to your dataset folder
base_path = r'C:\Users\Anya\Downloads\D1-16-anya\D1-16'

# Define participant folder
participant_folder = 'NIS'  # Change this to the appropriate participant code

def load_and_merge_data(emotion):
    # Load data from both subfolders and merge for a specific emotion
    df1 = pd.read_csv(f"{base_path}\\{participant_folder}\\{emotion}\\1\\target_cued.csv")
    df2 = pd.read_csv(f"{base_path}\\{participant_folder}\\{emotion}\\2\\target_cued.csv")
    return pd.concat([df1, df2])

# Load and merge data for each emotion
happy_data = load_and_merge_data('E1')  # Happy
angry_data = load_and_merge_data('E2')  # Angry
neutral_data = load_and_merge_data('E3')  # Neutral

# Assuming pupil diameter data starts from column 87
pupil_columns = happy_data.columns[86:]  # 0-indexed: column 87 is at index 86

# Calculate average pupil diameter for each emotion
average_pupil_happy = happy_data[pupil_columns].mean(axis=0)
average_pupil_angry = angry_data[pupil_columns].mean(axis=0)
average_pupil_neutral = neutral_data[pupil_columns].mean(axis=0)

# Plotting average pupil diameter
plt.figure(figsize=(12, 6))
plt.plot(average_pupil_happy, label='Happy', color='blue')
plt.plot(average_pupil_angry, label='Angry', color='red')
plt.plot(average_pupil_neutral, label='Neutral', color='green')
plt.title('Average Pupil Diameter During Emotion Recognition')
plt.xlabel('Time (ms)')
plt.ylabel('Average Pupil Diameter (mm)')
plt.legend()
plt.show()

# Calculate average reaction times for valid and invalid cues
reaction_times = pd.concat([
    happy_data['Reaction Time'],
    angry_data['Reaction Time'],
    neutral_data['Reaction Time']
], axis=1)

# Adding emotion labels for plotting
reaction_times.columns = ['Happy', 'Angry', 'Neutral']

# Melt the DataFrame for easier plotting
reaction_times_melted = reaction_times.melt(var_name='Emotion', value_name='Reaction Time')

# Plotting reaction times
plt.figure(figsize=(12, 6))
sns.barplot(x='Emotion', y='Reaction Time', data=reaction_times_melted)
plt.title('Reaction Times for Different Emotions')
plt.xlabel('Emotion')
plt.ylabel('Reaction Time (ms)')
plt.show()

# Save averaged pupil diameter data to CSV
average_pupil_data = pd.DataFrame({
    'Happy': average_pupil_happy,
    'Angry': average_pupil_angry,
    'Neutral': average_pupil_neutral
})

average_pupil_data.to_csv('averaged_pupil_data.csv', index=False)