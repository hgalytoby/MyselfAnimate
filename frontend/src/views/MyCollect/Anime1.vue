<template>
  <div class="container-fluid">
    <div class="row">
      <transition-group appear name="animate__animated animate__bounce" enter-active-class="animate__fadeIn"
                        leave-active-class="animate__fadeOut">
        <div class="col-auto" v-for="animate in animateCollect.data" :key="animate.id">
          <h5 class="card-title">{{ animate.name }}</h5>
          <p v-for="episode in animate.episode_info_model" :key="episode.id">
              <a href="javascript:void(0)" @click.prevent="startFancy(episode.video)">{{ episode.name }}</a>
            </p>
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script>
import { animateCollectAction, animateCollectState } from '../../variables/my'
import { startFancy } from '../../tools'
import useAnimateCollect from '../../hooks/uwsAnimateCollect'

export default {
  name: 'Anime1',
  setup () {
    const animateCollect = useAnimateCollect('anime1', animateCollectAction, animateCollectState)
    return {
      animateCollect,
      startFancy
    }
  }
}
</script>

<style scoped>

</style>
