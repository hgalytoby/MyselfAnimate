<template>
  <Sidebar/>
</template>

<script>
import Sidebar from './components/Sidebar'
import { connectSocket } from './hooks/useWS'
import 'animate.css'

export default {
  name: 'App',
  components: { Sidebar },
  setup () {
    connectSocket()
    return {}
  }
}
</script>

<style lang="scss">
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@500&display=swap');

  * {
    font-family: 'Noto Sans TC', 'Poppins', sans-serif;
  }

  * ::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
    border-radius: 10px;
    background-color: transparent;
  }

  * ::-webkit-scrollbar {
    width: 8px;
    background-color: transparent;
  }

  * ::-webkit-scrollbar-thumb {
    border-radius: 10px;
    -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, .3);
    background-color: rgba(109, 106, 106, 0.12);
  }

  body {
    .fancybox__content {
      width: 80% !important;
      height: 100% !important;
    }
  }
</style>
