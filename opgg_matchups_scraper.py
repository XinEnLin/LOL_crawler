import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

OUTPUT_DIR = "matchup_data"

opponent_names = [
    "aatrox", "ahri", "akali", "akshan", "alistar", "amumu", "anivia", "annie", "aphelios", "ashe",
    "aurelionsol", "azir", "bard", "belveth", "blitzcrank", "brand", "braum", "briar", "caitlyn",
    "camille", "cassiopeia", "chogath", "corki", "darius", "diana", "drmundo", "draven", "ekko",
    "elise", "evelynn", "ezreal", "fiddlesticks", "fiora", "fizz", "galio", "gangplank", "garen",
    "gnar", "gragas", "graves", "gwen", "hecarim", "heimerdinger", "hwei", "illaoi", "irelia",
    "ivern", "janna", "jarvaniv", "jax", "jayce", "jhin", "jinx", "kaisa", "kalista", "karma",
    "karthus", "kassadin", "katarina", "kayle", "kayn", "kennen", "khazix", "kindred", "kled",
    "kogmaw", "ksante", "leblanc", "leesin", "leona", "lillia", "lissandra", "lucian", "lulu", "lux",
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

champion_names = [ "xayah", "xerath", "xinzhao", "yasuo", "yone",
    "yorick", "yuumi", "zac", "zed", "zeri", "ziggs", "zilean", "zoe", "zyra"
]


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_champion_vs_opponent(champion, opponent):
    url = f"https://op.gg/lol/champions/{champion}/counters?target_champion={opponent}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        print(f"❌ 失敗: {champion} vs {opponent} - HTTP {r.status_code}")
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    outer_block = soup.select_one("div.flex.w-full.flex-col.gap-2")
    if not outer_block:
        print(f"⚠️ 無資料區塊: {champion} vs {opponent}")
        return None

    result = {"Opponent": opponent}

    # ✅ 抓取對線勝率（左邊是 champion，右邊是 opponent）
    winrate_block = soup.select_one("div.flex.w-full.items-center.justify-center.gap-4")
    if winrate_block:
        left = winrate_block.select_one("span.absolute.left-0")
        right = winrate_block.select_one("span.absolute.right-0")
        if left and right:
            result["Self_winrate"] = left.text.strip()
            result["Opponent_winrate"] = right.text.strip()

    # ✅ 抓取其他指標（如 KDA、擊殺參與率…）
    stat_blocks = outer_block.select("div.flex.w-full.flex-col.gap-4 div.relative.pt-7")
    for stat in stat_blocks:
        spans = stat.select("span")
        if len(spans) < 3:
            continue
        self_val = spans[0].text.strip()
        stat_name = spans[1].text.strip()
        opp_val = spans[2].text.strip()
        result[f"Self_{stat_name}"] = self_val
        result[f"Opponent_{stat_name}"] = opp_val

    return result

def fetch_all_matchups_for_champion(champion):
    print(f"🔍 處理 {champion} 的對線資料...")
    all_data = []
    for opponent in opponent_names:
        if champion == opponent:
            continue
        data = fetch_champion_vs_opponent(champion, opponent)
        if data:
            all_data.append(data)
        time.sleep(0.5)  # 降低請求速度，避免封鎖
    return all_data

def main():
    for champ in champion_names:
        matchups = fetch_all_matchups_for_champion(champ)
        if matchups:
            df = pd.DataFrame(matchups)
            filename = f"{champ}.csv"
            output_path = os.path.join(OUTPUT_DIR, filename)  # 把資料夾與檔名組合成完整路徑
            df.to_csv(output_path, index=False, encoding="utf-8-sig")
            print(f"✅ 已儲存 {filename}")
        else:
            print(f"⚠️ {champ} 沒有任何對線資料")

if __name__ == "__main__":
    main()
