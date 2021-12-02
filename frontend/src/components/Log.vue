<template>
  <div class="tab-pane fade" :class="typeData === 'system' ? 'show active' : ''" :id="`pills-${typeData}`"
       role="tabpanel" :aria-labelledby="`pills-${typeData}-tab`">
    <table class="table table-hover">
      <thead>
      <tr class="table">
        <th scope="col" v-for="(title, index) in table.title" :key="index">{{ title }}</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="items in logData.data" :key="items.id">
        <td v-for="(item, index) in table.item" :key="index">{{ items[item] }}</td>
      </tr>
      </tbody>
    </table>
    <Pagination :pageDataObj="logData" :changePageFunction="changePage" :pageShowMsg="pageMsg"/>
  </div>
</template>

<script>
import Pagination from './Pagination'
import { computed, reactive } from 'vue'
import { useStore } from 'vuex'
// import useWindowsFocus from '../hooks/useWindowsFocus'

export default {
  name: 'Log',
  components: { Pagination },
  props: {
    state: String,
    action: String,
    type: String,
    itemTable: Object
  },
  setup (props) {
    const pageConfig = reactive({
      page: 1,
      size: 15
    })
    const store = useStore()
    const logData = computed(() => store.state.my[props.state])
    const typeData = computed(() => props.type)
    const table = computed(() => props.itemTable)
    const storeAction = computed(() => props.action)
    const pageMsg = computed(() => {
      const startMsgNum = logData.value.page * 15 - 14
      const endMsgNum = logData.value.count > logData.value.page * 15 ? logData.value.page * 15 : logData.value.count
      return `顯示 ${startMsgNum} 到 ${endMsgNum} 共 ${logData.value.count} 個訊息`
    })

    function changePage (page) {
      pageConfig.page = page
      store.dispatch(storeAction.value, { page: page, size: pageConfig.size })
    }
    // useWindowsFocus(store.dispatch, storeAction.value)
    return {
      pageMsg,
      changePage,
      typeData,
      logData,
      table
    }
  }
}
</script>

<style scoped>

</style>
