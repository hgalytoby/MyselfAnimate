<template>
  <div class="col-sm-4">
    <vue3-chart-js
      v-show="downloadBarChart.updated"
      :id="downloadBarChart.id"
      ref="DownloadRef"
      :type="downloadBarChart.type"
      :data="downloadBarChart.data"
      :options="downloadBarChart.options"
      :height="downloadBarChart.height"
    />
  </div>
</template>

<script>
import Vue3ChartJs from '@j-t-mcc/vue3-chartjs'
import { DownloadRef } from '../../hooks/useWS'
import { useStore } from 'vuex'
import { computed } from 'vue'
import { downloadBarChartState } from '../../variables/my'

export default {
  name: 'Download',
  components: {
    Vue3ChartJs
  },
  setup () {
    const store = useStore()
    const downloadBarChart = computed(() => store.state.my[downloadBarChartState])
    return {
      downloadBarChart,
      DownloadRef
    }
  }
}

</script>

<style scoped>

</style>
