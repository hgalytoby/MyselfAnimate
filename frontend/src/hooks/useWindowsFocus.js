import { onMounted, onBeforeUnmount } from 'vue'

export default function (windowsFocus) {
  onMounted(() => {
    console.log('addEventListener: visibilitychange')
    window.addEventListener('visibilitychange', windowsFocus)
  })
  onBeforeUnmount(() => {
    console.log('removeEventListener: visibilitychange')
    window.removeEventListener('visibilitychange', windowsFocus)
  })
}
