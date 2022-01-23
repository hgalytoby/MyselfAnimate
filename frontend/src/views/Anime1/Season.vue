<template>
  <p class="fs-1" :title="seasonData.header">{{seasonData.header}}</p>
  <table class="table border week">
    <thead>
    <tr>
      <th class="text-center" colspan="7" :title="seasonData.title">{{ seasonData.title }}</th>
    </tr>
    <tr>
      <th v-for="(day, index) in seasonData.days" :key="index" :title="day">{{ day }}</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="(animateArr, dayIndex) in seasonData.week_data" :key="dayIndex">
      <td v-for="(animate, animateIndex) in animateArr" :key="animateIndex"
          :class="animateIndex === today ? 'today' : 'not-today'">
        <router-link v-if="animate.url" :to="{
                name: 'Anime1Animate',
                query: {
                  url: animate.url
                }
              }" :title="animate.name">{{ animate.name }}
        </router-link>
        <template v-else :title="animate.name">{{ animate.name }}</template>
      </td>
    </tr>
    </tbody>
  </table>
  <p class="season">
    <template v-for="(season, index) in seasonData.season_data" :key="index">
      <router-link v-if="season.url" @click="getSeasonData(season.season.split('(')[0].split(' ')[1])" :to="{
            name: 'Anime1Season',
            params: {
              season: season.season.split('(')[0].split(' ')[1]
            }
          }" :title="season.season.split('(')[0].split(' ')[1]">{{ season.season }}
        <br>
      </router-link>
      <template v-else>{{ season.season }}</template>
    </template>
  </p>
</template>

<script>
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import { computed } from 'vue'
import { seasonState, seasonAction } from '../../variables/anime1'
import useWindowsFocus from '../../hooks/useWindowsFocus'

export default {
  name: 'Season',
  setup () {
    const route = useRoute()
    const store = useStore()
    const seasonData = computed(() => store.state.anime1[seasonState])
    const today = new Date().getDay()
    store.dispatch(`anime1/${seasonAction}`, route)
    function getSeasonData (season) {
      store.dispatch(`anime1/${seasonAction}`, season)
    }
    useWindowsFocus(store.dispatch, `anime1/${seasonAction}`, route)
    return {
      seasonData,
      today,
      seasonAction,
      getSeasonData
    }
  }
}
</script>

<style scoped lang="scss">
  @import "./src/assets/scss/tools";
  /*用 @/<scss path> IDE 會顯示紅色的，看了不開心*/
  .week {
    border: #e6e6e6;
  }

  .today {
    background-color: #fff9bc
  }

  .not-today {
    background-color: #fff;
  }

  table {
    th {
      background: #f9f9f9;
      border-bottom: 1px solid #e6e6e6 !important;
    }

    td {
      background: #fff;
      border: 1px solid #e6e6e6
    }

    @extend %a-hover;
  }

  .season {
    @extend %a-hover;
    color: #666666;
  }

</style>
