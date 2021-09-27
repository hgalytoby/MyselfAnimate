<template>
  <div>我是搜尋</div>
  <button type="button" class="btn btn-primary" :disabled="finishAnimateUpdate" @click="updateFinishAnimateData">
    {{ finishAnimateUpdateButton }}
  </button>
</template>

<script>
import { sendSocketMessage } from '../../hooks/useWS'
import { computed } from 'vue'
import {
  finishAnimateUpdateButtonState,
  finishAnimateUpdateState
} from '../../variables/variablesMyself'
import { useStore } from 'vuex'

export default {
  name: 'Search',
  setup () {
    const store = useStore()
    const updateFinishAnimateData = () => {
      sendSocketMessage({
        action: 'myself_finish_animate_update'
      })
    }
    const finishAnimateUpdate = computed(() => store.state.myself[finishAnimateUpdateState])
    const finishAnimateUpdateButton = computed(() => store.state.myself[finishAnimateUpdateButtonState])
    return {
      updateFinishAnimateData,
      finishAnimateUpdate,
      finishAnimateUpdateButton
    }
  }
}
</script>

<style scoped>

</style>
