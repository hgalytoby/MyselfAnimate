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
  <button type="button" @click="deleteAnimate" class="col-auto btn btn-danger">
    <span style="writing-mode: vertical-lr">刪除所選取的集數</span>
  </button>
</template>

<script>
import { reactive } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'CollectEpisode',
  props: {
    episodeData: Object,
    deleteAction: String,
    animate: String,
    dataIndex: Number
  },
  setup (props) {
    const store = useStore()
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
    function deleteAnimate () {
      store.dispatch(`${props.animate}/${props.deleteAction}`, {
        data: { deleteArray: checkBox },
        episodeData: props.episodeData,
        dataIndex: props.dataIndex
      })
    }
    return {
      props,
      checkBox,
      checkBoxAction,
      checkBoxFind,
      deleteAnimate
    }
  }
}
</script>

<style scoped>

</style>
