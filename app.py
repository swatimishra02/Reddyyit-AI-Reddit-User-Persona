

from flask import Flask, render_template, request
from llm.persona_generator import generate_persona_with_openrouter
from reddit.fetch_data import fetch_user_posts_and_comments
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"].strip()
        output_dir = "data/outputs"
        os.makedirs(output_dir, exist_ok=True)

        content_path = f"{output_dir}/{username}_content.txt"

        #fetch user posts and comments
        if not os.path.exists(content_path):
            comments, posts = fetch_user_posts_and_comments(username)

            if not comments and not posts:
                return f"Could not fetch Reddit data for user '{username}'. They might not exist or have no public activity."

            # Save content to .txt
            with open(content_path, "w", encoding="utf-8") as f:
                for item in posts + comments:
                    f.write(f"[{item['type'].upper()}] r/{item['subreddit']}\n{item['content']}\n\n")

       
        with open(content_path, "r", encoding="utf-8") as f:
            reddit_text = f.read()

        persona = generate_persona_with_openrouter(reddit_text, username, return_text=True)

       
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, f"user_persona_{username}.txt")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(persona)

        return render_template("result.html", username=username, persona=persona)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


