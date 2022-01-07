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
  }).catch(function (error) {
    console.log(error.response)
    app.config.globalProperties.$Progress.fail()
    // alert(error.response.statusText)
  })
}

export const axiosPost = (url, data, context, mutation) => {
  app.config.globalProperties.$Progress.start()
  axios.post(url, data).then(function (response) {
    app.config.globalProperties.$Progress.finish()
    context.commit(mutation, response.data)
  }).catch(function (error) {
    console.log(error.response)
    app.config.globalProperties.$Progress.fail()
  })
}

export const startFancy = (video) => {
  Fancybox.show([
    {
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
