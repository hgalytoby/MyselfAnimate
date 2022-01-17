<template>
  <div class="row">
    <input type="text" class="form-control shadow-sm p-3 mb-2 bg-body rounded" id="search" @keyup="searchAnimate"
           v-model="searchText" placeholder="搜尋動漫">
  </div>
  <div class="row align-items-center">
    <button type="button" class="btn btn-primary mb-2 col-auto" :disabled="finishAnimateUpdate"
            @click="updateFinishAnimateData">
      {{ finishAnimateUpdateButton }}
    </button>
    <h6 class="col-auto">最後更新時間: {{ !settings.myself_finish_animate_date ? '尚未更新' : settings.myself_finish_animate_date
      }}</h6>
  </div>

  <div class="row justify-content-center">
    <transition-group appear name="animate__animated animate__bounce" enter-active-class="animate__fadeIn"
                      leave-active-class="animate__fadeOut">
      <div class="card bg-transparent col-sm-5 col-lg-3 col-xxl-2 mb-3 mx-3" v-for="animate in finishAnimate.data"
           :key="animate.id">
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
    <Pagination :page-data-obj="finishAnimate" :change-page-function="changePage" :page-show-msg="pageMsg"/>
  </transition>
</template>

<script>
import { sendSocketMessage } from '../../hooks/useWS'
import { computed, ref } from 'vue'
import {
  finishAnimateAction, finishAnimateInitMutation, finishAnimateState,
  finishAnimateUpdateButtonState,
  finishAnimateUpdateState
} from '../../variables/myself'
import { useStore } from 'vuex'
import Pagination from '../../components/Pagination'
import { settingsGetAction, settingsState } from '../../variables/my'

export default {
  name: 'Search',
  components: { Pagination },
  setup () {
    const searchText = ref('')
    const store = useStore()
    const finishAnimate = computed(() => store.state.myself[finishAnimateState])
    const finishAnimateUpdate = computed(() => store.state.myself[finishAnimateUpdateState])
    const finishAnimateUpdateButton = computed(() => store.state.myself[finishAnimateUpdateButtonState])
    const pageMsg = computed(() => {
      const startMsgNum = finishAnimate.value.page * 15 - 14
      const endMsgNum = finishAnimate.value.count > finishAnimate.value.page * 15 ? finishAnimate.value.page * 15 : finishAnimate.value.count
      return `顯示 ${startMsgNum} 到 ${endMsgNum} 共 ${finishAnimate.value.count} 個動漫`
    })
    const settings = computed(() => store.state.my[settingsState])
    store.dispatch(`myself/${finishAnimateAction}`)
    store.dispatch(`my/${settingsGetAction}`)
    const updateFinishAnimateData = () => {
      const date = new Date()
      sendSocketMessage({
        action: 'myself_finish_animate_update',
        data: {
          ...settings.value,
          myself_finish_animate_date: date.toISOString().slice(0, 10) + ' ' + date.toTimeString().slice(0, 8),
          myself_finish_animate_update: true
        }
      })
      store.commit(`myself/${finishAnimateInitMutation}`)
    }
    const searchAnimate = () => {
      sendSocketMessage({
        action: 'search_myself_animate',
        msg: searchText.value
      })
    }

    function changePage (page) {
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
      pageMsg,
      settings
    }
  }
}
</script>

<style lang="scss" scoped>
  .animate-name {
    text-overflow: ellipsis;
  }

  .p-bg {
    background: rgba(0, 0, 0, 0.6);
  }
</style>
