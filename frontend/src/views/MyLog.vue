<template>
  我是Log
  <table class="table table-hover">
    <thead>
    <tr class="table">
      <th scope="col">Action</th>
      <th scope="col">msg</th>
      <th scope="col">datetime</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="log in logs" :key="log.id">
      <td>{{ log.action }}</td>
      <td>{{ log.msg }}</td>
      <td>{{ log.datetime }}</td>
    </tr>
    </tbody>
  </table>
</template>

<script>
import { onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { myLogAction, myLogState } from '../variables/variablesMyself'

export default {
  name: 'MyLog',
  setup () {
    const store = useStore()
    const logs = computed(() => store.state.myself[myLogState])
    onMounted(() => {
      store.dispatch(`myself/${myLogAction}`)
    })
    return {
      logs
    }
  }
}
</script>

<style scoped>
</style>
