# 外送平台優惠碼爬蟲

這個專案旨在爬取並整理 Uber、UberEats 和 Foodpanda 的優惠碼,並生成一個易於瀏覽的 HTML 頁面。

## 主要功能

- 爬取 Uber、UberEats 和 Foodpanda 的優惠碼
- 將優惠碼按照類別整理
- 生成包含所有優惠碼的 HTML 頁面
- 支持一鍵複製優惠碼並打開相應的 APP

## 文件說明

- `scrape_delivery_codes.py`: 主要的爬蟲和 HTML 生成腳本
- `DeliveryCodes.html`: 生成的包含所有優惠碼的 HTML 文件
- `coupon.PNG`: 網站圖標文件

## 使用方法

1. 確保已安裝所需的 Python 庫:
   ```bash
   pip install requests beautifulsoup4 jinja2
   ```

2. 運行爬蟲腳本:
   ```bash
   python scrape_delivery_codes.py
   ```

3. 在瀏覽器中打開生成的 `DeliveryCodes.html` 文件查看結果

## 注意事項

- 請確保 `coupon.PNG` 文件與生成的 HTML 文件在同一目錄下
- 爬蟲結果的準確性取決於源網站的結構,如遇到問題請檢查源網站是否有變動


## 貢獻

歡迎提出建議和改進意見!

## 授權

本專案採用 MIT 授權協議。
