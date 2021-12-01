<template>
  <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
    <li class="nav-item" role="presentation">
      <button class="nav-link active" id="pills-system-tab" data-bs-toggle="pill" data-bs-target="#pills-system"
              type="button" role="tab" aria-controls="pills-system" aria-selected="true">系統
      </button>
    </li>
    <li class="nav-item" role="presentation">
      <button class="nav-link" id="pills-profile-tab" data-bs-toggle="pill" data-bs-target="#pills-profile"
              type="button" role="tab" aria-controls="pills-profile" aria-selected="false">動漫
      </button>
    </li>
  </ul>
  <div class="tab-content" id="pills-tabContent">
    <div class="tab-pane fade show active" id="pills-system" role="tabpanel" aria-labelledby="pills-system-tab">
      <table class="table table-hover">
    <thead>
    <tr class="table">
      <th scope="col">Action</th>
      <th scope="col">msg</th>
      <th scope="col">datetime</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="log in logs.data" :key="log.id">
      <td>{{ log.action }}</td>
      <td>{{ log.msg }}</td>
      <td>{{ log.datetime }}</td>
    </tr>
    </tbody>
  </table>
  <Pagination :pageDataObj="logs" :changePageFunction="changePage" :pageShowMsg="pageMsg"/>
    </div>
    <div class="tab-pane fade" id="pills-profile" role="tabpanel" aria-labelledby="pills-profile-tab">...</div>
  </div>
</template>

<script>
import { computed, reactive } from 'vue'
import { useStore } from 'vuex'
import { myHistoryAction, myHistoryState, myLogAction, myLogState } from '../variables/my'
import useWindowsFocus from '../hooks/useWindowsFocus'
import Pagination from '../components/Pagination'

export default {
  name: 'MyLog',
  components: { Pagination },
  setup () {
    const pageConfig = reactive({
      page: 1,
      size: 15
    })
    const store = useStore()
    const logs = computed(() => store.state.my[myLogState])
    const history = computed(() => store.state.my[myHistoryState])
    const pageMsg = computed(() => {
      const startMsgNum = logs.value.page * 15 - 14
      const endMsgNum = logs.value.count > logs.value.page * 15 ? logs.value.page * 15 : logs.value.count
      return `顯示 ${startMsgNum} 到 ${endMsgNum} 共 ${logs.value.count} 個訊息`
    })

    function changePage (page) {
      pageConfig.page = page
      store.dispatch(`my/${myLogAction}`, { page: page, size: pageConfig.size })
    }

    useWindowsFocus(store.dispatch, `my/${myLogAction}`, pageConfig)
    store.dispatch(`my/${myLogAction}`, { page: pageConfig.page, size: pageConfig.size })
    store.dispatch(`my/${myHistoryAction}`, { page: pageConfig.page, size: pageConfig.size })
    return {
      logs,
      pageMsg,
      changePage,
      history
    }
  }
}
</script>

<style scoped>
</style>
