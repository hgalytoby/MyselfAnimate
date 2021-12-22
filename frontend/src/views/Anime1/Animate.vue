<template>
  <div>Anime1Animate</div>
  <div>{{ animateInfo }}</div>
</template>

<script>
import { useStore } from 'vuex'
import { computed } from 'vue'
import { animateInfoAction, animateInfoState } from '../../variables/anime1'

export default {
  name: 'Animate',
  props: {
    url: String
  },
  setup (props) {
    const store = useStore()
    const animateInfo = computed(() => store.state.anime1[animateInfoState])
    console.log('props', props)
    store.dispatch(`anime1/${animateInfoAction}`, props.url)
    return {
      animateInfo
    }
  }
}
</script>

<style scoped>

</style>
