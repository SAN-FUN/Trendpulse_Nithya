#Task3-Data Analysis
import pandas as pd
import numpy as np
import os

# Step 1: Load and Explore

file_path = "data/trends_clean.csv"

if not os.path.exists(file_path):
    print("Clean CSV not found. Run Task 2 first.")
    exit()

# Load CSV
df = pd.read_csv(file_path)
# Print shape
print(f"Loaded data: {df.shape}")

# Print first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Average values
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {avg_score:.2f}")
print(f"Average comments: {avg_comments:.2f}")

# Step 2: NumPy Analysis

scores = df["score"].to_numpy()
comments = df["num_comments"].to_numpy()

print("\n--- NumPy Stats ---")

# Mean, Median, Std
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")

# Max & Min
print(f"Max score    : {np.max(scores)}")
print(f"Min score    : {np.min(scores)}")

# Category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Most commented story
max_comments_idx = np.argmax(comments)
top_story = df.iloc[max_comments_idx]
print(f"\nMost commented story: \"{top_story['title']}\" — {top_story['num_comments']} comments")

# Step 3: Add New Columns

# Engagement = comments per score
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Popular if score > average score
df["is_popular"] = df["score"] > avg_score

# Step 4: Save Result

output_file = "data/trends_analysed.csv"

df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")