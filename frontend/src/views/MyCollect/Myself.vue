<template>
  <transition-group appear name="animate__animated animate__bounce" enter-active-class="animate__fadeIn"
                    leave-active-class="animate__fadeOut">
    <div class="row">
      <div class="bg-transparent animate mb-4 col-auto" v-for="animate in animateCollect.data"
           :key="animate.id">
        <router-link :title="animate.name" :to="{
              name: 'MyselfAnimate',
              query: {
                url: animate.url.split('/').at(-1)
              }
            }">
            <div class="fs-5 text-nowrap overflow-hidden" style="text-overflow: ellipsis;"
                 :title="animate.name">{{ animate.name }}
            </div>
          </router-link>
        <div class="row">
          <div class="col-auto">
            <img :src="animate.image" class="img-fluid" :alt="animate.name" :title="animate.name">
          </div>
          <div class="overflow-auto col-auto" style="max-height: 350px;">
            <div class="row" v-for="episode in animate.episode_info_model" :key="episode.id">
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

<style scoped lang="scss">
  @import "../../assets/scss/tools";

  .animate {
    @extend %a-hover;
  }
</style>
