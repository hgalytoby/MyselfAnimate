# 現在還在開發中，隨時都可能放棄。

## 目標是想做一個整合下載的網頁
- 前端使用 Vue3
- 後端使用 Django
- 因為只給自己使用的，所以資料庫用 Sqlite
- WebSocket 需要使用 redis
    - 下載
        - [Windows](https://github.com/tporadowski/redis/releases)
        - [Mac Linux](http://download.redis.io)
- 使用 ffmpeg 合併影片
    - 下載
        - Windows
            - [官網下載](https://ffmpeg.org/)
        - Mac
            - `brew install ffmpeg`
        - Linux:
            - `apt-get install ffmpeg`
- 為什麼使用 WebSocket ?
    - 傳送下載進度給前端做顯示，不用一直 ajax 去後端看下載進度。

# 目前狀況
## 只有基本下載與網頁觀看影片
`docker-compose up` 我試過沒問題了

# 問題
- 1.不知道 npm run serve 怎麼設定 websocket url，不然每次用 Docker 我都要改一下 websocket url。
- 2.自己學 HTML CSS JavaScript 都還沒很熟我就直接學 Vue 了，遇到前端問題會卡很久。
- 3.很多資料與功能還沒串起來。
- 4.版面設計 RWD 還在學習中。
- 5.不知道何時完成。



