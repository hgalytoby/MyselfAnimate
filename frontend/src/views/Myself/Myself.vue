<template>
  <div class="row align-items-center">
    <div class="col">
      <input type="text" class="form-control shadow-sm p-3 mb-2 bg-body rounded" id="search"
       v-model="searchText" title="貼上網址搜尋指定動漫" placeholder="貼上網址搜尋指定動漫">
    </div>
    <div class="col-1 d-flex justify-content-center">
      <button type="button" class="btn btn-primary" title="搜尋" @click="searchAnimate">搜尋</button>
    </div>
  </div>
  <ul class="nav nav-tabs" id="pills-tab" role="tablist">
    <li class="nav-item" role="presentation" v-for="(_, week) of weekAnimate" :key="week">
      <button class="nav-link" :class="week === daySwitch ? 'active' : ''" :id="`pills-${week}-tab`"
              data-bs-toggle="pill" :data-bs-target="`#pills-${week}`" :title="weekDict[week]"
              @mouseover="hoverDay(week)" type="button" role="tab" :aria-controls="`pills-${week}`"
              aria-selected="true">{{ weekDict[week] }}
      </button>
    </li>
  </ul>
  <div class="tab-content" id="pills-tabContent">
    <template v-for="(animateArray, week) of weekAnimate" :key="week">
      <ul class="tab-pane fade list-unstyled" :class="week === daySwitch ? 'show active' : ''"
          :id="`pills-${week}`" role="tabpanel" :aria-labelledby="`pills-${week}-tab`">
        <li v-for="animate in animateArray" :key="animate.url">
          <div class="row justify-content-start">
            <div class="col animateLink">
              <router-link :title="animate.name" :to="{
              name: 'MyselfAnimate',
              query: {
                url: animate.url.split('/').at(-1)
              }
            }">{{ animate.name }}
              </router-link>
            </div>
            <div class="col text-end" :style="animate.update_color">
              {{ animate.update }}
            </div>
          </div>
        </li>
      </ul>
    </template>
  </div>
</template>

<script>
import { computed, ref } from 'vue'
import { useStore } from 'vuex'
import {
  searchAnimateAction,
  weekAnimateAction,
  weekAnimateState
} from '../../variables/myself'

export default {
  name: 'Myself',
  setup () {
    const weekDict = {
      Monday: '星期一',
      Tuesday: '星期二',
      Wednesday: '星期三',
      Thursday: '星期四',
      Friday: '星期五',
      Saturday: '星期六',
      Sunday: '星期日'
    }

    const store = useStore()
    const searchText = ref('')
    const weekAnimate = computed(() => store.state.myself[weekAnimateState])
    store.dispatch(`myself/${weekAnimateAction}`)
    const daySwitch = ref('Monday')
    function searchAnimate () {
      store.dispatch(`myself/${searchAnimateAction}`, encodeURIComponent(searchText.value))
    }
    function hoverDay (day) {
      daySwitch.value = day
    }
    return {
      weekAnimate,
      weekDict,
      searchText,
      searchAnimate,
      daySwitch,
      hoverDay
    }
  }
}
</script>

<style lang="scss" scoped>
  .animateLink {
    a {
      text-decoration: none;
      color: #339900;

      &:hover {
        text-decoration: underline;
        color: #0f8001;
      }
    }
  }
</style>
