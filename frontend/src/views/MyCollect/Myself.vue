<template>
<transition-group appear name="animate__animated animate__bounce" enter-active-class="animate__fadeIn"
                    leave-active-class="animate__fadeOut">
    <div class="card bg-transparent" v-for="animate in animateCollect.data" :key="animate.id">
      <div class="row g-0">
        <div class="col-md-2">
          <h5 class="card-title">{{ animate.name }}</h5>
          <img :src="animate.image" class="img-fluid rounded-start" :alt="animate.name">
        </div>
        <div class="col-md-8">
          <div class="card-body">
            <p v-for="episode in animate.episode_info_model" :key="episode.id">
              <a href="" @click.prevent="startFancy(episode.video)">{{ episode.name }}</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  </transition-group>
</template>

<script>
import { animateCollectAction, animateCollectState } from '../../variables/my'
import { startFancy } from '../../tools'
import useAnimateCollect from '../../hooks/uwsAnimateCollect'
export default {
  name: 'Myself',
  setup () {
    const animateCollect = useAnimateCollect('myself', animateCollectAction, animateCollectState)
    return {
      animateCollect,
      startFancy
    }
  }
}
</script>

<style scoped>

</style>
