<template>
  <div class="fs-4">您好</div>
  <div class="p-4"></div>
  <div class="fs-4">websocket
    <div class="fs-4">action: {{ $store.state.ws.wsClick.action }}</div>
    <div class="fs-4">msg: {{ $store.state.ws.wsClick.msg }}</div>
  </div>
  <div class="p-4"></div>
  <div>
    <div class="fs-4">用的套件如下</div>
    <div><a href="https://github.com/dafcoe/vue-notification">notification/toast</a></div>
    <div><a href="https://github.com/aacassandra/vue3-progressbar">Progressbar</a></div>
    <div><a href="https://github.com/dvuckovic/vue3-bootstrap-icons">bootstrap-icons</a></div>
    <div><a href="https://github.com/szboynono/mosha-vue-toastify">Mosha Vue Toastify</a></div>
    <div><a href="https://github.com/linmasahiro/vue3-table-lite">vue3-table-lite</a></div>
  </div>
  <div class="p-4"></div>
  <div>
    <div class="fs-4">學習與研究!</div>
    <div class="fs-4">應在24小時內刪除影片。</div>
  </div>
  <div style="height:600px;width: 600px;display: flex;flex-direction:column;">
    <vue3-chart-js
        v-show="storageDoughnutChart.data.datasets[0].data.length > 0"
        :id="storageDoughnutChart.id"
        ref="storageRef"
        :type="storageDoughnutChart.type"
        :data="storageDoughnutChart.data"
        :options="storageDoughnutChart.options"
    ></vue3-chart-js>
  </div>
</template>

<script>
import Vue3ChartJs from '@j-t-mcc/vue3-chartjs'
import { computed } from 'vue'
import { useStore } from 'vuex'
import { storageDoughnutChartState } from '../variables/my'
import { storageRef } from '../hooks/useWS'

export default {
  name: 'MyHome',
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
