<template>
  <div>我是 Myself</div>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item" v-on:mouseover="changeWeek('Monday')">
            <span class="nav-link" :class="isActive('Monday')" aria-current="page">星期一</span>
          </li>
          <li class="nav-item" v-on:mouseover="changeWeek('Tuesday')">
            <span class="nav-link" :class="isActive('Tuesday')" aria-current="page">星期二</span>
          </li>
          <li class="nav-item" v-on:mouseover="changeWeek('Wednesday')">
            <span class="nav-link" :class="isActive('Wednesday')" aria-current="page">星期三</span>
          </li>
          <li class="nav-item" v-on:mouseover="changeWeek('Thursday')">
            <span class="nav-link" :class="isActive('Thursday')" aria-current="page">星期四</span>
          </li>
          <li class="nav-item"  v-on:mouseover="changeWeek('Friday')">
            <span class="nav-link" :class="isActive('Friday')" aria-current="page">星期五</span>
          </li>
          <li class="nav-item"  v-on:mouseover="changeWeek('Saturday')">
            <span class="nav-link" :class="isActive('Saturday')" aria-current="page">星期六</span>
          </li>
          <li class="nav-item" v-on:mouseover="changeWeek('Sunday')">
            <span class="nav-link" :class="isActive('Sunday')" aria-current="page">星期日</span>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <div>
    <li v-for="data in activeWeek" :key="data.name">
      <router-link :to="{
        name: 'MyselfAnimate',
        query: {
          url: data.url,
        }
      }">{{ data.name }}
        <span :style="data.update_color">{{ data.update }}</span>
      </router-link>
    </li>
    <div/>
  </div>
</template>

<script>
import { computed, onMounted, reactive } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'Myself',
  setup () {
    const weekDict = reactive({
      Monday: 1,
      Tuesday: 2,
      Wednesday: 3,
      Thursday: 4,
      Friday: 5,
      Saturday: 6,
      Sunday: 7,
      isActive: 1
    })
    const store = useStore()
    const activeWeek = computed(() => store.state.api.activeWeek)
    const weekAnimateData = computed(() => store.state.api.weekAnimateData)
    onMounted(() => {
      store.dispatch('api/weekAnimateAction')
    })
    function changeWeek (status) {
      store.commit('api/changeActiveWeek', status)
      // isActive.value++
      weekDict.isActive = weekDict[status]
      // console.log(isActive.value == 1)
    }
    function isActive (status) {
      return weekDict.isActive === weekDict[status] ? 'active' : ''
    }
    return {
      changeWeek,
      activeWeek,
      weekAnimateData,
      isActive,
      weekDict
    }
  }
}
</script>

<style lang="scss" scoped>
  a {
    text-decoration:none;
  }
  li {
    list-style-type: none;
  }
</style>
