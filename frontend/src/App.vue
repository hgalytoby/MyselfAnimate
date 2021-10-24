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
