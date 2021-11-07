<template>
  <a href="#">
    <BootstrapIcon class="pe-auto" icon="trash" size="2x"/>
  </a>
  <div class="table-responsive">
    <table class="table table-hover" style="word-wrap:break-word;word-break:break-all;white-space:normal;">
      <thead>
      <tr class="table">
        <th scope="col">
          <BootstrapIcon icon="square"/>
        </th>
        <th scope="col">動漫名字</th>
        <th scope="col">集數</th>
        <th scope="col">狀況</th>
        <th scope="col">下載進度</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="animate in downloadMyselfAnimateArray" :key="animate.id">
        {{animate}}
        <td style="width: 2%">
          <BootstrapIcon icon="square"/>
        </td>
        <td>{{ animate.animate_name }}</td>
        <td>{{ animate.episode_name }}</td>
        <td>{{ animate.status }}</td>
        <td>
          <div class="progress">
            <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar"
                 :aria-valuenow="computeProgressRate(animate.count, animate.ts_count)"
                 aria-valuemin="0" aria-valuemax="100"
                 :style="`width: ${computeProgressRate(animate.count, animate.ts_count)}%`">
              {{ computeProgressRate(animate.count, animate.ts_count) }}%
            </div>
          </div>
        </td>
      </tr>
      </tbody>
    </table>
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

<style lang="scss" scoped>
  .animate-name {
      text-overflow: ellipsis;
    }
</style>
