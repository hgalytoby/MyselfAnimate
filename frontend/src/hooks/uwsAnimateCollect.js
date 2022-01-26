import { computed } from 'vue'
import useWindowsFocus from './useWindowsFocus'

export default function (store, animate, action, state) {
  useWindowsFocus(store.dispatch, `${animate}/${action}`)
  store.dispatch(`${animate}/${action}`)
  return computed(() => store.state[animate][state])
}
