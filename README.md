# 成大 (NCKU) 自動計算迄今總 GPA
- 可自計算在成績系統上，已出現在「歷年選課成績資料查詢」成績已確認的學期。
- 結果會有：迄今為止總 GPA、總GPA加權、有成績科目總學分數以及各學期有成績課目細節

## 用法
1. 下載專案
2. 進終端機下 `cd ncku-grade-parser`
3.
    - 用 uv `uv venv .` 建立虛擬環境，然後下 `source .venv/bin/activate` 或 `.\venv\Scripts\activate.ps1`，最後 `uv sync`
    - 不是 uv 的話，建立虛擬環境開啟後安裝 `selenium`
4. 安裝完成後 `python main.py` 然後會開啟網頁，登入網頁後就會自動爬取，結果會顯示在終端機