<template>
  <div>
    <div class="mb-5">
      <h3>Myself設定</h3>
      <div class="mb row">
        <label for="myselfDownload" class="col-sm-2  col-form-label">最大同時下載數量</label>
        <div class="col-sm-1">
          <input type="text" class="form-control text-center" id="myselfDownload" aria-describedby="emailHelp"
                 v-model.number="settings.myself_download_value">
        </div>
      </div>
    </div>
    <div class="mb-5">
      <h3>Anime1設定</h3>
      <div class="mb row">
        <label for="anime1Download" class="col-sm-2 col-form-label">最大同時下載數量</label>
        <div class="col-sm-1">
          <input type="text" class="form-control text-center" id="anime1Download" aria-describedby="emailHelp"
                 v-model.number="settings.anime1_download_value">
        </div>
      </div>
    </div>
    <button class="btn btn-primary" @click="update">儲存</button>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { settingsGetAction, settingsState, settingsPutAction } from '../variables/my'

export default {
  name: 'MySettings',
  setup () {
    const store = useStore()
    const settings = computed(() => store.state.my[settingsState])
    store.dispatch(`my/${settingsGetAction}`)
    function update () {
      store.dispatch(`my/${settingsPutAction}`)
    }

    return {
      settings,
      update
    }
  }
}
</script>

<style scoped>

</style>
