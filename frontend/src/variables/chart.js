export const storageDoughnutChartObj = {
  id: 'storage-chart',
  type: 'doughnut',
  updated: false,
  data: {
    labels: ['硬碟剩餘空間(GB)', '硬碟使用空間(GB)'],
    datasets: [
      {
        backgroundColor: [
          'rgba(0,216,255,0.8)',
          'rgba(221,27,22,0.8)'
        ],
        data: []
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
      // title: {
      //   font: {
      //     size: 24
      //   },
      //   color: 'black',
      //   display: true,
      //   text: '硬碟剩餘空間(GB)'
      // }
    }
  }
}

export const downloadChartObj = {
  id: 'download-chart',
  type: 'bar',
  height: 300,
  updated: false,
  options: {
    responsive: true,
    animation: false,
    plugins: {
      legend: {
        position: 'top'
      }
    },
    scales: {
      y: {
        min: 0,
        max: 0,
        ticks: {
          callback: function (value) {
            return `${value}`
          }
        }
      }
    }
  },
  data: {
    labels: ['下載數量'],
    datasets: [
      {
        label: 'Myself',
        backgroundColor: ['rgba(252,137,63,0.8)'],
        data: [1]
      },
      {
        label: 'Anime1',
        backgroundColor: ['rgba(255,25,25,0.8)'],
        data: [1]
      },
      {
        label: 'Total',
        backgroundColor: ['rgba(108,243,153,0.8)'],
        data: [2]
      }
    ]
  }
}
