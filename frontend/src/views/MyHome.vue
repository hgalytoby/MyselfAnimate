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
  <div class="card">
  <h5 class="card-header">Featured</h5>
  <div class="card-body">
    <h5 class="card-title">Special title treatment</h5>
    <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
    <a href="#" class="btn btn-primary">Go somewhere</a>
  </div>
</div>
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
