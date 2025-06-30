import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 英雄英文 key 名稱（用於 URL 中）
champion_names = [
    "aatrox", "ahri", "akali", "akshan", "alistar", "amumu", "anivia", "annie", "aphelios", "ashe",
    "aurelionsol", "azir", "bard", "belveth", "blitzcrank", "brand", "braum", "briar", "caitlyn",
    "camille", "cassiopeia", "chogath", "corki", "darius", "diana", "drmundo", "draven", "ekko",
    "elise", "evelynn", "ezreal", "fiddlesticks", "fiora", "fizz", "galio", "gangplank", "garen",
    "gnar", "gragas", "graves", "gwen", "hecarim", "heimerdinger", "hwei", "illaoi", "irelia",
    "ivern", "janna", "jarvaniv", "jax", "jayce", "jhin", "jinx", "kaisa", "kalista", "karma",
    "karthus", "kassadin", "katarina", "kayle", "kayn", "kennen", "khazix", "kindred", "kled",
    "kogmaw", "leblanc", "leesin", "leona", "lillia", "lissandra", "lucian", "lulu", "lux",
    "malphite", "malzahar", "maokai", "milio", "missfortune", "mordekaiser", "morgana", "naafiri",
    "nami", "nasus", "nautilus", "neeko", "nidalee", "nilah", "nocturne", "nunu", "olaf", "orianna",
    "ornn", "pantheon", "poppy", "pyke", "qiyana", "quinn", "rakan", "rammus", "reksai", "rell",
    "renata", "renekton", "rengar", "riven", "rumble", "ryze", "samira", "sejuani", "senna",
    "seraphine", "sett", "shaco", "shen", "shyvana", "singed", "sion", "sivir", "skarner",
    "smolder", "sona", "soraka", "swain", "sylas", "syndra", "tahmkench", "taliyah", "talon",
    "taric", "teemo", "thresh", "tristana", "trundle", "tryndamere", "twistedfate", "twitch",
    "udyr", "urgot", "varus", "vayne", "veigar", "velkoz", "vex", "vi", "viego", "viktor",
    "vladimir", "volibear", "warwick", "wukong", "xayah", "xerath", "xinzhao", "yasuo", "yone",
    "yorick", "yuumi", "zac", "zed", "zeri", "ziggs", "zilean", "zoe", "zyra"
]

# 設定模擬瀏覽器的標頭，避免被擋下請求
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# 📘 函式：抓取某個英雄在特定路線的對線資料
def fetch_matchups(champion, lane):
    url = f"https://op.gg/lol/champions/{champion}/counters/{lane}"  # 英文版網址
    r = requests.get(url, headers=HEADERS)
    
    # 如果請求失敗則略過該英雄
    if r.status_code != 200:
        print(f"[跳過] {champion} - HTTP {r.status_code}")
        return []

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(r.text, "html.parser")
    results = []

    # 找出所有對線英雄的 li 區塊
    rows = soup.select("li[class*=cursor-pointer]")

    # 逐一取出每個對線英雄名稱與勝率
    for row in rows:
        name_tag = row.select_one("span.text-ellipsis")           # 對手英雄名稱
        winrate_tag = row.select_one("strong.text-main-600")      # 勝率百分比

        if name_tag and winrate_tag:
            opponent_name = name_tag.text.strip()
            winrate_text = winrate_tag.text.strip().replace("%", "")
            try:
                winrate = float(winrate_text)  # 嘗試轉成浮點數
            except:
                winrate = None

            results.append({
                "Champion": champion,
                "Opponent": opponent_name,
                "WinRate (%)": winrate
            })

    return results

# 📘 主程式：依照指定路線，逐一抓取所有英雄的對線資料
def main():
    lane = input("請輸入路線（adc/mid/top/jungle/support）：").strip().lower()
    valid_lanes = {"adc", "mid", "top", "jungle", "support"}

    # 驗證輸入是否合法
    if lane not in valid_lanes:
        print(f"❌ 無效路線：{lane}")
        return

    all_matchups = []

    # 逐一抓取每位英雄的資料
    for i, champ in enumerate(champion_names):
        print(f"[{i+1}/{len(champion_names)}] 抓取 {champ} 的對線資料（{lane}）...")
        data = fetch_matchups(champ, lane)
        all_matchups.extend(data)
        time.sleep(0.5)  # 加入延遲避免過快請求被封鎖

    # 儲存成 CSV 檔案
    df = pd.DataFrame(all_matchups)
    output_filename = f"{lane}_matchups.csv"
    df.to_csv(output_filename, index=False, encoding="utf-8-sig")
    print(f"✅ 對線資料已儲存為 {output_filename}")

# 執行主程式
if __name__ == "__main__":
    main()
