<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-sm-auto sticky-top sidebar-bg">
        <div class="d-flex flex-column flex-row flex-nowrap sticky-top">
          <div class="d-flex flex-column border-bottom border-white">
            <img src="/me.ico" alt="" class="img-fluid rounded-circle mx-auto mb-3 w-auto">
            <h4 class="text-white text-center">
              <span class="text-center">嘟嘟嚕</span>
            </h4>
            <!--            <BootstrapIcon icon="list" color="white" size="2x"/>-->
            <h6 class="text-white">請教我刻板</h6>
            <a class="nav-link py-2 px-2" title="" href="https://github.com/hgalytoby/MyselfAnimate"
               data-bs-toggle="tooltip"
               data-bs-placement="right"
               data-bs-original-title="Home">
              <BootstrapIcon icon="github" color="white"/>
              <span class="text-white ms-2">GitHub</span>
            </a>
          </div>
          <ul
            class="nav nav-pills nav-flush flex-sm-column flex-row flex-nowrap mt-3">
            <li class="nav-item m-1">
              <router-link class="nav-link px-2" title="" to="/" data-bs-toggle="tooltip"
                           data-bs-placement="right"
                           data-bs-original-title="Home">
                <BootstrapIcon icon="house" color="white"/>
                <span class="text-white ms-2">首頁</span>
              </router-link>
            </li>
            <li class="nav-item m-1">
              <router-link class="nav-link px-2" title="" to="/MyDownload" data-bs-toggle="tooltip"
                           data-bs-placement="right"
                           data-bs-original-title="Orders">
                <BootstrapIcon icon="cloud-download" color="white"/>
                <span class="text-white ms-2">下載</span>
              </router-link>
            </li>
            <li class="nav-item m-1">
              <router-link class="nav-link px-2" title="" to="/MyCollect" data-bs-toggle="tooltip"
                           data-bs-placement="right"
                           data-bs-original-title="Products">
                <BootstrapIcon icon="collection-play" color="white"/>
                <span class="text-white ms-2">收藏</span>
              </router-link>
            </li>
            <li class="nav-item m-1">
              <router-link class="nav-link px-2" title="" to="/MyLog" data-bs-toggle="tooltip"
                           data-bs-placement="right"
                           data-bs-original-title="Products">
                <BootstrapIcon icon="journal-text" color="white"/>
                <span class="text-white ms-2">日誌</span>
              </router-link>
            </li>
            <li class="nav-item m-1">
              <router-link class="nav-link px-2" title="" to="/MySettings" data-bs-toggle="tooltip"
                           data-bs-placement="right"
                           data-bs-original-title="Products">
                <BootstrapIcon icon="gear" color="white"/>
                <span class="text-white ms-2">設定</span>
              </router-link>
            </li>
          </ul>
        </div>
      </div>
      <div class="col-sm min-vh-100 content-bg p-0">
        <!-- content -->
        <Navbar/>
        <div class="mt-4 mx-4">
          <router-view></router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from './Navbar'

export default {
  name: 'Sidebar',
  components: { Navbar }
}
</script>

<style lang="scss" scoped>
  .items a {
    color: black;
  }

  .bi {
    font-size: 24px;
  }
  ul li {
    border-radius: 12px;
    &:hover {
      background: white;
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
  .content-bg {
    background: rgba(203,203,210,.15);
  }
</style>
