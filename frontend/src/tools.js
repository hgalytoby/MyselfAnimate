import axios from 'axios'
import { Fancybox } from '@fancyapps/ui/src/Fancybox'
import { app } from './main'

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

export const startFancy = (video) => {
  Fancybox.show([
    {
      src: video,
      type: 'iframe',
      preload: false
    }], {})
}
