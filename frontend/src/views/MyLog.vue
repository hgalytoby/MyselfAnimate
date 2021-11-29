<template>
  我是Log
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
</template>

<script>
import { onMounted, computed, reactive } from 'vue'
import { useStore } from 'vuex'
import { myLogAction, myLogState } from '../variables/my'
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
    const pageMsg = computed(() => {
      const startMsgNum = logs.value.page * 15 - 14
      const endMsgNum = logs.value.count > logs.value.page * 15 ? logs.value.page * 15 : logs.value.count
      return `顯示 ${startMsgNum} 到 ${endMsgNum} 共 ${logs.value.count} 個訊息`
    })
    function changePage (page) {
      store.dispatch(`my/${myLogAction}`, { page: page, size: pageConfig.size })
    }
    useWindowsFocus(store.dispatch, `my/${myLogAction}`)
    onMounted(() => {
      store.dispatch(`my/${myLogAction}`, { page: pageConfig.page, size: pageConfig.size })
    })
    return {
      logs,
      pageMsg,
      changePage
    }
  }
}
</script>

<style scoped>
</style>
