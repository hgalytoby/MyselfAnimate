<template>
  <router-link :to="{
      name: 'Anime1Animate',
      query: {
        url: props.data.value.url
      }
    }">{{ props.data.value.name }}
  </router-link>
</template>

<script>
export default {
  name: 'TableSlot',
  props: {
    data: Object
  },
  setup (props) {
    return {
      props
    }
  }
}
</script>

<style lang="scss" scoped>
  @import "../../assets/scss/tools";
  /*用 @/<scss path> IDE 會顯示紅色的，看了不開心*/
  table {
    th {
      background: #f9f9f9;
      border-bottom: 1px solid #e6e6e6 !important;
    }

    td {
      background: #fff;
      border: 1px solid #e6e6e6
    }
    @extend %a-hover;
  }
</style>
