# LOL_crawler

這是一個用於爬取 OPGG 英雄對戰數據的 Python 專案，使用 `requests`、`BeautifulSoup` 與 `pandas` 對網頁內容進行解析與儲存。

## 📁 專案結構

```
LOL_crawler/
├── adc_matchups.csv         # ADC 對戰資料
├── mid_matchups.csv         # 中路對戰資料
├── top_matchups.csv         # 上路對戰資料
├── opgg_matchups_scraper.py # 主爬蟲程式
├── requirements.txt         # 套件依賴列表
└── README.md                # 說明文件（你現在正在看）
```

## 🔧 環境建置

建議使用虛擬環境來隔離開發環境：

```bash
# 建立虛擬環境
python -m venv .venv

# 啟動虛擬環境（Windows）
.venv\Scripts\activate

# 安裝所需套件
pip install -r requirements.txt
```

## 🚀 執行爬蟲

啟動虛擬環境後，執行以下指令來開始爬蟲：

```bash
python opgg_matchups_scraper.py
```

執行完畢後會輸出 `.csv` 對戰資料於專案資料夾中。

## 🧰 主要套件

- `requests` - 發送 HTTP 請求
- `beautifulsoup4` - 網頁資料解析
- `pandas` - 資料處理與儲存

## 📌 注意事項

- 若從 GitHub clone 本專案，請務必先依照上方步驟建立 `.venv` 虛擬環境再執行。
- 若有新增套件，記得執行 `pip freeze > requirements.txt` 以更新依賴列表。
