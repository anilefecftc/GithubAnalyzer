import os
import requests
from dotenv import load_dotenv
from collections import Counter

# .env dosyasını yükle
load_dotenv()
token = os.getenv("GITHUB_TOKEN")
username = "anilefecftc"  # <-- BURAYA KENDİ GITHUB KULLANICI ADINI YAZ

# API'den veri çek
url = f"https://api.github.com/users/{username}/repos"
headers = {"Authorization": f"token {token}"}
response = requests.get(url, headers=headers)
repos = response.json()

# Hata kontrolü
if isinstance(repos, dict) and "message" in repos:
    print("❌ GitHub API Hatası:", repos["message"])
    exit()

# 1. Toplam repo sayısı
print(f"\n📦 Toplam repo sayısı: {len(repos)}")

# 2. Repo adları ve yıldız sayıları
print("\n⭐ Repo listesi:")
for repo in repos:
    print(f"{repo['name']} → ⭐ {repo['stargazers_count']} yıldız")

# 3. En çok kullanılan diller
languages = [repo['language'] for repo in repos if repo['language'] is not None]
language_counts = Counter(languages)

print("\n🌐 En çok kullanılan diller:")
for lang, count in language_counts.most_common():
    print(f"{lang}: {count} repo")

# 4. En çok yıldız alan repo
most_starred = max(repos, key=lambda r: r['stargazers_count'])
print(f"\n🏆 En çok yıldız alan repo: {most_starred['name']} → ⭐ {most_starred['stargazers_count']} yıldız")
