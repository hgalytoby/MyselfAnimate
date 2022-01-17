<template>
  <div>
    <div class="mb-5">
      <h3>Myself設定</h3>
      <div class="col-md-2">
        <label for="myself-download-value" class="form-label">最大同時下載數量</label>
        <input type="text" class="form-control text-center" :class="validation.myselfDownloadValue"
               id="myself-download-value" v-model.number="settings.myself_download_value" @keypress="isNumber($event)" required>
        <div class="invalid-feedback">限制 1 ~ 15</div>
      </div>
    </div>
    <div class="mb-5">
      <h3>Anime1設定</h3>
      <div class="col-md-2">
        <label for="anime1-download-value" class="form-label">最大同時下載數量</label>
        <input type="text" class="form-control text-center" :class="validation.anime1DownloadValue"
               id="anime1-download-value" v-model.number="settings.anime1_download_value" @keypress="isNumber($event)" required>
        <div class="invalid-feedback">限制 1 ~ 10</div>
      </div>
    </div>
    <button class="col-auto btn btn-primary" @click="update">儲存</button>
  </div>
</template>

<script>
import { computed, reactive } from 'vue'
import { useStore } from 'vuex'
import { settingsState, settingsGetAction, settingsUpdateDownloadValueAction } from '../variables/my'

export default {
  name: 'MySettings',
  setup () {
    const store = useStore()
    const settings = computed(() => store.state.my[settingsState])
    const validation = reactive({
      myselfDownloadValue: computed(() => settings.value.myself_download_value <= 15 && settings.value.myself_download_value > 0 ? 'is-valid' : 'is-invalid'),
      anime1DownloadValue: computed(() => settings.value.anime1_download_value <= 10 && settings.value.anime1_download_value > 0 ? 'is-valid' : 'is-invalid')
    })
    store.dispatch(`my/${settingsGetAction}`)

    function update () {
      if (Object.values(validation).filter((value) => value !== 'is-valid').length === 0) {
        store.dispatch(`my/${settingsUpdateDownloadValueAction}`)
      }
    }

    function isNumber (event) {
      if (!/^[0-9]+$/.test(event.key) || event.key === '.') return event.preventDefault()
    }
    return {
      settings,
      update,
      validation,
      isNumber
    }
  }
}
</script>

<style scoped>

</style>
