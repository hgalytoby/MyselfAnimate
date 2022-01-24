<template>
  <div v-for="(years, index) of finishList" :key="index">
    <ul class="nav nav-pills nav-fill" id="pills-tab" role="tablist">
      <li class="nav-item col-3" role="presentation" :id="`${index}-${season}`" v-for="(season, s) in 4"
          :key="`${index}-${season}`">
        <button v-if="years.data[s]"
                class="nav-link"
                :class="!s ? 'active' : ''"
                :id="`pills-${years.data[s].title}-tab`"
                data-bs-toggle="pill"
                :data-bs-target="`#pills-${years.data[s].title}`"
                type="button" role="tab" :aria-controls="`pills-${years.data[s].title}`"
                aria-selected="true" :title="years.data[s].title">{{ years.data[s].title }}
        </button>
      </li>
    </ul>
    <div class="tab-content" id="pills-tabContent">
      <ul class="tab-pane fade" :class="s === 0 ? 'show active' : ''" :id="`pills-${season.title}`" role="tabpanel"
          :aria-labelledby="`pills-${season.title}-tab`" v-for="(season, s) in years.data" :key="season.title">
        <div class="row">
          <li class="tab-items col-3" v-for="animate in season.data" :key="animate.name">
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
import { computed } from 'vue'
import { useStore } from 'vuex'
import { finishListAction, finishListState } from '../../variables/myself'

export default {
  name: 'Finish',
  setup () {
    const store = useStore()
    const finishList = computed(() => store.state.myself[finishListState])
    store.dispatch(`myself/${finishListAction}`)
    return {
      finishList
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
