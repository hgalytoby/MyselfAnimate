import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import BootstrapIcon from '@dvuckovic/vue3-bootstrap-icons'
import Pagination from 'v-pagination-3'
const app = createApp(App).use(store).use(router)

app.component('BootstrapIcon', BootstrapIcon)
app.component('pagination', Pagination)
app.mount('#app')
