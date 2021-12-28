<template>
  <nav class="navbar navbar-expand navbar-light bg-white ms-auto">
    <div class="container-fluid">
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <div class="nav-item dropdown">
            <div class="nav-link dropdown-toggle" id="myself-animate" role="button" data-bs-toggle="dropdown"
             aria-expanded="false">MyselfAnimate</div>
            <ul class="dropdown-menu" aria-labelledby="myself-animate">
              <li>
                <router-link class="dropdown-item" to="/Myself">本季新番</router-link>
              </li>
              <li>
                <router-link class="dropdown-item" to="/Myself/AnimateSearch">搜尋動漫</router-link>
              </li>
              <li>
                <router-link class="dropdown-item" to="/Myself/AnimateFinish">完結動漫</router-link>
              </li>
            </ul>
          </div>
          <div class="nav-item dropdown">
            <div class="nav-link dropdown-toggle" id="anime1" role="button" data-bs-toggle="dropdown"
               aria-expanded="false">Anime1</div>
            <ul class="dropdown-menu" aria-labelledby="anime1">
              <li>
                <router-link class="dropdown-item" to="/AnimateList">動畫列表</router-link>
              </li>
            </ul>
          </div>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar'
}
</script>

<style scoped>

</style>
