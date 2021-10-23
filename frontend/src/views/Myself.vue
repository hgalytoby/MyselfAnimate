<template>
  <div>我是 Myself</div>
  <!--  {{weekAnimate}}-->
  <ul class="nav nav-tabs" id="pills-tab" role="tablist">
    <li class="nav-item" role="presentation" v-for="(_, week, index) of weekAnimate" :key="week">
      <button class="nav-link" :class="index===0 ? 'active' : ''" :id="`pills-${week}-tab`" data-bs-toggle="pill"
              :data-bs-target="`#pills-${week}`"
              type="button" role="tab" :aria-controls="`pills-${week}`" :aria-selected="index===0"> {{week}}
      </button>
    </li>
  </ul>
  <div class="tab-content" id="pills-tabContent">
    <template v-for="(animateArray, week, index) of weekAnimate" :key="week">
      <ul class="tab-pane fade" :class="index===0 ? 'show active' : ''"
          :id="`pills-${week}`" role="tabpanel" :aria-labelledby="`pills-${week}-tab`">
        <li v-for="animate in animateArray" :key="animate.url">
          <div class="row justify-content-start">
            <div class="col-4 animateName">
              <router-link :to="{
            name: 'MyselfAnimate',
            query: {
              url: animate.url.split('/').at(-1)
            }
          }" style="color: #339900;">{{ animate.name }}
              </router-link>
            </div>
              <div class="col-4" :style="animate.update_color">
                {{ animate.update }}
              </div>
            </div>
        </li>
      </ul>
    </template>
    <!--    <div class="tab-pane fade" :class="index===0 ? 'show active' : ''"  id="pills-home" role="tabpanel" aria-labelledby="pills-home-tab">...</div>-->
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
    const store = useStore()
    const weekAnimate = computed(() => store.state.myself[weekAnimateState])
    onMounted(() => {
      store.dispatch(`myself/${weekAnimateAction}`)
    })
    return {
      weekAnimate
    }
  }
}
</script>

<style lang="scss" scoped>
  li {
    list-style-type: none;
  }
  .animateName {
    a {
      text-decoration: none;
      &:hover {
        text-decoration: underline;
      }
    }
  }
</style>
