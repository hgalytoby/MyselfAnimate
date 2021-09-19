<template>
  <div>我是 Myself</div>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <span class="nav-link active" v-on:mouseover="changeWeek('Monday')" aria-current="page">星期一</span>
          </li>
          <li class="nav-item">
            <span class="nav-link" v-on:mouseover="changeWeek('Tuesday')" aria-current="page">星期二</span>
          </li>
          <li class="nav-item">
            <span class="nav-link" v-on:mouseover="changeWeek('Wednesday')" aria-current="page">星期三</span>
          </li>
          <li class="nav-item">
            <span class="nav-link" v-on:mouseover="changeWeek('Thursday')" aria-current="page">星期四</span>
          </li>
          <li class="nav-item">
            <span class="nav-link" v-on:mouseover="changeWeek('Friday')" aria-current="page">星期五</span>
          </li>
          <li class="nav-item">
            <span class="nav-link" v-on:mouseover="changeWeek('Saturday')" aria-current="page">星期六</span>
          </li>
          <li class="nav-item">
            <span class="nav-link" v-on:mouseover="changeWeek('Sunday')" aria-current="page">星期日</span>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <div>
    <li v-for="data in activeWeek" :key="data.name">
      <a :href="data.url">{{ data.name }}</a>{{ data.update }}{{ data.update_color }}
    </li>
    <div/>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'Myself',
  setup () {
    const store = useStore()
    store.dispatch('api/weekAnimateAction')
    const activeWeek = computed(() => store.state.api.activeWeek)
    const weekAnimateData = computed(() => store.state.api.weekAnimateData)
    function changeWeek (status) {
      store.commit('api/changeActiveWeek', status)
    }
    return {
      changeWeek,
      activeWeek,
      weekAnimateData
    }
  }
}
</script>

<style scoped>

</style>
