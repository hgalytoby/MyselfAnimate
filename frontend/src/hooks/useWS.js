import { useStore } from 'vuex'

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
    store.commit('ws/setWsRes', JSON.parse(msg.data))
  }
  socket.onerror = function (err) {
    console.log('error', err)
  }
}
