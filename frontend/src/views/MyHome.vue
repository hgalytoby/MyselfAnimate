<template>
  <div>我的首頁</div>
  <span>我的首頁</span>
  <h1>我的首頁</h1>
  <button @click="onSubmit">Login</button>
  <pagination v-model="page" :records="500" :per-page="25" @paginate="myCallback"/>
  <!--  <h3>webSocket: {{ $store.getters['ws/getWsWhile'] }}</h3>-->
  <h3>webSocket: {{ $store.state.ws.wsClick }}</h3>
</template>

<script>
import { sendSocketMessage } from '../hooks/useWS'
import { ref } from 'vue'

export default {
  name: 'MyHome',
  setup () {
    const page = ref(1)
    const onSubmit = () => {
      console.log('我按下去了')
      sendSocketMessage({
        msg: 'some message to websocket server'
      })
    }
    function myCallback (page) {
      console.log(page)
    }
    return {
      onSubmit,
      page,
      myCallback
    }
  }
}
</script>

<style scoped>

</style>
