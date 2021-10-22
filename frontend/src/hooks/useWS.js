import { useStore } from 'vuex'
import { finishAnimateUpdateButtonMutation } from '../variables/variablesMyself'
const wsUrl = 'ws://127.0.0.1:8000/ws/'
const socket = new WebSocket(wsUrl)

export const sendSocketMessage = msg => {
  if (socket.readyState === 1) socket.send(JSON.stringify(msg))
}

export const connectSocket = () => {
  const store = useStore()
  socket.onopen = function () {
    console.log('websocket connected!!')
    // sendSocketMessage(JSON.stringify({ msg1: '我要跟後端連線了!' }))
  }
  socket.onmessage = function (msg) {
    console.log('onmessage', JSON.parse(msg.data))
    const receive = JSON.parse(msg.data)
    if (receive.action === 'myself_finish_animate_update') {
      store.commit(`myself/${finishAnimateUpdateButtonMutation}`, receive)
    } else if (receive.action === 'download_myself_animate') {
      console.log(receive)
    } else if (receive.action === 'download_myself_animate_array') {
      store.commit('myself/downloadMyselfAnimateMutation', receive.data)
    } else if (receive.action === 'search_myself_animate') {
      store.commit('myself/searchMyselfAnimateMutation', receive.data)
    } else {
      store.commit('ws/setWsRes', JSON.parse(msg.data))
    }
  }
  socket.onerror = function (err) {
    console.log('error', err)
  }
}
