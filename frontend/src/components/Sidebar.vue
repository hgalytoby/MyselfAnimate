<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-sm-auto bg-light sticky-top">
        <div class="d-flex flex-sm-column flex-row flex-nowrap bg-light align-items-center sticky-top">
          <a href="https://github.com/hgalytoby/MyselfAnimate" class="d-block p-3 link-dark text-decoration-none"
             title="" data-bs-toggle="tooltip"
             data-bs-placement="right" data-bs-original-title="Icon-only">
            <BootstrapIcon icon="github" size="2x"/>
          </a>
          <ul
            class="nav nav-pills nav-flush flex-sm-column flex-row flex-nowrap mb-auto mx-auto text-center align-items-center items">
            <li class="nav-item">
              <router-link class="nav-link py-3 px-2" title="" to="/" data-bs-toggle="tooltip"
                           data-bs-placement="right"
                           data-bs-original-title="Home">
                <BootstrapIcon icon="house" size="2x"/>
              </router-link>
            </li>
            <div class="dropdown">
              <a href="#"
                 class="d-flex align-items-center justify-content-center p-3 link-dark text-decoration-none dropdown-toggle"
                 data-bs-toggle="dropdown" aria-expanded="false">
                <img src="/animate/myself.ico" alt="Myself">
              </a>
              <ul class="dropdown-menu" aria-labelledby="">
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
            <li class="nav-item">
              <router-link class="nav-link py-3 px-2" title="" to="/MyDownload" data-bs-toggle="tooltip"
                           data-bs-placement="right"
                           data-bs-original-title="Orders">
                <BootstrapIcon icon="cloud-download" size="2x"/>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link py-3 px-2" title="" to="/MyLove" data-bs-toggle="tooltip"
                           data-bs-placement="right"
                           data-bs-original-title="Products">
                <BootstrapIcon icon="suit-heart-fill" size="2x"/>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link py-3 px-2" title="" to="/MyLog" data-bs-toggle="tooltip"
                           data-bs-placement="right"
                           data-bs-original-title="Products">
                <BootstrapIcon icon="journal-text" size="2x"/>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link py-3 px-2" title="" to="/MySettings" data-bs-toggle="tooltip"
                           data-bs-placement="right"
                           data-bs-original-title="Products">
                <BootstrapIcon icon="gear" size="2x"/>
              </router-link>
            </li>
          </ul>
        </div>
      </div>
      <div class="col-sm p-3 min-vh-100">
        <!-- content -->
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Sidebar'
}
</script>

<style lang="scss" scoped>
  .items a {
    color: black;
  }
</style>
