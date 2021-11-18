import axios from 'axios'
import { Fancybox } from '@fancyapps/ui/src/Fancybox'

export const axiosGet = (url, context, mutation) => {
  axios.get(url).then(function (response) {
    context.commit(mutation, response.data)
  }).catch(function (error) {
    // console.log(error.response)
    alert(error.response.statusText)
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
