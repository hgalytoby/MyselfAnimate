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
    <template v-for="animate in displayFinishAnimate.data" :key="animate.id">
    <transition appear name="animate__animated animate__bounce" enter-active-class="animate__backInDown"
                      leave-active-class="animate__heartBeat">
      <div class="card col-sm-5 col-lg-3 col-xxl-2">
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
    </transition>
    </template>
  </div>
  <nav aria-label="Page navigation example">
    <ul class="pagination justify-content-center">
      <li class="page-item" :class="displayFinishAnimate.previous ? '' : 'disabled'" @click="changePage(displayFinishAnimate.page - 1)">
        <a class="page-link">Previous</a>
      </li>
      <li class="page-item"><a class="page-link" href="#">{{ displayFinishAnimate.page }}</a></li>
      <li class="page-item" :class="displayFinishAnimate.next ? '' : 'disabled'" @click="changePage(displayFinishAnimate.page + 1)">
        <a class="page-link">next</a>
      </li>
    </ul>
    <p class="text-center">全部:{{ displayFinishAnimate.count }} / 總頁數:{{ displayFinishAnimate.total_pages }}</p>
  </nav>
</template>

<script>
import { sendSocketMessage } from '../../hooks/useWS'
import { computed, onMounted, ref } from 'vue'
import {
  displayFinishAnimateMutation,
  displayFinishAnimateState,
  finishAnimateAction,
  finishAnimateUpdateButtonState,
  finishAnimateUpdateState
} from '../../variables/variablesMyself'
import { useStore } from 'vuex'

export default {
  name: 'Search',
  setup () {
    const show = ref(true)
    const searchText = ref('')
    const store = useStore()
    const displayFinishAnimate = computed(() => store.state.myself[displayFinishAnimateState])
    const updateFinishAnimateData = () => {
      sendSocketMessage({
        action: 'myself_finish_animate_update'
      })
    }
    onMounted(() => {
      store.dispatch(`myself/${finishAnimateAction}`)
    })
    const finishAnimateUpdate = computed(() => store.state.myself[finishAnimateUpdateState])
    const finishAnimateUpdateButton = computed(() => store.state.myself[finishAnimateUpdateButtonState])
    const searchAnimate = () => {
      if (searchText.value) {
        sendSocketMessage({
          action: 'search_myself_animate',
          msg: searchText.value
        })
      } else {
        store.commit(`myself/${displayFinishAnimateMutation}`)
      }
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
      displayFinishAnimate,
      searchText,
      searchAnimate,
      changePage,
      show
    }
  }
}
</script>

<style scoped>
  .animate-name {
    text-overflow: ellipsis;
  }

  .p-main {
    display: block;
    max-width: 265px;
    width: 100%;
    height: 225px;
    position: relative;
  }

  .p-test {
    position: absolute;
    z-index: 1;
    bottom: 0;
    left: 0;
    width: 100%;
  }

  .p-bg {
    background: rgba(0, 0, 0, 0.6);
  }
</style>
