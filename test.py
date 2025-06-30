import requests

url = "https://www.op.gg/api/v1.0/internal/champions/neeko/matchups?position=mid&region=global&tier=platinum_plus"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.op.gg/lol/champions/neeko/counters/mid"
}

res = requests.get(url, headers=headers)
print(res.json())
