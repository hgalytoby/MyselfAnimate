<template>
  <p class="text-center">{{ props.msg }}</p>
</template>

<script>
export default {
  name: 'CustomToast',
  props: {
    msg: String
  },
  setup (props) {
    return {
      props
    }
  }
}
</script>

<style scoped>

</style>
