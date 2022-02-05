<template>
  <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
    <li class="nav-item" v-for="animate in animateArray" :key=animate role="presentation">
      <button class="nav-link" :class="animate.upper === downloadSwitch ? 'active' : ''"
              :id="`pills-${animate.upper}-tab`" @mouseover="hoverDownload(animate.upper)"
              data-bs-toggle="pill" :data-bs-target="`#pills-${animate.upper}`"
              type="button" role="tab" :aria-controls="`pills-${animate.upper}`"
              aria-selected="true">{{ animate.upper }}
      </button>
    </li>
  </ul>
  <div class="tab-content" id="pills-tabContent">
    <div v-for="animate in animateArray" :key=animate
         :class="animate.upper === downloadSwitch ? 'show active' : ''" class="tab-pane fade"
         :id="`pills-${animate.upper}`" role="tabpanel" :aria-labelledby="`pills-${animate.upper}-tab`">
      <TabModel :animate="animate.lower" :target="`${animate.lower}-target`"
                :clear-action="`clear_finish_${animate.lower}_animate`"
                :delete-action="`delete_${animate.lower}_download_animate`"
                :download-check-box="animate.downloadCheckBoxArray"/>
      <AnimateDownload :animate="animate.lower" :order-action="`download_order_${animate.lower}_animate`"
                       :download-animate-getters="animate.downloadAnimateGetters"
                       :downloadCheckBox="animate.downloadCheckBoxArray"/>
    </div>
  </div>
</template>

<script>
import { useStore } from 'vuex'
import { downloadMyselfAnimateGetters } from '../variables/myself'
import { ref } from 'vue'
import { downloadAnime1AnimateGetters } from '../variables/anime1'
import AnimateDownload from './MyDownload/AnimateDownload'
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
    const downloadSwitch = ref('Myself')
    const animateArray = [
      {
        upper: 'Myself',
        lower: 'myself',
        downloadAnimateGetters: `myself/${downloadMyselfAnimateGetters}`,
        downloadCheckBoxArray: store.state.myself[downloadCheckBoxState]
      },
      {
        upper: 'Anime1',
        lower: 'anime1',
        downloadAnimateGetters: `anime1/${downloadAnime1AnimateGetters}`,
        downloadCheckBoxArray: store.state.anime1[downloadCheckBoxState]
      }
    ]
    function hoverDownload (animate) {
      downloadSwitch.value = animate
    }
    return {
      hoverDownload,
      downloadSwitch,
      animateArray
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
