<template>
  <div class="col-sm-8">
  <vue3-chart-js
    :id="barChart.id"
    :type="barChart.type"
    :data="barChart.data"
    :options="barChart.options"
  />
  </div>
</template>

<script>
import Vue3ChartJs from '@j-t-mcc/vue3-chartjs'

export default {
  name: 'Download',
  components: {
    Vue3ChartJs
  },
  setup () {
    const barChart = {
      type: 'bar',
      options: {
        min: 0,
        max: 100,
        responsive: true,
        plugins: {
          legend: {
            position: 'top'
          },
          title: {
            font: {
              size: 24
            },
            color: 'black',
            display: true,
            text: '下載數量'
          }
        },
        scales: {
          y: {
            min: 0,
            max: 100,
            ticks: {
              callback: function (value) {
                return `${value}`
              }
            }
          }
        }
      },
      data: {
        labels: ['VueJs'],
        datasets: [
          {
            label: 'Myself',
            backgroundColor: ['rgba(252,137,63,0.8)'],
            data: [10]
          },
          {
            label: 'Anime1',
            backgroundColor: ['rgba(255,25,25,0.8)'],
            data: [30]
          }
        ]
      }
    }
    return {
      barChart
    }
  }
}

</script>

<style scoped>

</style>
