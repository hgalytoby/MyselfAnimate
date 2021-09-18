import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import BootstrapIcon from '@dvuckovic/vue3-bootstrap-icons'

const app = createApp(App).use(store).use(router)

app.component('BootstrapIcon', BootstrapIcon)

app.mount('#app')
