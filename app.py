import os
import requests
import streamlit as st
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from collections import Counter

# Load GitHub token from .env
load_dotenv()
token = os.getenv("GITHUB_TOKEN")

# Streamlit UI setup
st.set_page_config(page_title="GitHub Analyzer", layout="centered")
st.title("🐙 GitHub Repository Analyzer")

# GitHub username input
username = st.text_input("🔍 Enter a GitHub username", value="anilefecftc")

if not username:
    st.warning("Please enter a GitHub username.")
    st.stop()

# Get user info
user_url = f"https://api.github.com/users/{username}"
headers = {"Authorization": f"token {token}"}
user_resp = requests.get(user_url, headers=headers)
user_data = user_resp.json()

# Error handling
if isinstance(user_data, dict) and "message" in user_data:
    st.error(f"❌ User not found: {user_data['message']}")
    st.stop()

# Display user info
st.subheader("👤 User Information")
col1, col2 = st.columns([1, 3])
with col1:
    st.image(user_data["avatar_url"], width=100)
with col2:
    st.markdown(f"**Name:** {user_data.get('name') or 'Not provided'}")
    st.markdown(f"**Bio:** {user_data.get('bio') or 'No bio'}")
    st.markdown(f"**Followers:** {user_data.get('followers')} &nbsp;&nbsp; **Following:** {user_data.get('following')}")

# Get repo data
repo_url = f"https://api.github.com/users/{username}/repos"
repo_resp = requests.get(repo_url, headers=headers)
repos = repo_resp.json()

# Total repository count
st.subheader("📦 Total Public Repositories")
st.write(len(repos))

# List repositories with star count
st.subheader("⭐ Repositories")
if repos:
    for repo in repos:
        st.write(f"- {repo['name']} → ⭐ {repo['stargazers_count']} stars")
else:
    st.info("This user has no public repositories.")

# Language usage analysis
languages = [repo['language'] for repo in repos if repo['language'] is not None]
language_counts = Counter(languages)

st.subheader("🌐 Most Used Languages")
if language_counts:
    for lang, count in language_counts.most_common():
        st.write(f"- {lang}: {count} repos")

    # Pie chart for language distribution
    fig1, ax1 = plt.subplots()
    ax1.pie(language_counts.values(), labels=language_counts.keys(), autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)
else:
    st.info("No language data available.")

# Most starred repository
if repos:
    most_starred = max(repos, key=lambda r: r['stargazers_count'])
    st.subheader("🏆 Most Starred Repository")
    st.write(f"{most_starred['name']} → ⭐ {most_starred['stargazers_count']} stars")
