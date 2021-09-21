<template>
  <div>我是animate</div>
  <div v-if="loading">加載中...</div>
  <div v-else>
    <img :src="animateInfo.image" :alt="animateInfo.name">
    <li>名字{{ animateInfo.name }}</li>
    <li>作品類型{{ animateInfo.animate_type }}</li>
    <li>首播日期{{ animateInfo.premiere_date }}</li>
    <li>播放集數{{ animateInfo.episodes }}</li>
    <li>作者{{ animateInfo.author }}</li>
    <li>官方網站{{ animateInfo.official_website }}</li>
    <li>備註{{ animateInfo.remarks }}</li>
    <li>synopsis{{ animateInfo.synopsis }}</li>
    <li v-for="data in animateInfo.video" :key="data.name">
      <a :href="data.url">{{ data.name }}</a>
    </li>
  </div>

</template>

<script>
import { onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { animateInfoAction, animateInfoState, loadingMutation, loadingState } from '../variables/variablesMyself'

export default {
  name: 'Animate',
  props: ['url'],
  setup (props) {
    const store = useStore()
    const loading = computed(() => store.state.api[loadingState])
    const animateInfo = computed(() => store.state.api[animateInfoState])
    store.commit(`api/${loadingMutation}`)
    onMounted(() => {
      store.dispatch(`api/${animateInfoAction}`, props.url)
    })
    return {
      loading,
      animateInfo
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
