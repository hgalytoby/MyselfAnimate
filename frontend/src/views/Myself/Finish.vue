<template>
  <div v-for="(years, index) of finishList" :key="index">
    <ul class="nav nav-pills nav-fill" id="pills-tab" role="tablist">
      <li class="nav-item col-sm-12 col-md-3" role="presentation" :id="`${index}-${season}`" v-for="(season, num) in 4"
          :key="`${index}-${season}`">
        <button v-if="years.data[num]"
                class="nav-link"
                :class="seasonSwitch[index] === years.data[num].title ? 'active' : ''"
                :id="`pills-${years.data[num].title}-tab`"
                data-bs-toggle="pill"
                :data-bs-target="`#pills-${years.data[num].title}`"
                type="button" role="tab" :aria-controls="`pills-${years.data[num].title}`"
                aria-selected="true" :title="years.data[num].title"
                @mouseover="hoverSeason(index, years.data[num].title)">{{years.data[num].title }}
        </button>
      </li>
    </ul>
    <div class="tab-content" id="pills-tabContent">
      <ul class="tab-pane fade p-1" :class="seasonSwitch[index] === season.title ? 'show active' : ''"
          :id="`pills-${season.title}`" role="tabpanel"
          :aria-labelledby="`pills-${season.title}-tab`" v-for="season in years.data" :key="season.title">
        <div class="row">
          <li class="tab-items col-sm-12 col-md-3 " v-for="animate in season.data" :key="animate.name">
            <router-link :title="animate.name" :to="{
              name: 'MyselfAnimate',
              query: {
                url: animate.url.split('/').at(-1)
              }
            }">{{ animate.name }}
            </router-link>
          </li>
        </div>
      </ul>
    </div>
  </div>
</template>

<script>
import { computed, reactive, watch } from 'vue'
import { useStore } from 'vuex'
import { finishListAction, finishListState } from '../../variables/myself'

export default {
  name: 'Finish',
  setup () {
    const store = useStore()
    const seasonSwitch = reactive({})
    const finishList = computed(() => store.state.myself[finishListState])
    const seasonTable = computed(() => {
      if (finishList.value.length) {
        return Object.assign(...finishList.value.map((item, index) => ({ [index]: item.data[0].title })))
      }
      return []
    })

    watch(seasonTable, (newValue, oldValue) => {
      for (const [key, value] of Object.entries(newValue)) {
        seasonSwitch[key] = value
      }
    }, { deep: false })
    store.dispatch(`myself/${finishListAction}`)

    function hoverSeason (index, title) {
      seasonSwitch[index] = title
    }

    return {
      finishList,
      hoverSeason,
      seasonSwitch
    }
  }
}
</script>

<style lang="scss" scoped>
  @import "./src/assets/scss/tools";

  .tab-items {
    @extend %a-hover;
  }

  li {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
</style>
