<template>
  <table class="table table-striped">
    <thead>
    <tr>
      <th scope="col">動畫名稱</th>
      <th scope="col">集數</th>
      <th scope="col">年份</th>
      <th scope="col">季節</th>
      <th scope="col">字幕組</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="animate in animateList" :key="animate.url">
      <td>
        <router-link :to="{
              name: 'Anime1Animate',
              params: {
                animateData: JSON.stringify(animate)
                },
              query: {
                url: animate.url === '0' ? 123456 : animate.url
              }
            }">{{ animate.name }}
        </router-link>
      </td>
      <td>{{animate.episode}}</td>
      <td>{{animate.years}}</td>
      <td>{{animate.season}}</td>
      <td>{{animate.subtitle_group}}</td>
    </tr>
    </tbody>
  </table>
</template>

<script>
import { useStore } from 'vuex'
import { computed } from 'vue'
import { animateListAction, animateListState } from '../../variables/anime1'

export default {
  name: 'AnimateList',
  setup () {
    const store = useStore()
    store.dispatch(`anime1/${animateListAction}`)
    const animateList = computed(() => store.state.anime1[animateListState])
    return {
      animateList
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
