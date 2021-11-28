import { onMounted, onBeforeUnmount } from 'vue'

export default function (func, action, args) {
  function getTimestamp () {
    return Math.floor(Date.now() / 1000)
  }

  function windowsFocus () {
    const newTimestamp = getTimestamp()
    if (document.visibilityState === 'visible' && newTimestamp - nowTimestamp > 5) {
      func(action, args)
      nowTimestamp = newTimestamp
    }
  }
  let nowTimestamp = Math.floor(Date.now() / 1000)
  onMounted(() => {
    console.log('addEventListener: visibilitychange')
    window.addEventListener('visibilitychange', windowsFocus)
  })
  onBeforeUnmount(() => {
    console.log('removeEventListener: visibilitychange')
    window.removeEventListener('visibilitychange', windowsFocus)
  })
}
