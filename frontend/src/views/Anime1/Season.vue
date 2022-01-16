<template>
  <p class="fs-1">{{seasonData.header}}</p>
  <table class="table border week">
    <thead>
    <tr>
      <th class="text-center" colspan="7">{{ seasonData.title }}</th>
    </tr>
    <tr>
      <th v-for="(day, index) in seasonData.days" :key="index">{{ day }}</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="(animateArr, dayIndex) in seasonData.week_data" :key="dayIndex">
      <td v-for="(animate, animateIndex) in animateArr" :key="animateIndex"
          :class="animateIndex === today ? 'today' : 'not-today'">
        <router-link v-if="animate.url" :to="{
                name: 'Anime1Animate',
                query: {
                  url: animate.url === '0' ? 123456 : animate.url
                }
              }">{{ animate.name }}
        </router-link>
        <template v-else>{{ animate.name }}</template>
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
          }">{{ season.season }}
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

export default {
  name: 'Season',
  setup () {
    const route = useRoute()
    const season = route.params.season
    const store = useStore()
    store.dispatch(`anime1/${seasonAction}`, season)
    const seasonData = computed(() => store.state.anime1[seasonState])
    const today = new Date().getDay()

    function getSeasonData (season) {
      store.dispatch(`anime1/${seasonAction}`, season)
    }

    return {
      seasonData,
      today,
      getSeasonData
    }
  }
}
</script>

<style scoped lang="scss">
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

  %a-hover {
    a {
      color: #3d3d3d;
      text-decoration: none;

      &:hover {
        color: #77cc6d;
      }
    }
  }
</style>
