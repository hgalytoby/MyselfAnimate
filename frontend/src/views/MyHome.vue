<template>
  <h1>還不知道要放什麼的首頁</h1>
  <h2>webSocket</h2>
  <h4>action: {{ $store.state.ws.wsClick.action }}</h4>
  <h4>msg: {{ $store.state.ws.wsClick.msg }}</h4>
  <div><a href="https://github.com/dafcoe/vue-notification">notification/toast</a></div>
  <div><a href="https://github.com/aacassandra/vue3-progressbar">Progressbar</a></div>
  <div><a href="https://github.com/dvuckovic/vue3-bootstrap-icons">bootstrap-icons</a></div>
  <div><a href="https://github.com/szboynono/mosha-vue-toastify">Mosha Vue Toastify</a></div>
  <div>學習與研究!</div>
  <div>應在24小時內刪除影片。</div>
  <vue-table-lite
    :is-static-mode="true"
    :columns="table.columns"
    :rows="table.rows"
    :total="table.totalRecordCount"
    :sortable="table.sortable"
  ></vue-table-lite>
</template>

<script>
import VueTableLite from 'vue3-table-lite'
import { computed, reactive } from 'vue'

export default {
  name: 'MyHome',
  components: { VueTableLite },
  setup () {
    const data = reactive([])
    for (let i = 0; i < 126; i++) {
      data.push({
        id: i,
        name: 'TEST' + i,
        email: 'test' + i + '@example.com'
      })
    }
    const table = reactive({
      columns: [
        {
          label: 'ID',
          field: 'id',
          width: '3%',
          sortable: true,
          isKey: true
        },
        {
          label: 'Name',
          field: 'name',
          width: '10%',
          sortable: true
        },
        {
          label: 'Email',
          field: 'email',
          width: '15%',
          sortable: true
        }
      ],
      rows: data,
      totalRecordCount: computed(() => {
        return table.rows.length
      }),
      sortable: {
        order: 'id',
        sort: 'asc'
      }
    })
    return {
      table
    }
  }
}
</script>

<style scoped>

</style>
