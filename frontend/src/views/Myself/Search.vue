<template>
  <div class="row">
    <input type="text" class="form-control shadow-sm p-3 mb-2 bg-body rounded" id="search" @keyup="searchAnimate"
           v-model="searchText" placeholder="搜尋動漫">
  </div>
  <button type="button" class="btn btn-primary mb-2" :disabled="finishAnimateUpdate" @click="updateFinishAnimateData">
    {{ finishAnimateUpdateButton }}
  </button>
  <div class="row justify-content-center">
    <transition-group appear name="animate__animated animate__bounce" enter-active-class="animate__fadeIn"
                      leave-active-class="animate__fadeOut">
      <div class="card col-sm-5 col-lg-3 col-xxl-2 mb-3 mx-3" v-for="animate in finishAnimate.data" :key="animate.id">
        <router-link :to="{
          name: 'MyselfAnimate',
          query: {
            url: animate.url.split('/').at(-1),
          }
        }">
          <img :src="animate.image" class="card-img-top rounded d-block img-thumbnail p-2 w-100"
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
<!--    <pagination v-if="finishAnimate.page && finishAnimate.data.length > 0" v-model="finishAnimate.page" :records="finishAnimate.count" :per-page="25" @paginate="myCallback"/>-->
    <nav aria-label="Page navigation example" v-show="showPagination">
      <ul class="pagination justify-content-center">
        <li class="page-item" :class="previousPage10" @click="changePage(finishAnimate.page - 10)">
          <a class="page-link" href="#">&lt;&lt;</a>
        </li>
        <li class="page-item" :class="previousPage" @click="changePage(finishAnimate.page - 1)">
          <a class="page-link" href="#">&lt;</a>
        </li>
        <li class="page-item">
          <a class="page-link" href="#">{{ finishAnimate.page }}</a>
        </li>
        <li class="page-item" :class="nextPage" @click="changePage(finishAnimate.page + 1)">
          <a class="page-link" href="#">&gt;</a>
        </li>
        <li class="page-item" :class="nextPage10" @click="changePage(finishAnimate.page + 10)">
          <a class="page-link" href="#">&gt;&gt;</a>
        </li>
      </ul>
      <p class="text-center">顯示 {{ pageMsg.startNum }} 到 {{ pageMsg.endNum }} 共 {{ finishAnimate.count }} 個動漫</p>
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
} from '../../variables/myself'
import { useStore } from 'vuex'

export default {
  name: 'Search',
  setup () {
    const searchText = ref('')
    const store = useStore()
    const finishAnimate = computed(() => store.state.myself[finishAnimateState])
    const previousPage = computed(() => finishAnimate.value.previous ? '' : 'disabled')
    const previousPage10 = computed(() => finishAnimate.value.total_pages > 10 && finishAnimate.value.page - 10 > 0 ? '' : 'disabled')
    const nextPage = computed(() => finishAnimate.value.next ? '' : 'disabled')
    const nextPage10 = computed(() => finishAnimate.value.total_pages > 10 && finishAnimate.value.total_pages - 10 > finishAnimate.value.page ? '' : 'disabled')
    const showPagination = computed(() => finishAnimate.value.data && finishAnimate.value.data.length)
    const finishAnimateUpdate = computed(() => store.state.myself[finishAnimateUpdateState])
    const finishAnimateUpdateButton = computed(() => store.state.myself[finishAnimateUpdateButtonState])
    const pageMsg = computed(() => {
      return {
        startNum: finishAnimate.value.page * 15 - 14,
        endNum: finishAnimate.value.count > finishAnimate.value.page * 15 ? finishAnimate.value.page * 15 : finishAnimate.value.count
      }
    })
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

    function myCallback (page) {
      console.log(page)
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
      previousPage10,
      nextPage,
      nextPage10,
      myCallback,
      pageMsg
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
