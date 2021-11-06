<template>
  <nav class="navbar navbar-expand navbar-light bg-white ms-auto">
    <div class="container-fluid">
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <div class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown"
               aria-expanded="false">
              MyselfAnimate
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
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
