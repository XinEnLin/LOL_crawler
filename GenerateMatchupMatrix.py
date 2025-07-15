import os
import pandas as pd

# 設定你的csv資料夾路徑
DATA_DIR = "./matchup_data"

# 所有欄位（含Self與Opponent）
COLUMNS = [
    "Self_winrate", "Opponent_winrate",
    "Self_Lane Kill Rate", "Opponent_Lane Kill Rate",
    "Self_KDA", "Opponent_KDA",
    "Self_Kill participation", "Opponent_Kill participation",
    "Self_Win rate", "Opponent_Win rate",
    "Self_Lane Win Rate", "Opponent_Lane Win Rate",
    "Self_Lane Pick Rate", "Opponent_Lane Pick Rate",
    "Self_Ban rate", "Opponent_Ban rate"
]

# 擷取所有角色檔案名稱（以 .csv 結尾）
champion_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
champions = [f[:-4] for f in champion_files]  # 去掉 .csv

# 為每個欄位建立一個空矩陣 DataFrame
matrices = {col: pd.DataFrame(index=champions, columns=champions, dtype=object) for col in COLUMNS}

# 讀取每個檔案
for file in champion_files:
    champ_name = file[:-4]
    df = pd.read_csv(os.path.join(DATA_DIR, file))

    for _, row in df.iterrows():
        opponent = row['Opponent']
        if pd.isna(opponent) or opponent not in champions:
            continue

        for col in COLUMNS:
            val = row.get(col)
            if pd.isna(val):
                continue
            if col.startswith("Self_"):
                matrices[col].at[champ_name, opponent] = val
            elif col.startswith("Opponent_"):
                matrices[col].at[opponent, champ_name] = val

# 輸出每個欄位的矩陣為 csv
OUTPUT_DIR = "./output_matrices"
os.makedirs(OUTPUT_DIR, exist_ok=True)

for col, df in matrices.items():
    sanitized_col = col.replace(" ", "_")
    df.to_csv(os.path.join(OUTPUT_DIR, f"matrix_{sanitized_col}.csv"))

print("✅ 所有矩陣已輸出完畢。")
