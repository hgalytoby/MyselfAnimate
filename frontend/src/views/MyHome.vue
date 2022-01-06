<template>
  <h1>還不知道要放什麼的首頁</h1>
  <h2>webSocket</h2>
  <h4>action: {{ $store.state.ws.wsClick.action }}</h4>
  <h4>msg: {{ $store.state.ws.wsClick.msg }}</h4>
</template>

<script>

export default {
  name: 'MyHome',
  setup () {
    return {
    }
  }
}
</script>

<style scoped>

</style>
