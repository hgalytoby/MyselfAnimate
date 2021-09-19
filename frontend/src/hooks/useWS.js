import { useStore } from 'vuex'

const wsUrl = 'ws://127.0.0.1:8000'
const socket = new WebSocket(wsUrl)
export const connectSocket = () => {
  const store = useStore()
  socket.onopen = function () {
    console.log('websocket connected!!')
  }
  socket.onmessage = function (msg) {
    store.commit('ws/setWsRes', JSON.parse(msg.data))
    console.log('onmessage', JSON.parse(msg.data))
  }
  socket.onerror = function (err) {
    console.log('error', err)
  }
}
export const sendSocketMessage = msg => {
  if (socket.readyState === 1) socket.send(JSON.stringify(msg))
}
