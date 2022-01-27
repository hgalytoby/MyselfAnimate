# 現在還在開發中，隨時都可能放棄。
我從 Traffic 上看到有人在 clone 此專案，所以我說明一下。

本來要開其他分支進行開發，但因為在其他分支 push 後，github 不會顯示我今天有 commit 的紀錄，因我不想斷 commit 連續天數，所以我就 push master。

正因為我都 push master，所以 clone 下來運行可能會發生程式錯誤的關係導致無法運行是正常的。


## Demo 2022/01/08
頁面刻板還在學習，目前先做功能出來，此專案還有 Bug 要修。

看影片了解一下此專案有哪些功能。

此影片為技術探討，不作其他營利用途。

研究爬蟲 Api 。

研究完畢請將下載的影片刪除。

謝謝。

### 點擊圖片可以在 Youtube 上觀看。
[![Demo](https://i.imgur.com/6G1kPWD.png)](https://youtu.be/ZW70RJYAwek)

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
    - 傳送下載進度給前端做顯示，不需一直 ajax 去後端看下載進度。

# 目前狀況
## 只有基本下載與網頁觀看影片
- `docker compose build`
- `docker-compose up` 
- 我試過沒有問題了

# 問題
- 自己學 HTML CSS JavaScript 都還沒很熟我就直接學 Vue 了，遇到前端問題會卡很久。
- 很多資料與功能還沒串起來。
- 版面設計 RWD 還在學習中。
- 2021/12月底我整好 Anime1 的 Api，但是在 2022/1 月中時， Anime1 改了 3 次 Api，必須一直更新才行。
- Anime1 有些影片是連接 Youtube，目前還沒修好下載 Youtube 影片的方法，預計是用 yt-dlp。
- 不知道何時完成。



