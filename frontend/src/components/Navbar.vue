<template>
  <nav class="navbar navbar-expand navbar-light bg-white ms-auto">
    <div class="container-fluid">
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <div class="nav-item dropdown">
            <div class="nav-link dropdown-toggle" id="myself-animate" role="button" data-bs-toggle="dropdown"
             aria-expanded="false" title="MyselfAnimate">MyselfAnimate</div>
            <ul class="dropdown-menu" aria-labelledby="myself-animate">
              <li>
                <router-link class="dropdown-item" to="/Myself" title="本季新番">本季新番</router-link>
              </li>
              <li>
                <router-link class="dropdown-item" to="/Myself/AnimateSearch" title="搜尋動漫">搜尋動漫</router-link>
              </li>
              <li>
                <router-link class="dropdown-item" to="/Myself/AnimateFinish" title="完結動漫">完結動漫</router-link>
              </li>
            </ul>
          </div>
          <div class="nav-item dropdown">
            <div class="nav-link dropdown-toggle" id="anime1" role="button" data-bs-toggle="dropdown"
               aria-expanded="false" title="Anime1">Anime1</div>
            <ul class="dropdown-menu" aria-labelledby="anime1">
              <li>
                <router-link class="dropdown-item" to="/Anime1/AnimateList" title="動畫列表">動畫列表</router-link>
              </li>
              <li>
                <router-link v-if="homeMenu.text" class="dropdown-item" :to="{
                    name: 'Anime1Season',
                    params: {
                      season: homeMenu.text
                    }
                  }" :title="homeMenu.text">{{ homeMenu.text }}
                </router-link>
              </li>
            </ul>
          </div>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { useStore } from 'vuex'
import { computed } from 'vue'
import { homeMenuAction, homeMenuState } from '../variables/anime1'

export default {
  name: 'Navbar',
  setup () {
    const store = useStore()
    store.dispatch(`anime1/${homeMenuAction}`)
    const homeMenu = computed(() => store.state.anime1[homeMenuState])
    return {
      homeMenu
    }
  }
}
</script>

<style scoped>

</style>
