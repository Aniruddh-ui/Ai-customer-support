def update_language(language):
    import json
    try:
        with open("user_profile.json", "r") as f:
            profile = json.load(f)
    except FileNotFoundError:
        profile = {"user_id": "user_001"}

    profile["preferred_language"] = language

    with open("user_profile.json", "w") as f:
        json.dump(profile, f, indent=2)
import json
import os
from collections import Counter

PROFILE_PATH = "user_profile.json"


def load_profile():
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r") as file:
            return json.load(file)
    else:
        return {
            "user_id": "user_001",
            "preferred_language": "English",
            "previous_queries": [],
            "sentiment_history": [],
            "common_issues": []
        }


def update_profile(user_query, sentiment, issue_category):
    profile = load_profile()

    # Update query log
    profile["previous_queries"].append(user_query)

    # Update sentiment log
    profile["sentiment_history"].append(sentiment)

    # Update issue categories
    profile["common_issues"].append(issue_category)

    # Optionally compute top 3 common issue types
    counter = Counter(profile["common_issues"])
    profile["top_issues"] = [issue for issue, _ in counter.most_common(3)]

    # Save back to file
    with open(PROFILE_PATH, "w") as file:
        json.dump(profile, file, indent=2)

    return profile


def get_profile():
    return load_profile()
