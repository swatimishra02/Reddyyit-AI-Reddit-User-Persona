import praw
import os
import re
import json
from dotenv import load_dotenv

# -------------------------------
# Load Reddit API credentials
# -------------------------------
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# -------------------------------
# Helpers
# -------------------------------

def extract_username(profile_url):
    """Extracts Reddit username from profile URL."""
    match = re.search(r"reddit\.com/user/([^/]+)/?", profile_url)
    return match.group(1) if match else None

def truncate_text(text, word_limit=500):
    """Trims text to a maximum number of words."""
    words = text.split()
    return ' '.join(words[:word_limit])

def fetch_user_posts_and_comments(username, limit=100):
    """Fetch posts and comments for a Reddit user."""
    redditor = reddit.redditor(username)
    comments = []
    posts = []

    try:
        # Fetch latest comments
        for comment in redditor.comments.new(limit=limit):
            comments.append({
                "subreddit": comment.subreddit.display_name,
                "content": truncate_text(comment.body),
                "type": "comment",
                "permalink": f"https://reddit.com{comment.permalink}"
            })

        # Fetch latest submissions
        for submission in redditor.submissions.new(limit=limit):
            content = submission.title or ""
            if submission.selftext:
                content += "\n" + submission.selftext
            posts.append({
                "subreddit": submission.subreddit.display_name,
                "content": truncate_text(content),
                "type": "post",
                "permalink": f"https://reddit.com{submission.permalink}"
            })

    except Exception as e:
        print(f"[ERROR] Failed to fetch data for u/{username}: {e}")

    return comments, posts




def fetch_and_save_user_data(username, output_dir="data/outputs", limit=100):
    comments, posts = fetch_user_posts_and_comments(username, limit=limit)

    if not comments and not posts:
        raise Exception("No Reddit data found or user is invalid.")

    os.makedirs(output_dir, exist_ok=True)

    with open(f"{output_dir}/{username}_comments.json", "w", encoding="utf-8") as f:
        json.dump(comments, f, indent=2, ensure_ascii=False)

    with open(f"{output_dir}/{username}_posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    with open(f"{output_dir}/{username}_content.txt", "w", encoding="utf-8") as f:
        for item in posts + comments:
            f.write(f"[{item['type'].upper()}] r/{item['subreddit']}\n{item['content']}\n\n")

    return f"{output_dir}/{username}_content.txt"


# -------------------------------
# Main Script
# -------------------------------

if __name__ == "__main__":
    profile_url = input("🔗 Enter the Reddit profile URL: ").strip()
    username = extract_username(profile_url)

    if not username:
        print("Invalid Reddit profile URL.")
        exit()

    print(f" Fetching posts and comments for u/{username} ...")
    comments, posts = fetch_user_posts_and_comments(username)

    print(f" Retrieved {len(comments)} comments and {len(posts)} posts.")

    # Save directory
    output_dir = f"data/outputs"
    os.makedirs(output_dir, exist_ok=True)

    # Save to JSON
    with open(f"{output_dir}/{username}_comments.json", "w", encoding="utf-8") as f:
        json.dump(comments, f, indent=2, ensure_ascii=False)

    with open(f"{output_dir}/{username}_posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    # Save to text (for LLM prompt use)
    with open(f"{output_dir}/{username}_content.txt", "w", encoding="utf-8") as f:
        for item in posts + comments:
            f.write(f"[{item['type'].upper()}] r/{item['subreddit']}\n{item['content']}\n\n")

    



    print(f"\n Saved outputs to: {output_dir}/")
    print(f"   - {username}_comments.json")
    print(f"   - {username}_posts.json")
    print(f"   - {username}_content.txt\n")



