<template>
  <div class="overflow-auto col-auto" style="max-height: 350px;">
    <div class="row" v-for="episode in props.episodeData" :key="episode.id">
      <div class="col-1">
        <BootstrapIcon icon="check2-square"/>
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
// import { computed } from 'vue'

export default {
  name: 'Episode',
  props: {
    episodeData: Object
  },
  setup (props) {
    return {
      props
    }
  }
}
</script>

<style scoped>

</style>
