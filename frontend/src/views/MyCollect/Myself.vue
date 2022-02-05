<template>
  <div class="row">
    <transition-group appear name="animate__animated animate__bounce" enter-active-class="animate__fadeIn"
                      leave-active-class="animate__fadeOut">
      <template v-for="(animate, index) in animateCollect.data">
        <div class="bg-transparent animate mb-4 col-auto" v-if="animate?.episode_info_model.length"
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
            <CollectEpisode :episode-data="animate.episode_info_model" :data-index="index"
                            :delete-action="action" :animate="animateName"/>
          </div>
        </div>
      </template>
    </transition-group>
  </div>
</template>

<script>
import { animateCollectAction, animateCollectState, destroyManyAnimateAction } from '../../variables/my'
import { startFancy } from '../../tools'
import useAnimateCollect from '../../hooks/uwsAnimateCollect'
import CollectEpisode from './CollectEpisode'
import { useStore } from 'vuex'

export default {
  name: 'Myself',
  components: {
    CollectEpisode
  },
  setup () {
    const store = useStore()
    const animateName = 'myself'
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
