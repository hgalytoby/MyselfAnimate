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
  <div class="card" aria-hidden="true">
    <img src="" class="card-img-top" alt="">
    <div class="card-body">
      <h5 class="card-title placeholder-glow">
        <span class="placeholder col-6"></span>
      </h5>
      <p class="card-text placeholder-glow">
        <span class="placeholder col-7"></span>
        <span class="placeholder col-4"></span>
        <span class="placeholder col-4"></span>
        <span class="placeholder col-6"></span>
        <span class="placeholder col-8"></span>
      </p>
      <a href="#" tabindex="-1" class="btn btn-primary disabled placeholder col-6"></a>
    </div>
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
