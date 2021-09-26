<template>
    <div>我是搜尋</div>
    <button @click="updateFinishAnimateData">更新完結動漫資料</button>
</template>

<script>

import { sendSocketMessage } from '../../hooks/useWS'

export default {
  name: 'Search',
  setup () {
    const updateFinishAnimateData = () => {
      sendSocketMessage({
        action: 'myself_finish_animate_update'
      })
    }
    return {
      updateFinishAnimateData
    }
  }
}
</script>

<style scoped>

</style>
