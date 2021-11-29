import { onMounted, onBeforeUnmount } from 'vue'

export default function (func, action, args) {
  function windowsFocus () {
    console.log('focus')
    func(action, args)
  }
  onMounted(() => {
    console.log('addEventListener: focus')
    window.addEventListener('focus', windowsFocus)
  })
  onBeforeUnmount(() => {
    console.log('removeEventListener: focus')
    window.removeEventListener('focus', windowsFocus)
  })
}
