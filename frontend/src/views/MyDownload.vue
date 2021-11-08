<template>
  <button type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#exampleModal">
    <BootstrapIcon class="trash" icon="trash"/>
  </button>
  <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          ...
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary">Save changes</button>
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>
  <div class="table-responsive">
    <table class="table table-hover" style="word-wrap:break-word;word-break:break-all;white-space:normal;">
      <thead>
      <tr class="table">
        <th scope="col">
          <BootstrapIcon icon="square"/>
        </th>
        <th scope="col">播放</th>
        <th scope="col">動漫名字</th>
        <th scope="col">集數</th>
        <th scope="col">狀況</th>
        <th scope="col">下載進度</th>
      </tr>
      </thead>
      <tbody>
      <tr class="align-middle" v-for="animate in downloadMyselfAnimateArray" :key="animate.id">
        <td style="width: 2%;">
          <BootstrapIcon icon="square"/>
        </td>
        <td class="text-center video-play" style="width: 4%">
          <BootstrapIcon v-if="animate.video" icon="play-btn" @click="startFancy(animate.video)"/>
          <BootstrapIcon v-else icon="pause-circle"/>
        </td>
        <td>{{ animate.animate_name }}</td>
        <td>{{ animate.episode_name }}</td>
        <td>{{ animate.status }}</td>
        <td>
          <div class="progress">
            <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar"
                 :aria-valuenow="computeProgressRate(animate.count, animate.ts_count)"
                 aria-valuemin="0" aria-valuemax="100"
                 :style="`width: ${computeProgressRate(animate.count, animate.ts_count)}%`">
              {{ computeProgressRate(animate.count, animate.ts_count) }}%
            </div>
          </div>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { useStore } from 'vuex'
import { downloadMyselfAnimateGetters } from '../variables/variablesMyself'
import { computed } from 'vue'
import { useStartFancy } from '../hooks/useFancybox'

export default {
  name: 'MyDownload',
  setup: function () {
    const store = useStore()
    const downloadMyselfAnimateArray = computed(() => store.getters[`myself/${downloadMyselfAnimateGetters}`])

    function computeProgressRate (count, tsCount) {
      const result = parseInt(count / tsCount * 100)
      return !isNaN(result) ? result : 0
    }

    const startFancy = useStartFancy
    return {
      downloadMyselfAnimateArray,
      computeProgressRate,
      startFancy
    }
  }
}
</script>

<style lang="scss" scoped>
  @import '~@fancyapps/ui/dist/fancybox.css';

  .animate-name {
    text-overflow: ellipsis;
  }

  .video-play {
    font-size: 24px;
  }

  .trash {
    font-size: 20px;
  }
</style>
