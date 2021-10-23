<template>
  <div>我的下載區域</div>

  <div v-for="animate in downloadMyselfAnimateArray" :key="animate.id">
    id:{{ animate.id }}
    動漫名字:{{ animate.animate_name }}
    級數:{{ animate.episode_name }}
    狀態:{{ animate.status }}
    <div class="progress">
      <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar"
           :aria-valuenow="computeProgressRate(animate.count, animate.ts_count)"
           aria-valuemin="0" aria-valuemax="100"
           :style="`width: ${computeProgressRate(animate.count, animate.ts_count)}%`">
        {{ computeProgressRate(animate.count, animate.ts_count) }}%
      </div>
    </div>
  </div>
</template>

<script>
import { useStore } from 'vuex'
import { downloadMyselfAnimateGetters } from '../variables/variablesMyself'
import { computed } from 'vue'

export default {
  name: 'MyDownload',
  setup: function () {
    const store = useStore()
    const downloadMyselfAnimateArray = computed(() => store.getters[`myself/${downloadMyselfAnimateGetters}`])

    function computeProgressRate (count, tsCount) {
      const result = parseInt(count / tsCount * 100)
      return !isNaN(result) ? result : 0
    }

    return {
      downloadMyselfAnimateArray,
      computeProgressRate
    }
  }
}
</script>

<style scoped>

</style>
