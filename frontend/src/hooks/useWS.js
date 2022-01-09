import { useStore } from 'vuex'
import { finishAnimateUpdateButtonMutation } from '../variables/myself'
import { setToast, toastData } from '../tools'
import { createToast } from 'mosha-vue-toastify'

const wsUrl = process.env.VUE_APP_WS === 'dev' ? 'ws://127.0.0.1:8000/ws/' : `ws://${location.host}/ws/`
const socket = new WebSocket(wsUrl)

export const sendSocketMessage = msg => {
  if (socket.readyState === 1) socket.send(JSON.stringify(msg))
}

export const connectSocket = () => {
  const store = useStore()
  socket.onopen = function () {
    console.log('websocket connected!!')
    sendSocketMessage({ action: 'connect' })
  }
  socket.onmessage = function (msg) {
    console.log('onmessage', JSON.parse(msg.data))
    const receive = JSON.parse(msg.data)
    if (receive.action === 'myself_finish_animate_update') {
      store.commit(`myself/${finishAnimateUpdateButtonMutation}`, receive)
      if (receive.updating) {
        createToast(...toastData.myselfFinishAnimateUpdate)
      } else {
        setToast(toastData.myselfFinishAnimateUpdateFinish)
      }
    } else if (receive.action === 'download_myself_animate') {
      console.log(receive)
    } else if (receive.action === 'download_myself_animate_array') {
      store.commit('myself/downloadMyselfAnimateMutation', receive.data)
    } else if (receive.action === 'search_myself_animate') {
      store.commit('myself/searchMyselfAnimateMutation', receive.data)
    } else if (receive.action === 'clear_finish_myself_animate') {
    } else if (receive.action === 'download_order_myself_animate') {
    } else if (receive.action === 'download_anime1_animate_array') {
      store.commit('anime1/downloadAnime1AnimateMutation', receive.data)
    } else if (receive.action === 'download_animate_finish') {
      setToast(toastData.downloadAnimateFinish(receive.data))
    } else if (receive.action === 'connect') {
      createToast(...toastData.connectOk)
    } else {
      store.commit('ws/setWsRes', JSON.parse(msg.data))
    }
  }
  socket.onerror = function (err) {
    console.log('error', err)
  }
  socket.onclose = function (err) {
    console.log('onclose', err)
  }
}
