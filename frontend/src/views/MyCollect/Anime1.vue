<template>
  <div class="container-fluid">
    <div class="row">
      <transition-group appear name="animate__animated animate__bounce" enter-active-class="animate__fadeIn"
                        leave-active-class="animate__fadeOut">
        <div class="bg-transparent animate mb-4 col-auto" v-for="(animate, index) in animateCollect.data"
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
            <CollectEpisode :episode-data="animate.episode_info_model" :data-index="index"
                            :delete-action="action" :animate="animateName"/>
          </div>
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script>
import { animateCollectAction, animateCollectState, destroyManyAnimateAction } from '../../variables/my'
import { startFancy } from '../../tools'
import useAnimateCollect from '../../hooks/uwsAnimateCollect'
import CollectEpisode from '../../components/CollectEpisode'
import { useStore } from 'vuex'

export default {
  name: 'Anime1',
  components: {
    CollectEpisode
  },
  setup () {
    const store = useStore()
    const animateName = 'anime1'
    const action = destroyManyAnimateAction
    const animateCollect = useAnimateCollect(store, animateName, animateCollectAction, animateCollectState)
    return {
      animateCollect,
      startFancy,
      action,
      animateName
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
