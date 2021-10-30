<template>
  <div>我的首頁</div>
  <span>我的首頁</span>
  <h1>我的首頁</h1>
  <button @click="onSubmit">Login</button>
  <!--  <h3>webSocket: {{ $store.getters['ws/getWsWhile'] }}</h3>-->
  <h3>webSocket: {{ $store.state.ws.wsClick }}</h3>
</template>

<script>
import { sendSocketMessage } from '../hooks/useWS'

export default {
  name: 'MyHome',
  setup () {
    const onSubmit = () => {
      console.log('我按下去了')
      sendSocketMessage({
        msg: 'some message to websocket server'
      })
    }
    return {
      onSubmit
    }
  }
}
</script>

<style scoped>

</style>
