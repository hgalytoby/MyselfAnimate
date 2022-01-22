<template>
  <nav aria-label="Page navigation example" v-show="showPagination">
    <ul class="pagination justify-content-center">
      <li class="page-item" :class="previousPage10">
        <a class="page-link" href="javascript:void(0)" @click="changePage(pageObj.page - 10)">&lt;&lt;</a>
      </li>
      <li class="page-item" :class="previousPage">
        <a class="page-link" href="javascript:void(0)" @click="changePage(pageObj.page - 1)">&lt;</a>
      </li>
      <li class="page-item" :class="nowPage(page)" v-for="page in pageObj.range" :key="page">
        <a class="page-link" href="javascript:void(0)" @click="changePage(page)">{{ page }}</a>
      </li>
      <li class="page-item" :class="nextPage">
        <a class="page-link" href="javascript:void(0)" @click="changePage(pageObj.page + 1)">&gt;</a>
      </li>
      <li class="page-item" :class="nextPage10">
        <a class="page-link" href="javascript:void(0)" @click="changePage(pageObj.page + 10)">&gt;&gt;</a>
      </li>
    </ul>
    <p class="text-center">{{ pageMsg }}</p>
    </nav>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'Pagination',
  props: {
    pageDataObj: Object,
    changePageFunction: Function,
    pageShowMsg: String
  },
  setup (props) {
    const pageObj = computed(() => props.pageDataObj)
    const pageMsg = computed(() => props.pageShowMsg)
    const previousPage = computed(() => !pageObj.value.previous ? '' : 'disabled')
    const previousPage10 = computed(() => pageObj.value.total_pages > 10 && pageObj.value.page - 10 > 0 ? '' : 'disabled')
    const nextPage = computed(() => pageObj.value.next ? '' : 'disabled')
    const nextPage10 = computed(() => pageObj.value.total_pages > 10 && pageObj.value.total_pages - 10 >= pageObj.value.page ? '' : 'disabled')
    const showPagination = computed(() => pageObj.value.data && pageObj.value.data.length)
    function nowPage (page) {
      return page === pageObj.value.page ? 'active' : ''
    }
    function changePage (page) {
      if (pageObj.value.page !== page) return props.changePageFunction(page)
    }
    return {
      pageObj,
      pageMsg,
      previousPage,
      previousPage10,
      nowPage,
      nextPage,
      nextPage10,
      showPagination,
      changePage
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
