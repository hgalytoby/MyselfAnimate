<template>
  <div>完結列表</div>
  <div v-for="(years, index) of finishList" :key="index">
    <ul class="nav nav-pills nav-fill" id="pills-tab" role="tablist">
      <li class="nav-item" role="presentation" :id="`${index}-${s}`" v-for="(season, s) in years.data"
          :key="season.title">
        <button class="nav-link"
                :class="s === 0 ? 'active' : ''"
                :id="`pills-${season.title}-tab`"
                data-bs-toggle="pill"
                :data-bs-target="`#pills-${season.title}`"
                type="button" role="tab" :aria-controls="`pills-${season.title}`"
                :aria-selected="s === 0">{{ season.title }}
        </button>
      </li>
    </ul>
    <div class="tab-content" id="pills-tabContent">
      <ul class="tab-pane fade" :class="s === 0 ? 'show active' : ''" :id="`pills-${season.title}`" role="tabpanel"
          :aria-labelledby="`pills-${season.title}-tab`" v-for="(season, s) in years.data" :key="season.title">
        <li class="tab-items" v-for="animate in season.data" :key="animate.name">
          <router-link :to="{
            name: 'MyselfAnimate',
            query: {
              url: animate.url.split('/').at(-1)
            }
          }">{{ animate.name }}
          </router-link>
        </li>
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
  .tab-items {
    a {
      color: black;
      text-decoration: none;

      &:hover {
        text-decoration: underline;
      }
    }
  }
</style>
