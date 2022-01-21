<template>
  <vue-table-lite
    :is-slot-mode="true"
    :is-static-mode="true"
    :columns="table.columns"
    :rows="table.rows"
    :total="table.totalRecordCount"
    :sortable="table.sortable"
  >
    <template v-slot:name="data">
      <Test :data="data"></Test>
    </template>
  </vue-table-lite>
</template>

<script>
import { useStore } from 'vuex'
import { computed, reactive } from 'vue'
import VueTableLite from 'vue3-table-lite'
import { animateListAction, animateListState } from '../../variables/anime1'
import Test from './TableSlot'

export default {
  name: 'AnimateList',
  components: { VueTableLite, Test },
  setup () {
    const store = useStore()
    store.dispatch(`anime1/${animateListAction}`)
    const animateList = computed(() => store.state.anime1[animateListState])
    const table = reactive({
      columns: [
        {
          label: '動漫名稱',
          field: 'name',
          width: '20%',
          sortable: true
          // isKey: true
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
      rows: computed(() => animateList.value),
      totalRecordCount: computed(() => {
        return table.rows.length
      }),
      sortable: {
        order: 'id',
        sort: 'asc'
      }
    })
    return {
      animateList,
      table
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
