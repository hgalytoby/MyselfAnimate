<template>
  <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
    <li class="nav-item" role="presentation">
      <button class="nav-link active" id="pills-myself-tab" data-bs-toggle="pill" data-bs-target="#pills-myself"
              type="button" role="tab" aria-controls="pills-myself" aria-selected="true">Myself
      </button>
    </li>
    <li class="nav-item" role="presentation">
      <button class="nav-link" id="pills-anime1-tab" data-bs-toggle="pill" data-bs-target="#pills-anime1"
              type="button" role="tab" aria-controls="pills-anime1" aria-selected="false">Anime1
      </button>
    </li>
  </ul>
  <div class="tab-content" id="pills-tabContent">
    <div class="tab-pane fade show active" id="pills-myself" role="tabpanel" aria-labelledby="pills-myself-tab">
      <AnimateDownload :downloadAnimateData="downloadMyselfAnimateArray"/>
    </div>
    <div class="tab-pane fade" id="pills-anime1" role="tabpanel" aria-labelledby="pills-anime1-tab">
      <AnimateDownload :downloadAnimateData="downloadAnime1AnimateArray"/>
    </div>
  </div>
</template>

<script>
import { useStore } from 'vuex'
import { downloadMyselfAnimateGetters } from '../variables/myself'
import { computed } from 'vue'
import { downloadAnime1AnimateGetters } from '../variables/anime1'
import AnimateDownload from '../components/AnimateDownload'

export default {
  name: 'MyDownload',
  components: {
    AnimateDownload
  },
  setup: function () {
    const store = useStore()
    const downloadMyselfAnimateArray = computed(() => store.getters[`myself/${downloadMyselfAnimateGetters}`])
    const downloadAnime1AnimateArray = computed(() => store.getters[`anime1/${downloadAnime1AnimateGetters}`])

    return {
      downloadMyselfAnimateArray,
      downloadAnime1AnimateArray
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
