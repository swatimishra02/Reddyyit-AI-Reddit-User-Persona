# Reddyyit : Find out your persona on Reddit

Reddit is a website where redditors can be a part of their favourite sub reddits, share their ideas and opinions on the topics they're a nerd about, while having a quirky anonimity on the website. This project is a fun way to analyse the reddit profiles of users using LLMs, allowing AI to dissect the anonymous presence of users and gives insight on what actually makes a redditor, a redditor.

This project achieves this by fetchning and analysing the users top 100 posts and comments.

## 🚀 Features

- 🔍 Fetches posts & comments from any Reddit user
- 🤖 Generates detailed personas using Mistral-7B via OpenRouter
- 🧾 Saves output as a **text file**
- 📄 Offers **PDF download** of the persona
- 🎨 Clean and organized web interface with personalized sections
- 💾 Local data caching for faster re-runs

## Usage

### Installation

1. Create venv

```bash
conda create --name myenv python=3.10
```

2. Install Requirements

```bash
pip install -r requirements.txt
```

### Setup

Create a .env file in your root directory with the following:

```bash
REDDIT_CLIENT_ID=your_reddit_app_id
REDDIT_CLIENT_SECRET=your_reddit_app_secret
REDDIT_USER_AGENT=your_unique_user_agent
OPENROUTER_API_KEY=your_openrouter_api_key
```

You can obtain these from:
- [Reddit API Console](https://www.reddit.com/prefs/apps)
- [OpenRouter](https://openrouter.ai/)


### Running


``` bash
python app.py
```
This will start the Flask server and you can access the app at `http://localhost:5000.

### Demo

[![Watch the demo](https://raw.githubusercontent.com/swatimishra02/Reddyyit/main/assets/thumbnail.png)](https://youtu.be/7z4DfkhEXsM)

### Example 

[📄 View Persona for u/kojied (PDF)](https://github.com/your-username/your-repo-name/raw/main/path/to/Persona%20for%20u_kojied.pdf)


 Acknowledgements
-------------------

- [OpenRouter](https://openrouter.ai/) – API gateway for accessing various open-source LLMs
- [Reddit API (PRAW)](https://praw.readthedocs.io/en/stable/) – Python Reddit API Wrapper for interacting with Reddit data
- [Flask](https://flask.palletsprojects.com/) – Lightweight Python web framework
- [Mistral-7B (via OpenRouter)](https://openrouter.ai/models/mistralai/mistral-7b-instruct) – Open-weight LLM used for persona generation



