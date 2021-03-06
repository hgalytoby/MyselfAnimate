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
  settingsPutOk: [withProps(CustomToast, { msg: '????????????!' }), {
    position: 'top-center',
    transition: 'slide',
    showCloseButton: false,
    timeout: 2000
  }],
  searchMyselfAnimateFail: [withProps(CustomToast, { msg: '??????????????????!' }), {
    position: 'top-center',
    transition: 'slide',
    showCloseButton: false,
    timeout: 3000
  }],
  downloadAnimateFinish: (data) => {
    return {
      message: `${data.animate_name}<br>${data.episode_name}????????????!!`,
      type: 'info',
      automatically: false
    }
  },
  connectOk: [withProps(CustomToast, { msg: '??????' }), {
    position: 'top-center',
    transition: 'slide',
    showCloseButton: false,
    timeout: 2000
  }],
  downloadArrayCreateAnimate: (data) => {
    return {
      message: `??????????????????<br>${data}!!`,
      type: 'success',
      automatically: true,
      duration: 3000
    }
  },
  apiFail: [withProps(CustomToast, { msg: '???????????????' }), {
    position: 'top-center',
    transition: 'slide',
    showCloseButton: false,
    timeout: 2000
  }],
  myselfFinishAnimateUpdate: [withProps(CustomToast, { msg: '??????????????????????????????????????????!!' }), {
    position: 'top-center',
    transition: 'slide',
    showCloseButton: false,
    timeout: 2000
  }],
  myselfFinishAnimateUpdateFinish: {
    message: '???????????????????????????!',
    type: 'info',
    automatically: false
  },
  clearDownloadArrayOk: [withProps(CustomToast, { msg: '???????????????????????????!' }), {
    position: 'top-center',
    transition: 'slide',
    showCloseButton: false,
    timeout: 2000
  }],
  deleteAnimateOk: [withProps(CustomToast, { msg: '??????????????????????????????!' }), {
    position: 'top-center',
    transition: 'slide',
    showCloseButton: false,
    timeout: 2000
  }]
}
