import { computed } from 'vue'
import { useStore } from 'vuex'
import useWindowsFocus from './useWindowsFocus'

export default function (animate, action, state) {
  const store = useStore()
  useWindowsFocus(store.dispatch, `${animate}/${action}`)
  store.dispatch(`${animate}/${action}`)
  return computed(() => store.state[animate][state])
}
