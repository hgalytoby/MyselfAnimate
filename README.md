## Demo 2022/01/08
這是我學習 Vue 後與 Django 結合的專案。

目前有新的想法想做的更大一點，所以此專案只做為我練習設計架構與熟悉 Vue 的用途。

看影片了解一下此專案有哪些功能。

此影片為技術探討，不作其他營利用途。

研究爬蟲 Api 。

研究完畢請將下載的影片刪除。

謝謝。


### 點擊圖片可以在 Youtube 上觀看。
[![Demo](https://i.imgur.com/6G1kPWD.png)](https://youtu.be/ZW70RJYAwek)

## 目標是想做一個整合下載的網頁
- 目前有 [Myself](https://myself-bbs.com/portal.php) 與 [Anime1.me](https://anime1.me/)
- 前端 Vue3
- 後端 Django-Restframework
- Websocket Django-Channels
- 個人使用，資料庫 Sqlite
- 快取 Redis
    - [Windows](https://github.com/tporadowski/redis/releases)
    - [Mac Linux](http://download.redis.io)
- 使用 ffmpeg 合併影片
    - Windows
        - [官網下載](https://ffmpeg.org/)
    - Mac
        - `brew install ffmpeg`
    - Linux:
        - `apt-get install ffmpeg`
- 使用 Docker 部屬
- Youtube 影片 yt-dlp

# 目前狀況
## 只有基本下載與網頁觀看影片
- `docker compose build`
- `docker compose up` 
- 我試過沒有問題了。

