<template>
  <input type="text" class="form-control shadow-sm p-3 mb-2 bg-body rounded" id="search"
       v-model="searchTerm" title="搜尋動漫" placeholder="搜尋動漫">
  <vue-table-lite
    :is-slot-mode="true"
    :is-static-mode="true"
    :columns="table.columns"
    :rows="table.rows"
    :total="table.totalRecordCount"
    :sortable="table.sortable"
    :messages="table.messages"
    :page-size="table.pageSize"
  >
    <template v-slot:name="data">
      <Test :data="data"></Test>
    </template>
  </vue-table-lite>
</template>

<script>
import { useStore } from 'vuex'
import { computed, reactive, ref } from 'vue'
import VueTableLite from 'vue3-table-lite'
import { animateListAction, animateListState } from '../../variables/anime1'
import Test from './TableSlot'
import useWindowsFocus from '../../hooks/useWindowsFocus'

export default {
  name: 'AnimateList',
  components: { VueTableLite, Test },
  setup () {
    const store = useStore()
    const searchTerm = ref('')
    store.dispatch(`anime1/${animateListAction}`)
    const animateList = computed(() => store.state.anime1[animateListState])
    const table = reactive({
      columns: [
        {
          label: '動漫名稱',
          field: 'name',
          width: '20%',
          sortable: true,
          isKey: true
        },
        {
          label: '集數',
          field: 'episode',
          width: '7%',
          sortable: true
        },
        {
          label: '年份',
          field: 'years',
          width: '8%',
          sortable: true
        },
        {
          label: '季節',
          field: 'season',
          width: '6%',
          sortable: true
        },
        {
          label: '字幕組',
          field: 'subtitle_group',
          width: '8%',
          sortable: true
        }
      ],
      rows: computed(() => {
        return computed(() => animateList.value).value.filter(
          (x) =>
            x.name.toLowerCase().includes(searchTerm.value.toLowerCase())
        )
      }),
      pageSize: 10,
      totalRecordCount: computed(() => {
        return table.rows.length
      }),
      sortable: {
        order: 'id',
        sort: 'asc'
      },
      messages: {
        pagingInfo: '現在顯示 {0} 到 {1}筆 共{2}筆',
        pageSizeChangeLabel: '每頁筆數:',
        gotoPageLabel: '現在頁數:',
        noDataAvailable: '沒有資料'
      }
    })
    useWindowsFocus(store.dispatch, `anime1/${animateListAction}`)
    return {
      animateList,
      searchTerm,
      table
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
