<template>
  <div class="row">
    <div class="col-auto" v-for="animate in animateArray" :key="animate">
        <router-link :to="`/MyCollect/${animate.upper}`">
        <figure class="figure bottom">
          <img :src="`/animate/${animate.lower}.png`" :alt="animate.upper"
                class="figure-img img-fluid rounded" :title="animate.upper">
<!--            <figcaption class="figure-caption text-center text-dark">Myself</figcaption>-->
        </figure>
      </router-link>
    </div>
  </div>
</template>

<script>

export default {
  name: 'MyCollect',
  setup () {
    const animateArray = [
      {
        upper: 'Myself',
        lower: 'myself'
      },
      {
        upper: 'Anime1',
        lower: 'anime1'
      }
    ]
    return {
      animateArray
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
