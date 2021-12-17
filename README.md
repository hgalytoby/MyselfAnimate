# 現在還在開發中，隨時都可能放棄。
本來應該要開其他分支進行開發，但因為在其他分支 push 程式 github 不會顯示我今天有 commit，因我不想斷 commit 連續天數，所以我就 push master。

正因為我都 push master，所以 clone 下來運行可能會發生程式錯誤的關係導致無法運行是正常的。


## 目標是想做一個整合下載的網頁
- 我現在只有 [Myself](https://myself-bbs.com/portal.php) 與 [Anime1.me](https://anime1.me/) 不需登入會員就能下載 `720p` 影片。
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
- `docker compose build`
- `docker-compose up` 
- 我試過沒有問題了

# 問題
- 1.自己學 HTML CSS JavaScript 都還沒很熟我就直接學 Vue 了，遇到前端問題會卡很久。
- 2.很多資料與功能還沒串起來。
- 3.版面設計 RWD 還在學習中。
- 4.不知道何時完成。



