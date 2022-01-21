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
    console.log(props.data)
    return {
      props
    }
  }
}
</script>

<style lang="scss" scoped>
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
  %a-hover {
    a {
      color: #3d3d3d;
      text-decoration: none;

      &:hover {
        color: #77cc6d;
      }
    }
  }
</style>
