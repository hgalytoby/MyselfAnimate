<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-sm-auto sticky-top sidebar-bg">
        <div class="d-flex flex-column flex-row flex-nowrap align-items-center sticky-top">
          <div class="d-flex align-items-center justify-content-center">
            <img src="/me.ico" alt="" class="rounded-circle">
            <h4 class="text-white">
              <span class="text-center">嘟嘟嚕</span>
            </h4>
            <BootstrapIcon icon="list" color="white" size="2x"/>
          </div>
          <ul
            class="nav nav-pills nav-flush flex-sm-column flex-row flex-nowrap">
            <li class="nav-item">
              <router-link class="nav-link py-3 px-2" title="" href="https://github.com/hgalytoby/MyselfAnimate" to=""
                           data-bs-toggle="tooltip"
                           data-bs-placement="right"
                           data-bs-original-title="Home">
                <BootstrapIcon icon="github" color="white"/>
                <span class="text-white">GitHub</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link py-3 px-2" title="" to="/" data-bs-toggle="tooltip"
                           data-bs-placement="right"
                           data-bs-original-title="Home">
                <BootstrapIcon icon="house" color="white"/>
                <span class="text-white">首頁</span>
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
                <BootstrapIcon icon="cloud-download" color="white"/>
                <span class="text-white">下載</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link py-3 px-2" title="" to="/MyLove" data-bs-toggle="tooltip"
                           data-bs-placement="right"
                           data-bs-original-title="Products">
                <BootstrapIcon icon="suit-heart-fill" color="white"/>
                <span class="text-white">收藏</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link py-3 px-2" title="" to="/MyLog" data-bs-toggle="tooltip"
                           data-bs-placement="right"
                           data-bs-original-title="Products">
                <BootstrapIcon icon="journal-text" color="white"/>
                <span class="text-white">日誌</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link py-3 px-2" title="" to="/MySettings" data-bs-toggle="tooltip"
                           data-bs-placement="right"
                           data-bs-original-title="Products">
                <BootstrapIcon icon="gear" color="white"/>
                <span class="text-white">設定</span>
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

  ul > li {
    &:hover {
      background: white;
      border-radius: 12px;
      span {
        color: black !important;
      }
      .bi {
        color: black;
      }
    }
  }
  .sidebar-bg {
    background: #11101D;
  }
</style>
