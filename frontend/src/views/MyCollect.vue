<template>
  <div class="container">
    <div class="row">
      <div class="col-auto">
          <router-link to="/MyCollect/Myself">
          <figure class="figure bottom">
            <img src="/animate/myself.png" class="figure-img img-fluid rounded" alt="">
<!--            <figcaption class="figure-caption text-center text-dark">Myself</figcaption>-->
          </figure>
        </router-link>
      </div>
      <div class="col-auto">
        <router-link to="/MyCollect/Anime1">
          <figure class="figure">
            <img src="/animate/anime1.png" class="figure-img img-fluid rounded" alt="">
<!--            <figcaption class="figure-caption text-center text-dark">Anime1</figcaption>-->
          </figure>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'MyCollect',
  setup () {
  }
}
</script>

<style lang="scss" scoped>

</style>
