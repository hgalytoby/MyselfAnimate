import { onMounted, onBeforeUnmount } from 'vue'

export default function (func, action, args) {
  let timestamp = Math.floor(Date.now() / 1000)
  function windowsFocus () {
    const nowTimestamp = Math.floor(Date.now() / 1000)
    if (nowTimestamp - timestamp > 2) {
      console.log('axios')
      timestamp = nowTimestamp
      func(action, args)
    }
  }
  onMounted(() => {
    window.addEventListener('focus', windowsFocus)
  })
  onBeforeUnmount(() => {
    console.log('removeEventListener: focus')
    window.removeEventListener('focus', windowsFocus)
  })
}
