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
    <transition-group mode="out-in" appear name="animate__animated animate__bounce" enter-active-class="animate__fadeIn"
                      leave-active-class="animate__fadeOut">
      <div class="card col-sm-5 col-lg-3 col-xxl-2" v-for="animate in displayFinishAnimate"
           :key="animate.id">
        <router-link :to="{
          name: 'MyselfAnimate',
          query: {
            url: animate.url.split('/').at(-1),
          }
        }">
          <img :src="animate.image" class="card-img-top rounded mx-auto d-block img-thumbnail p-2" alt="animate.name">
<!--          <span class="bg-dark text-white text-center position-relative bottom-50">{{ animate.info }}</span>-->
          <div class="card-img-overlay">
            <p class="bg-dark position-relative top-50 start-50 translate-middle-x text-white text-center">{{animate.info}}</p>
          </div>
        </router-link>
        <div class="card-body">
          <p class="card-text overflow-hidden text-nowrap animate-name text-center" data-toggle="tooltip" data-placement="bottom"
               :title="animate.name">{{ animate.name }}</p>
          </div>
        <div class="h-auto d-inline-block">
        </div>
      </div>
    </transition-group>
  </div>
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
    const searchText = ref('')
    const show = ref(true)
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
    return {
      updateFinishAnimateData,
      finishAnimateUpdate,
      finishAnimateUpdateButton,
      displayFinishAnimate,
      searchText,
      searchAnimate,
      show
    }
  }
}
</script>

<style scoped>
  .animate-name {
    text-overflow: ellipsis;
  }
</style>
