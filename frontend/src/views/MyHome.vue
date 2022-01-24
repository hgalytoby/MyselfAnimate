<template>
  <div class="fs-4">您好</div>
  <div class="p-4"></div>
  <div class="fs-4">websocket
    <div class="fs-4">action: {{ $store.state.ws.wsClick.action }}</div>
    <div class="fs-4">msg: {{ $store.state.ws.wsClick.msg }}</div>
  </div>
  <div class="p-4"></div>
  <div>
    <div class="fs-4">用的套件如下</div>
    <div><a href="https://github.com/dafcoe/vue-notification">notification/toast</a></div>
    <div><a href="https://github.com/aacassandra/vue3-progressbar">Progressbar</a></div>
    <div><a href="https://github.com/dvuckovic/vue3-bootstrap-icons">bootstrap-icons</a></div>
    <div><a href="https://github.com/szboynono/mosha-vue-toastify">Mosha Vue Toastify</a></div>
    <div><a href="https://github.com/linmasahiro/vue3-table-lite">vue3-table-lite</a></div>
  </div>
  <div class="p-4"></div>
  <div>
    <div class="fs-4">學習與研究!</div>
    <div class="fs-4">應在24小時內刪除影片。</div>
  </div>
</template>

<script>
export default {
  name: 'MyHome',
  setup () {
    return {}
  }
}
</script>

<style scoped>

</style>
