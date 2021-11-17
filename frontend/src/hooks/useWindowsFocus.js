import { onMounted, onBeforeUnmount } from 'vue'

export default function () {
  function windowsFocus () {
    if (document.visibilityState === 'visible') {
      console.log('tab is active')
    } else {
      console.log('tab is inactive')
    }
  }
  onMounted(() => {
    console.log('addEventListener: visibilitychange')
    window.addEventListener('visibilitychange', windowsFocus)
  })
  onBeforeUnmount(() => {
    console.log('removeEventListener: visibilitychange')
    window.removeEventListener('visibilitychange', windowsFocus)
  })
}
