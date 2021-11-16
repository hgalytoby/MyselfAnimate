<template>
  <!--  {{myselfAnimateCollect}}-->
  <transition-group appear name="animate__animated animate__bounce" enter-active-class="animate__fadeIn"
                    leave-active-class="animate__fadeOut">
    <div class="card" v-for="animate in myselfAnimateCollect.data" :key="animate.id">
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
  <!--  <transition appear name="animate__animated animate__bounce" enter-active-class="animate__fadeIn"-->
  <!--              leave-active-class="animate__fadeOut">-->
  <!--    <nav aria-label="Page navigation example" v-show="showPagination">-->
  <!--      <ul class="pagination justify-content-center">-->
  <!--        <li class="page-item" :class="previousPage" @click="changePage(myselfAnimateCollect.page - 1)">-->
  <!--          <a class="page-link" href="#">Previous</a>-->
  <!--        </li>-->
  <!--        <li class="page-item"><a class="page-link" href="#">{{ finishAnimate.page }}</a></li>-->
  <!--        <li class="page-item" :class="nextPage" @click="changePage(finishAnimate.page + 1)">-->
  <!--          <a class="page-link" href="#">next</a>-->
  <!--        </li>-->
  <!--      </ul>-->
  <!--      <p class="text-center">全部:{{ finishAnimate.count }} / 總頁數:{{ finishAnimate.total_pages }}</p>-->
  <!--    </nav>-->
  <!--  </transition>-->
</template>

<script>
import { useStore } from 'vuex'
import { onMounted, computed } from 'vue'
import { animateCollectState, animateCollectAction } from '../variables/myself'
import { useStartFancy } from '../hooks/useFancybox'

document.addEventListener('visibilitychange', event => {
  if (document.visibilityState === 'visible') {
    console.log('tab is active')
  } else {
    console.log('tab is inactive')
  }
})
export default {
  name: 'MyCollect',
  setup () {
    const store = useStore()
    const myselfAnimateCollect = computed(() => store.state.myself[animateCollectState])
    const startFancy = useStartFancy
    onMounted(() => {
      store.dispatch(`myself/${animateCollectAction}`)
    })
    return {
      myselfAnimateCollect,
      startFancy
    }
  }
}
</script>

<style scoped>

</style>
