import axios from 'axios'
import { Fancybox } from '@fancyapps/ui/src/Fancybox'
import { app } from './main'
import { useNotificationStore } from '@dafcoe/vue-notification'
import { createToast, withProps } from 'mosha-vue-toastify'
import CustomToast from './components/CustomToast'

const { setNotification } = useNotificationStore()

export const axiosGet = (url, context, mutation) => {
  app.config.globalProperties.$Progress.start()
  axios.get(url).then(function (response) {
    context.commit(mutation, response.data)
    app.config.globalProperties.$Progress.finish()
  }).catch(function (_) {
    app.config.globalProperties.$Progress.fail()
    createToast(...toastData.apiFail)
    console.log(_)
  })
}

export const axiosPost = (url, data, context, mutation) => {
  app.config.globalProperties.$Progress.start()
  axios.post(url, data).then(function (response) {
    context.commit(mutation, response.data)
    app.config.globalProperties.$Progress.finish()
  }).catch(function (_) {
    // console.log(error.response)
    app.config.globalProperties.$Progress.fail()
    createToast(...toastData.apiFail)
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
    createToast(...toastData.apiFail)
  })
}

export const axiosDelete = (url, data, context, mutation) => {
  app.config.globalProperties.$Progress.start()
  // console.log('axiosDelete', JSON.stringify(data))
  axios.delete(url, { data: data.data }).then(function (response) {
    app.config.globalProperties.$Progress.finish()
    context.commit(mutation, data)
  }).catch(function (_) {
    // console.log(error.response)
    app.config.globalProperties.$Progress.fail()
    createToast(...toastData.apiFail)
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
  settingsPutOk: [withProps(CustomToast, { msg: '更新成功!' }), {
    position: 'top-center',
    transition: 'slide',
    showCloseButton: false,
    timeout: 2000
  }],
  searchMyselfAnimateFail: [withProps(CustomToast, { msg: '沒有搜尋動漫!' }), {
    position: 'top-center',
    transition: 'slide',
    showCloseButton: false,
    timeout: 3000
  }],
  downloadAnimateFinish: (data) => {
    return {
      message: `${data.animate_name}<br>${data.episode_name}下載完成!!`,
      type: 'info',
      automatically: false
    }
  },
  connectOk: [withProps(CustomToast, { msg: '歡迎' }), {
    position: 'top-center',
    transition: 'slide',
    showCloseButton: false,
    timeout: 2000
  }],
  downloadArrayCreateAnimate: (data) => {
    return {
      message: `下載清單新增<br>${data}!!`,
      type: 'success',
      automatically: true,
      duration: 3000
    }
  },
  apiFail: [withProps(CustomToast, { msg: '請求失敗了' }), {
    position: 'top-center',
    transition: 'slide',
    showCloseButton: false,
    timeout: 2000
  }],
  myselfFinishAnimateUpdate: [withProps(CustomToast, { msg: '開始更新完結動漫，請耐心稍等!!' }), {
    position: 'top-center',
    transition: 'slide',
    showCloseButton: false,
    timeout: 2000
  }],
  myselfFinishAnimateUpdateFinish: {
    message: '完結動漫已更新完畢!',
    type: 'info',
    automatically: false
  },
  clearDownloadArrayOk: [withProps(CustomToast, { msg: '清除所有已完成下載!' }), {
    position: 'top-center',
    transition: 'slide',
    showCloseButton: false,
    timeout: 2000
  }],
  deleteAnimateOk: [withProps(CustomToast, { msg: '已刪除所有選擇的動漫!' }), {
    position: 'top-center',
    transition: 'slide',
    showCloseButton: false,
    timeout: 2000
  }]
}
