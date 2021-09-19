<template>
  <div>我是animate</div>
  <div v-if="myselfAnimateInfoLoading">加載中...</div>
  <div v-else>
    <img :src="myselfAnimateInfo.image" :alt="myselfAnimateInfo.name">
    <li>名字{{ myselfAnimateInfo.name }}</li>
    <li>作品類型{{ myselfAnimateInfo.animate_type }}</li>
    <li>首播日期{{ myselfAnimateInfo.premiere_date }}</li>
    <li>播放集數{{ myselfAnimateInfo.episodes }}</li>
    <li>作者{{ myselfAnimateInfo.author }}</li>
    <li>官方網站{{ myselfAnimateInfo.official_website }}</li>
    <li>備註{{ myselfAnimateInfo.remarks }}</li>
    <li>synopsis{{ myselfAnimateInfo.synopsis }}</li>
    <li v-for="data in myselfAnimateInfo.video" :key="data.name">
      <a :href="data.url">{{ data.name }}</a>
    </li>
  </div>

</template>

<script>
import { onMounted, computed } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'Animate',
  props: ['url'],
  setup (props) {
    const store = useStore()
    store.commit('api/initMyselfAnimateInfoLoading')
    const myselfAnimateInfoLoading = computed(() => store.state.api.myselfAnimateInfoLoading)
    const myselfAnimateInfo = computed(() => store.state.api.myselfAnimateInfo)
    onMounted(() => {
      store.dispatch('api/myselfAnimateInfoAction', props.url)
    })
    return {
      myselfAnimateInfoLoading,
      myselfAnimateInfo
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
