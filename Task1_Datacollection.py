#Task 1: Data collection

import requests
import time
import json
import os
from datetime import datetime
BASE_URL = "https://hacker-news.firebaseio.com/v0"
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# Category keyword mapping (case-insensitive)
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

MAX_PER_CATEGORY = 25
TOTAL_LIMIT = 500


# -------------------------------
# Helper Functions
# -------------------------------

def fetch_top_story_ids():
    """Fetch top story IDs from HackerNews"""
    url = f"{BASE_URL}/topstories.json"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()[:TOTAL_LIMIT]
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return []


def fetch_story(story_id):
    """Fetch individual story details"""
    url = f"{BASE_URL}/item/{story_id}.json"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching story {story_id}: {e}")
        return None

def categorize(title):
    """Assign category based on keywords"""
    if not title:
        return None

    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category

    return None


def main():
    story_ids = fetch_top_story_ids()

    # Storage
    collected_data = []
    category_counts = {cat: 0 for cat in CATEGORIES}

    for story_id in story_ids:
        story = fetch_story(story_id)

        if not story or "title" not in story:
            continue

        category = categorize(story.get("title"))

        # Skip if no category match
        if not category:
            continue

        # Skip if category already full
        if category_counts[category] >= MAX_PER_CATEGORY:
            continue

        # Extract required fields
        record = {
            "post_id": story.get("id"),
            "title": story.get("title"),
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        collected_data.append(record)
        category_counts[category] += 1

        # Stop if all categories filled
        if all(count >= MAX_PER_CATEGORY for count in category_counts.values()):
            break

    # Sleep once per category (requirement)
    for _ in CATEGORIES:
        time.sleep(2)


    # Create data folder if not exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # File name with date
    file_name = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    try:
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(collected_data, f, indent=4)

        print(f"Collected {len(collected_data)} stories. Saved to {file_name}")

    except Exception as e:
        print(f"Error saving file: {e}")


if __name__ == "__main__":
    main()