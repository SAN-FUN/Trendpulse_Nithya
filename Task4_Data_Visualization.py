#Task4-Data_Visualization
import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Setup

file_path = "data/trends_analysed.csv"

if not os.path.exists(file_path):
    print("Analysed CSV not found. Run Task 3 first.")
    exit()

# Load data
df = pd.read_csv(file_path)
# Create outputs folder
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# Helper: Shorten titles

def shorten_title(title, length=50):
    """Shorten long titles for better display"""
    return title[:length] + "..." if len(title) > length else title

# Chart 1: Top 10 Stories by Score

top10 = df.sort_values(by="score", ascending=False).head(10)

titles = [shorten_title(t) for t in top10["title"]]

plt.figure()
plt.barh(titles, top10["score"])
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()  # Highest score on top

plt.savefig("outputs/chart1_top_stories.png")
plt.close()

# Chart 2: Stories per Category

category_counts = df["category"].value_counts()

plt.figure()
plt.bar(category_counts.index, category_counts.values)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.savefig("outputs/chart2_categories.png")
plt.close()

# Chart 3: Score vs Comments

popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure()
plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()

plt.savefig("outputs/chart3_scatter.png")
plt.close()

#ViewDashboard
fig, axs = plt.subplots(1, 3, figsize=(18, 5))

# Chart 1 in dashboard
axs[0].barh(titles, top10["score"])
axs[0].set_title("Top 10 Stories")
axs[0].invert_yaxis()

# Chart 2 in dashboard
axs[1].bar(category_counts.index, category_counts.values)
axs[1].set_title("Stories per Category")

# Chart 3 in dashboard
axs[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axs[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axs[2].set_title("Score vs Comments")
axs[2].legend()

# Overall title
plt.suptitle("TrendPulse Dashboard")

plt.savefig("outputs/dashboard.png")
plt.close()

print("Charts saved in outputs/ folder")
