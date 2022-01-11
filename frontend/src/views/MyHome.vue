<template>
  <h1>還不知道要放什麼的首頁</h1>
  <h2>webSocket</h2>
  <h4>action: {{ $store.state.ws.wsClick.action }}</h4>
  <h4>msg: {{ $store.state.ws.wsClick.msg }}</h4>
  <div><a href="https://github.com/dafcoe/vue-notification">notification/toast</a></div>
  <div><a href="https://github.com/aacassandra/vue3-progressbar">Progressbar</a></div>
  <div><a href="https://github.com/dvuckovic/vue3-bootstrap-icons">bootstrap-icons</a></div>
  <div><a href="https://github.com/szboynono/mosha-vue-toastify">Mosha Vue Toastify</a></div>
  <div>學習與研究!</div>
  <div>應在24小時內刪除影片。</div>
</template>

<script>

import { createToast, withProps } from 'mosha-vue-toastify'
import CustomToast from '../components/CustomToast'
import { useStore } from 'vuex'
import { animateInfoEpisodeInfoAction } from '../variables/myself'

export default {
  name: 'MyHome',
  setup () {
    const store = useStore()
    store.dispatch(`myself/${animateInfoEpisodeInfoAction}`, { value: { id: 1 } })
    function toast () {
      createToast(withProps(CustomToast, { msg: '哈哈哈' }),
        {
          transition: 'slide',
          position: 'top-center',
          showCloseButton: false
        })
    }
    return {
      toast
    }
  }
}
</script>

<style scoped>

</style>
