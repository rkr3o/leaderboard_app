import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()

from django.db.models import Sum
from django.db import transaction
from apps.db_manager.models import GameSession, Leaderboard

import requests
import random
import time

HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJuYW1lIjoiVGVzdCIsImlhdCI6MTc1MzI5NDA2NywiZXhwIjoxNzUzMjk3NjY3fQ.MR2ZXZo7fZBmpMG1SsJt6tzxjg7FQjmfAK-Qs0itgjk",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "DNT": "1",
    "Origin": "http://localhost:3000",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
}

API_BASE_URL = "http://localhost:8000/api/leaderboard/"

# Simulate score submission
def submit_score(user_id):
    score = random.randint(100, 10000)
    requests.post(f"{API_BASE_URL}submit/", json={"user_id": user_id, "score": score}, headers=HEADERS)

# Fetch top players
def get_top_players():
    response = requests.get(f"{API_BASE_URL}top/", headers=HEADERS)
    return response.json()

# Fetch user rank
def get_user_rank(user_id):
    response = requests.get(f"{API_BASE_URL}rank/", headers=HEADERS, params={"user_id": user_id})
    return response.json()

if __name__ == "__main__":
    while True:
        user_id = random.randint(1, 1000000)
        submit_score(user_id)
        print(get_top_players())
        print(get_user_rank(user_id))
        time.sleep(random.uniform(0.5, 2))