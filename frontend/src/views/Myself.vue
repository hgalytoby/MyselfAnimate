<template>
    <ul class="nav nav-tabs" id="pills-tab" role="tablist">
      <li class="nav-item" role="presentation" v-for="(_, week, index) of weekAnimate" :key="week">
        <button class="nav-link" :class="index===0 ? 'active' : ''" :id="`pills-${week}-tab`" data-bs-toggle="pill"
                :data-bs-target="`#pills-${week}`"
                type="button" role="tab" :aria-controls="`pills-${week}`" :aria-selected="index===0"> {{ weekDict[week] }}
        </button>
      </li>
    </ul>
    <div class="tab-content" id="pills-tabContent">
      <template v-for="(animateArray, week, index) of weekAnimate" :key="week">
        <ul class="tab-pane fade list-unstyled" :class="index===0 ? 'show active' : ''"
            :id="`pills-${week}`" role="tabpanel" :aria-labelledby="`pills-${week}-tab`">
          <li v-for="animate in animateArray" :key="animate.url">
            <div class="row justify-content-start">
              <div class="col animateLink">
                <router-link :to="{
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
import { computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import {
  weekAnimateAction,
  weekAnimateState
} from '../variables/variablesMyself'

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
    const weekAnimate = computed(() => store.state.myself[weekAnimateState])
    onMounted(() => {
      store.dispatch(`myself/${weekAnimateAction}`)
    })
    return {
      weekAnimate,
      weekDict
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
