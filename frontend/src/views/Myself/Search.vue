<template>
  <div class="row">
    <div class="mb-3">
      <input type="text" class="form-control shadow-sm p-3 mb-5 bg-body rounded" id="search" @keyup="searchAnimate"
             v-model="searchText" placeholder="搜尋動漫">
    </div>
  </div>
  <button type="button" class="btn btn-primary" :disabled="finishAnimateUpdate" @click="updateFinishAnimateData">
    {{ finishAnimateUpdateButton }}
  </button>
  <div class="row">
    <transition-group appear name="animate__animated animate__bounce" enter-active-class="animate__fadeIn"
                      leave-active-class="animate__fadeOut">
      <div class="card col-sm-5 col-lg-3 col-xxl-2" v-for="animate in finishAnimate.data" :key="animate.id">
        <router-link :to="{
          name: 'MyselfAnimate',
          query: {
            url: animate.url.split('/').at(-1),
          }
        }">
          <img :src="animate.image" class="card-img-top rounded mx-auto d-block img-thumbnail p-2 w-100"
               alt="animate.name">
          <div class="card-body">
            <p class="card-title text-center text-white p-bg">{{ animate.info }}</p>
            <p class="card-text overflow-hidden text-nowrap animate-name text-center" data-toggle="tooltip"
             data-placement="bottom"
             :title="animate.name">{{ animate.name }}</p>
          </div>
        </router-link>
      </div>
    </transition-group>
  </div>
  <transition appear name="animate__animated animate__bounce" enter-active-class="animate__fadeIn"
              leave-active-class="animate__fadeOut">
    <nav aria-label="Page navigation example" v-show="showPagination">
    <ul class="pagination justify-content-center">
      <li class="page-item" :class="previousPage" @click="changePage(finishAnimate.page - 1)">
        <a class="page-link" href="#">Previous</a>
      </li>
      <li class="page-item"><a class="page-link" href="#">{{ finishAnimate.page }}</a></li>
      <li class="page-item" :class="nextPage" @click="changePage(finishAnimate.page + 1)">
        <a class="page-link" href="#">next</a>
      </li>
    </ul>
    <p class="text-center">全部:{{ finishAnimate.count }} / 總頁數:{{ finishAnimate.total_pages }}</p>
  </nav>
  </transition>
</template>

<script>
import { sendSocketMessage } from '../../hooks/useWS'
import { computed, onMounted, ref } from 'vue'
import {
  finishAnimateAction, finishAnimateState,
  finishAnimateUpdateButtonState,
  finishAnimateUpdateState
} from '../../variables/variablesMyself'
import { useStore } from 'vuex'

export default {
  name: 'Search',
  setup () {
    const searchText = ref('')
    const store = useStore()
    const finishAnimate = computed(() => store.state.myself[finishAnimateState])
    const previousPage = computed(() => finishAnimate.value.previous ? '' : 'disabled')
    const nextPage = computed(() => finishAnimate.value.next ? '' : 'disabled')
    const showPagination = computed(() => finishAnimate.value.data && finishAnimate.value.data.length)
    const finishAnimateUpdate = computed(() => store.state.myself[finishAnimateUpdateState])
    const finishAnimateUpdateButton = computed(() => store.state.myself[finishAnimateUpdateButtonState])
    const updateFinishAnimateData = () => {
      sendSocketMessage({
        action: 'myself_finish_animate_update'
      })
    }
    onMounted(() => {
      store.dispatch(`myself/${finishAnimateAction}`)
    })
    const searchAnimate = () => {
      sendSocketMessage({
        action: 'search_myself_animate',
        msg: searchText.value
      })
    }
    function changePage (page) {
      console.log('changePage')
      sendSocketMessage({
        action: 'search_myself_animate',
        msg: searchText.value,
        page: page
      })
    }
    return {
      updateFinishAnimateData,
      finishAnimateUpdate,
      finishAnimateUpdateButton,
      finishAnimate,
      searchText,
      searchAnimate,
      changePage,
      showPagination,
      previousPage,
      nextPage
    }
  }
}
</script>

<style scoped>
  .animate-name {
    text-overflow: ellipsis;
  }
  .p-bg {
    background: rgba(0, 0, 0, 0.6);
  }
</style>
