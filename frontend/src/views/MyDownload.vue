<template>
  <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
    <li class="nav-item" role="presentation">
      <button class="nav-link active" id="pills-myself-tab" data-bs-toggle="pill" data-bs-target="#pills-myself"
              type="button" role="tab" aria-controls="pills-myself" aria-selected="true">Myself
      </button>
    </li>
    <li class="nav-item" role="presentation">
      <button class="nav-link" id="pills-anime1-tab" data-bs-toggle="pill" data-bs-target="#pills-anime1"
              type="button" role="tab" aria-controls="pills-anime1" aria-selected="true">Anime1
      </button>
    </li>
  </ul>
  <div class="tab-content" id="pills-tabContent">
    <div class="tab-pane fade show active" id="pills-myself" role="tabpanel" aria-labelledby="pills-myself-tab">
      <TabModel animate="myself" target="myself-target" clear-action="clear_finish_myself_animate"
                delete-action="delete_myself_download_animate" :download-check-box="myselfDownloadCheckBoxArray"/>
      <AnimateDownload animate="myself" order-action="download_order_myself_animate"
                       :download-animate-data="downloadMyselfAnimateArray"
                       :downloadCheckBox="myselfDownloadCheckBoxArray"/>
    </div>
    <div class="tab-pane fade" id="pills-anime1" role="tabpanel" aria-labelledby="pills-anime1-tab">
      <TabModel animate="anime1" target="anime1-target" clear-action="clear_finish_anime1_animate"
                delete-action="delete_anime1_download_animate" :download-check-box="anime1DownloadCheckBoxArray"/>
      <AnimateDownload animate="anime1" order-action="download_order_anime1_animate"
                       :download-animate-data="downloadAnime1AnimateArray"
                       :download-check-box="anime1DownloadCheckBoxArray"/>
    </div>
  </div>
</template>

<script>
import { useStore } from 'vuex'
import { downloadMyselfAnimateGetters } from '../variables/myself'
import { computed } from 'vue'
import { downloadAnime1AnimateGetters } from '../variables/anime1'
import AnimateDownload from '../components/AnimateDownload'
import TabModel from './MyDownload/TabModel'
import { downloadCheckBoxState } from '../variables/my'

export default {
  name: 'MyDownload',
  components: {
    AnimateDownload,
    TabModel
  },
  setup: function () {
    const store = useStore()
    const downloadMyselfAnimateArray = computed(() => store.getters[`myself/${downloadMyselfAnimateGetters}`])
    const downloadAnime1AnimateArray = computed(() => store.getters[`anime1/${downloadAnime1AnimateGetters}`])
    const myselfDownloadCheckBoxArray = computed(() => store.state.myself[downloadCheckBoxState])
    const anime1DownloadCheckBoxArray = computed(() => store.state.anime1[downloadCheckBoxState])

    return {
      downloadMyselfAnimateArray,
      downloadAnime1AnimateArray,
      myselfDownloadCheckBoxArray,
      anime1DownloadCheckBoxArray
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
