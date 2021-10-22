<template>
  <div class="row">
    <div class="mb-3">
    <label for="exampleInputEmail1" class="form-label">搜尋動漫</label>
    <input type="email" class="form-control" id="exampleInputEmail1" @keyup="searchAnimate" v-model="searchText">
  </div>
  </div>
  <button type="button" class="btn btn-primary" :disabled="finishAnimateUpdate" @click="updateFinishAnimateData">
    {{ finishAnimateUpdateButton }}
  </button>
  <div class="row">
    <div class="col-2 col-sm-2" v-for="animate in displayFinishAnimate" :key="animate.id">
      <router-link :to="{
      name: 'MyselfAnimate',
      query: {
        url: animate.url.split('/').at(-1),
      }
    }">
        <figure class="figure">
          <img :src="animate.image" class="figure-img img-fluid rounded" alt="...">
          <figcaption class="figure-caption text-center">{{ animate.name}}</figcaption>
        </figure>
      </router-link>
    </div>
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
      searchAnimate
    }
  }
}
</script>

<style scoped>

</style>
