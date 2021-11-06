# 現在還在開發中，隨時都可能放棄。

目標是想做一個整合下載的網頁

前端使用 Vue3

後端使用 Django

因為是只給自己使用的，所以資料庫用 sqlite

websocket 需要使用 redis 

windows: https://github.com/tporadowski/redis/releases

mac linux: http://download.redis.io

使用 ffmpeg

用 websocket 傳送下載進度給前端做顯示，不用一直 ajax 去後端看下載進度。

# 目前狀況

只有基本下載與網頁觀看影片

`Docker build` `Docker run` 我試過沒問題了

# 問題
- 1.不知道 npm run serve 怎麼設定 websocket url，不然每次用 Docker 我都要改一下 websocket url。
- 2.自己學 `Html` `Css` `JavaScript` 都還沒很熟我就直接學 Vue 了，遇到前端問題會卡很久。
- 3.一堆功能還沒串起來。
- 4.`Docker compose` 我還沒研究，所以目前我把一大堆東西都塞在一個 Dockerfile 裡面。
- 5.還沒試過導出動漫影片過，之前有用了一下 `volume` ，但還沒實際放到這專案用過。
- 6.版面設計 RWD 還在學習中。
- 7.想到再補。

我看 2021 年底或 2022 年初我才能弄好。



