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
    return {
    }
  }
}
</script>

<style lang="scss" scoped>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@500&display=swap');
  * {
    font-family: 'Noto Sans TC', 'Poppins', sans-serif;
  }
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }

  #nav {
    padding: 30px;

    a {
      font-weight: bold;
      color: #2c3e50;

      &.router-link-exact-active {
        color: #42b983;
      }
    }
  }
</style>
