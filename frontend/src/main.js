import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import BootstrapIcon from '@dvuckovic/vue3-bootstrap-icons'
import VueProgressBar from '@aacassandra/vue3-progressbar'

const options = {
  color: '#478aff',
  failedColor: '#ff0000',
  thickness: '4px',
  transition: {
    speed: '0.2s',
    opacity: '0.6s',
    termination: 300
  },
  autoRevert: true,
  location: 'top',
  inverse: false
}
export const app = createApp(App).use(store).use(VueProgressBar, options).use(router)

app.component('BootstrapIcon', BootstrapIcon)
app.mount('#app')
