#Task2-Clean Data
import pandas as pd
import os
import glob

# Step 1: Load JSON File

# Find latest JSON file in data/ folder
json_files = glob.glob("data/trends_*.json")

if not json_files:
    print("No JSON file found in data/ folder. Run Task 1 first.")
    exit()

# Get latest file (based on name sorting)
latest_file = sorted(json_files)[-1]
# Load JSON into DataFrame
df = pd.read_json(latest_file)

print(f"Loaded {len(df)} stories from {latest_file}")

# Step 2: Clean Data

# 1. Remove duplicates based on post_id
before = len(df)
df = df.drop_duplicates(subset=["post_id"])
print(f"After removing duplicates: {len(df)}")

# 2. Remove missing values in key columns
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")
# 3. Fix data types (ensure integers)
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].fillna(0).astype(int)

# 4. Remove low-quality stories (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# 5. Strip whitespace from title
df["title"] = df["title"].str.strip()

# Step 3: Save as CSV

# Ensure data folder exists
if not os.path.exists("data"):
    os.makedirs("data")

output_file = "data/trends_clean.csv"

df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")

print("\nStories per category:")
print(df["category"].value_counts())