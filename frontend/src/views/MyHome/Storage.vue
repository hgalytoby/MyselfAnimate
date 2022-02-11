<template>
  <div class="col-sm-4">
    <vue3-chart-js
      v-show="storageDoughnutChart.updated"
      :id="storageDoughnutChart.id"
      ref="storageRef"
      :type="storageDoughnutChart.type"
      :data="storageDoughnutChart.data"
      :options="storageDoughnutChart.options"
    />
  </div>
</template>

<script>
import Vue3ChartJs from '@j-t-mcc/vue3-chartjs'
import { useStore } from 'vuex'
import { computed } from 'vue'
import { storageDoughnutChartState } from '../../variables/my'
import { storageRef } from '../../hooks/useWS'

export default {
  name: 'Storage',
  components: {
    Vue3ChartJs
  },
  setup () {
    const store = useStore()
    const storageDoughnutChart = computed(() => store.state.my[storageDoughnutChartState])
    return {
      storageDoughnutChart,
      storageRef
    }
  }
}
</script>

<style scoped>

</style>
