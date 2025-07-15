
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

## using Mistral AI via Openrouter and Reddit API

def call_openrouter_api(prompt, model="mistralai/mistral-7b-instruct", temperature=0.7, max_tokens=1000):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    print(f" Sending prompt to OpenRouter ({model})...")
    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return None

    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Failed to parse response: {e}")
        print("Raw preview:\n", response.text[:800])
        return None

def clean_persona_output(raw_text):
    """Standardize section headers for consistent UI parsing."""
    replacements = {
        "**Name**": "Name:",
        "**Quote**": "Quote:",
        "**Motivations**": "Motivations:",
        "**Preferences**": "Preferences:",
        "**Frustrations**": "Frustrations:",
        "**Behaviors**": "Behaviors & Habits:",
        "**Behaviors & Habits**": "Behaviors & Habits:",
        "**Goals**": "Goals & Needs:",
        "**Goals & Needs**": "Goals & Needs:",
        "**Personality**": "Personality:",
        "**CITED EXAMPLES FROM REDDIT**": "CITED EXAMPLES FROM REDDIT:"
    }

    for key, value in replacements.items():
        raw_text = raw_text.replace(key, value)

    return raw_text

def generate_persona_with_openrouter(content, username, return_text=False, max_words=1500):
    # Step 1: Truncate Reddit content
    words = content.split()
    truncated_content = ' '.join(words[:max_words])

    # Step 2: Generate main persona
    persona_prompt = f"""
You are a UX researcher creating a detailed, marketing-style user persona from Reddit activity.

From the posts and comments below, generate a persona with:
- A 2-line summary quote/introduction
- Name (or alias), Age, Occupation, Location (if guessable)
- Tier (e.g., Tier 1-5), Archetype (e.g., Power User, Curious Lurker, etc.)
- Motivations
- Preferences
- Frustrations
- Behaviors & Habits
- Goals & Needs
- Personality (MBTI-style: I/E, N/S, F/T, P/J)

Structure your output with bold section headers like **Motivations**, **Goals**, etc.

--- REDDIT USER CONTENT START ---
{truncated_content}
--- REDDIT USER CONTENT END ---
"""
    persona_text = call_openrouter_api(persona_prompt)
    if persona_text is None:
        return "Error generating persona."

    # Step 3: Generate cited examples
    cited_examples_prompt = f"""
You are continuing the same UX analysis of this Reddit user.

Given the following **persona** and the same **Reddit user content**, provide a section called **CITED EXAMPLES FROM REDDIT**.

Each cited example should include:
- The exact quote or paraphrased line
- The subreddit (e.g., r/technology)
- What that quote reveals about the user’s values, preferences, or behavior

Give exactly 4 examples, clearly structured like this:
**CITED EXAMPLES FROM REDDIT**
- r/subreddit: "quote" → explanation

--- PERSONA START ---
{persona_text}
--- PERSONA END ---

--- REDDIT USER CONTENT START ---
{truncated_content}
--- REDDIT USER CONTENT END ---
"""
    cited_examples_text = call_openrouter_api(cited_examples_prompt)
    if cited_examples_text is None:
        return "Error generating cited examples."

    
    raw_output = f"{persona_text}\n\n{cited_examples_text}"
    cleaned_output = clean_persona_output(raw_output)

   
    save_path = f"data/outputs/{username}_persona_combined.txt"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(cleaned_output)

    print(f"Persona with citations saved to: {save_path}")
    print(cleaned_output[:1000], "...\n")

    if return_text:
        return cleaned_output
