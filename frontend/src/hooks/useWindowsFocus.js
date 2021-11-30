import { onMounted, onBeforeUnmount } from 'vue'

export default function (func, action, args) {
  function windowsFocus () {
    console.log(args)
    func(action, args)
  }
  onMounted(() => {
    window.addEventListener('focus', windowsFocus)
  })
  onBeforeUnmount(() => {
    console.log('removeEventListener: focus')
    window.removeEventListener('focus', windowsFocus)
  })
}
