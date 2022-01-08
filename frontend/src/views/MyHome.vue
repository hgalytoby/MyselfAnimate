<template>
  <h1>還不知道要放什麼的首頁</h1>
  <h2>webSocket</h2>
  <h4>action: {{ $store.state.ws.wsClick.action }}</h4>
  <h4>msg: {{ $store.state.ws.wsClick.msg }}</h4>
  <div><a href="https://github.com/dafcoe/vue-notification">notification/toast</a></div>
  <div><a href="https://github.com/aacassandra/vue3-progressbar">Progressbar</a></div>
  <div><a href="https://github.com/dvuckovic/vue3-bootstrap-icons">bootstrap-icons</a></div>
</template>

<script>
import { useNotificationStore } from '@dafcoe/vue-notification'

export default {
  name: 'MyHome',
  setup () {
    const { setNotification } = useNotificationStore()
    function test () {
      setNotification({
        message: '<h1>Line 2<p>',
        type: 'info',
        showIcon: true,
        dismiss: {
          manually: true,
          automatically: true
        },
        duration: 5000,
        showDurationProgress: true,
        appearance: 'light'
      })
    }
    return {
      test
    }
  }
}
</script>

<style scoped>

</style>
