<template>
  <div class="overflow-auto col-auto" style="max-height: 350px;">
    <div class="row" v-for="episode in props.episodeData" :key="episode.id">
      <div class="col-1">
        <BootstrapIcon v-if="!checkBoxFind(episode.id)" icon="square" @click="checkBoxAction(episode.id, 'push')"/>
        <BootstrapIcon v-else @click="checkBoxAction(episode.id, 'remove')" icon="check2-square"/>
      </div>
      <div class="col-1">
        <BootstrapIcon icon="play-btn" @click="startFancy(episode.video)"/>
      </div>
      <span class="col-8 text-nowrap overflow-hidden" style="text-overflow: ellipsis;"
            :title="episode.name">{{ episode.name }}</span>
    </div>
  </div>
  <button type="button" class="col-auto btn btn-danger">
    <span style="writing-mode: vertical-lr">刪除所選取的集數</span>
  </button>
</template>

<script>
import { reactive } from 'vue'

export default {
  name: 'CollectEpisode',
  props: {
    episodeData: Object
  },
  setup (props) {
    const checkBox = reactive([])
    function checkBoxAction (id, action) {
      if (action === 'push') {
        checkBox.push(id)
      } else {
        const index = checkBox.indexOf(id)
        if (index !== -1) {
          checkBox.splice(index, 1)
        }
      }
    }
    function checkBoxFind (id) {
      return checkBox.indexOf(id) !== -1
    }
    return {
      props,
      checkBox,
      checkBoxAction,
      checkBoxFind
    }
  }
}
</script>

<style scoped>

</style>
