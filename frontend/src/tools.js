import axios from 'axios'
import { Fancybox } from '@fancyapps/ui/src/Fancybox'

export const axiosGet = (url, context, mutation) => {
  axios.get(url).then(function (response) {
    context.commit(mutation, response.data)
  }).catch(function (error) {
    alert(error.msg)
  })
}

export const startFancy = (video) => {
  Fancybox.show([
    {
      src: video,
      type: 'iframe',
      preload: false
    }], {}) // starts fancybox with the gallery object
}
