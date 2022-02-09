export const logState = 'logState'
export const systemState = 'systemState'
export const settingsState = 'settingsState'
export const historyState = 'historyState'
export const downloadCheckBoxState = 'downloadCheckBoxState'
export const animateCollectState = 'animateCollectState'
export const storageDoughnutChartState = 'storageDoughnutChartState'

export const logAction = 'logAction'
export const systemAction = 'systemAction'
export const settingsGetAction = 'settingsGetAction'
export const settingsPutAction = 'settingsPutAction'
export const settingsUpdateDownloadValueAction = 'settingsUpdateDownloadValueAction'
export const historyAction = 'historyAction'
export const animateCollectAction = 'animateCollectAction'
export const destroyManyAnimateAction = 'destroyManyAnimateAction'

export const logMutation = 'logMutation'
export const systemMutation = 'systemMutation'
export const settingsGetMutation = 'settingsGetMutation'
export const settingsPutMutation = 'settingsPutMutation'
export const settingsUpdateDownloadValueMutation = 'settingsUpdateDownloadValueMutation'
export const historyMutation = 'historyMutation'
export const downloadCheckBoxMutation = 'downloadCheckBoxMutation'
export const clickDownloadCheckBoxMutation = 'clickDownloadCheckBoxMutation'
export const clickAllDownloadCheckBoxMutation = 'clickAllDownloadCheckBoxMutation'
export const animateCollectMutation = 'animateCollectMutation'
export const destroyManyAnimateMutation = 'destroyManyAnimateMutation'
export const storageDoughnutChartMutation = 'storageDoughnutChartMutation'

export const systemTable = {
  title: ['操作', '訊息', '時間'],
  item: ['action', 'msg', 'datetime']
}

export const historyTable = {
  title: ['動漫網站', '動漫名字', '集數', '下載時間'],
  item: ['animate_website_name', 'animate_name', 'episode_name', 'download_date']
}

export const storageDoughnutChartObj = {
  id: 'storage',
  type: 'doughnut',
  data: {
    labels: ['剩餘空間', '使用空間'],
    datasets: [
      {
        backgroundColor: [
          '#00D8FF',
          '#DD1B16'
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
      },
      title: {
        font: {
          size: 24
        },
        color: 'black',
        display: true,
        text: '硬碟剩餘空間(GB)'
      }
    }
  }
}
