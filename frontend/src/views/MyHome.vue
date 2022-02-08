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
        :id="doughnutChart.id"
        ref="chartRef"
        :type="doughnutChart.type"
        :data="doughnutChart.data"
        :options="doughnutChart.options"
    ></vue3-chart-js>

  </div>
  <button @click="updateChart">Update Chart</button>
</template>

<script>
import Vue3ChartJs from '@j-t-mcc/vue3-chartjs'
import { ref } from 'vue'

export default {
  name: 'MyHome',
  components: {
    Vue3ChartJs
  },
  setup () {
    const chartRef = ref(null)
    const doughnutChart = {
      id: 'doughnut',
      type: 'doughnut',
      data: {
        labels: ['剩餘空間', '使用空間'],
        datasets: [
          {
            color: '#666',
            backgroundColor: [
              '#00D8FF',
              '#DD1B16'
            ],
            data: [40, 20]
          }
        ]
      },
      options: {
        animation: false,
        plugins: {
          legend: {
            labels: {
              color: 'black'
            }
          }
        }
      }
    }

    const updateChart = () => {
      doughnutChart.data.datasets = [
        {
          backgroundColor: [
            '#00D8FF',
            '#DD1B16'
          ],
          data: [10, 20]
        }
      ]
      chartRef.value.update()
    }
    const beforeRenderLogic = (event) => {}
    return {
      doughnutChart,
      beforeRenderLogic,
      updateChart,
      chartRef
    }
  }
}
</script>

<style scoped>

</style>
