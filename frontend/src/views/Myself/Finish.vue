<template>
  <div>完結列表</div>
  <div v-for="(years, index) of finishList" :key="index">
    <ul v-for="season in years.data" :key="season.title">
      {{season.title}}
      <li v-for="animate in season.data" :key="animate.name">
        {{animate.name}}
      </li>
    </ul>
  </div>
</template>

<script>
import { onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { finishListAction, finishListState } from '../../variables/variablesMyself'

export default {
  name: 'Finish',
  setup () {
    const store = useStore()
    const finishList = computed(() => store.state.api[finishListState])
    onMounted(() => {
      store.dispatch(`api/${finishListAction}`)
    })
    return {
      finishList
    }
  }
}
</script>

<style scoped>

</style>
