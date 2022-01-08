import axios from 'axios'
import { Fancybox } from '@fancyapps/ui/src/Fancybox'
import { app } from './main'
import { useNotificationStore } from '@dafcoe/vue-notification'

const { setNotification } = useNotificationStore()

export const axiosGet = (url, context, mutation) => {
  app.config.globalProperties.$Progress.start()
  axios.get(url).then(function (response) {
    app.config.globalProperties.$Progress.finish()
    context.commit(mutation, response.data)
  }).catch(function (_) {
    // console.log(error.response)
    app.config.globalProperties.$Progress.fail()
    setToast(toastData.apiFail)
    // alert(error.response.statusText)
  })
}

export const axiosPost = (url, data, context, mutation) => {
  app.config.globalProperties.$Progress.start()
  axios.post(url, data).then(function (response) {
    app.config.globalProperties.$Progress.finish()
    context.commit(mutation, response.data)
  }).catch(function (_) {
    // console.log(error.response)
    app.config.globalProperties.$Progress.fail()
    setToast(toastData.apiFail)
  })
}

export const axiosPut = (url, data, context, mutation) => {
  app.config.globalProperties.$Progress.start()
  axios.put(url, data).then(function (response) {
    app.config.globalProperties.$Progress.finish()
    context.commit(mutation, response.data)
  }).catch(function (_) {
    // console.log(error.response)
    app.config.globalProperties.$Progress.fail()
    setToast(toastData.apiFail)
  })
}

export const startFancy = (video) => {
  Fancybox.show([{
    src: video,
    type: 'iframe',
    preload: false
  }], {})
}

export const setToast = (data) => {
  setNotification({
    message: data.message,
    type: data.type,
    showIcon: true,
    dismiss: {
      manually: true,
      automatically: data.automatically
    },
    showDurationProgress: true,
    appearance: 'light',
    duration: data.duration
  })
}

export const toastData = {
  settingsPutOk: {
    message: '更新成功!',
    type: 'success',
    automatically: true,
    duration: 3000
  },
  searchMyselfAnimateFail: {
    message: '沒有搜尋動漫',
    type: 'alert',
    automatically: true,
    duration: 3000
  },
  downloadAnimateFinish: (data) => {
    return {
      message: `${data.animate_name}<br>${data.episode_name}下載完成!!`,
      type: 'info',
      automatically: false
    }
  },
  connectOk: {
    message: '歡迎~',
    type: 'success',
    automatically: true,
    duration: 3000
  },
  downloadArrayCreateAnimate: (data) => {
    return {
      message: `下載清單新增<br>${data}!!`,
      type: 'success',
      automatically: true,
      duration: 3000
    }
  },
  apiFail: {
    message: '請求失敗了',
    type: 'alert',
    automatically: true,
    duration: 3000
  },
  myselfFinishAnimateUpdate: {
    message: '更新完結動漫，請耐心稍等!!',
    type: 'info',
    automatically: true,
    duration: 5000
  },
  clearDownloadArrayOk: {
    message: '清除所有已完成下載!',
    type: 'success',
    automatically: true,
    duration: 3000
  },
  deleteAnimateOk: {
    message: '已刪除所有選擇的動漫!',
    type: 'success',
    automatically: true,
    duration: 3000
  }
}
