<template>
  <div class="container-fluid">
    <div class="row">
      <transition-group appear name="animate__animated animate__bounce" enter-active-class="animate__fadeIn"
                        leave-active-class="animate__fadeOut">
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
            <Episode :episode-data="animate.episode_info_model"/>
          </div>
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script>
import { animateCollectAction, animateCollectState } from '../../variables/my'
import { startFancy } from '../../tools'
import useAnimateCollect from '../../hooks/uwsAnimateCollect'
import Episode from './Episode'

export default {
  name: 'Anime1',
  components: {
    Episode
  },
  setup () {
    const animateCollect = useAnimateCollect('anime1', animateCollectAction, animateCollectState)
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
