<template>
    <ul class="nav nav-pills mb-3" id="pills-tab2" role="tablist">
      <li class="nav-item" role="presentation">
        <button class="nav-link active" id="pills-system-tab" data-bs-toggle="pill" data-bs-target="#pills-system"
                type="button" role="tab" aria-controls="pills-system">系統
        </button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link" id="pills-history-tab" data-bs-toggle="pill" data-bs-target="#pills-history"
                type="button" role="tab" aria-controls="pills-history">動漫
        </button>
      </li>
    </ul>
  <transition appear name="animate__animated animate__bounce" enter-active-class="animate__fadeIn"
              leave-active-class="animate__fadeOut">
    <div class="tab-content" id="pills-tabContent">
      <Log :state="systemState" :action="`my/${systemAction}`" type="system" :itemTable="systemTable"/>
      <Log :state="historyState" :action="`my/${historyAction}`" type="history" :itemTable="historyTable"/>
    </div>
  </transition>
</template>

<script>
import { useStore } from 'vuex'
import {
  logAction,
  systemAction,
  systemState,
  systemTable,
  historyAction,
  historyState,
  historyTable
} from '../variables/my'
import Log from '../components/Log'

export default {
  name: 'MyLog',
  components: { Log },
  setup () {
    const store = useStore()
    store.dispatch(`my/${logAction}`)
    return {
      systemAction,
      systemState,
      systemTable,
      historyAction,
      historyState,
      historyTable
    }
  }
}
</script>

<style scoped>
</style>
