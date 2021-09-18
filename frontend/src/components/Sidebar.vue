<template>
  <div></div>
  <div class="container-fluid">
    <div class="row">
      <div class="col-sm-auto bg-light sticky-top">
        <div class="d-flex flex-sm-column flex-row flex-nowrap bg-light align-items-center sticky-top">
          <a href="/" class="d-block p-3 link-dark text-decoration-none" title="" data-bs-toggle="tooltip"
             data-bs-placement="right" data-bs-original-title="Icon-only">
            <BootstrapIcon icon="bootstrap"/>
          </a>
          <ul
            class="nav nav-pills nav-flush flex-sm-column flex-row flex-nowrap mb-auto mx-auto text-center align-items-center">
            <li class="nav-item">
              <a href="#" class="nav-link py-3 px-2" title="" data-bs-toggle="tooltip" data-bs-placement="right"
                 data-bs-original-title="Home">
                <BootstrapIcon icon="house"/>
              </a>
            </li>
            <li>
              <a href="#" class="nav-link py-3 px-2" title="" data-bs-toggle="tooltip" data-bs-placement="right"
                 data-bs-original-title="Dashboard">
                <BootstrapIcon icon="speedometer2"/>
              </a>
            </li>
            <li>
              <a href="#" class="nav-link py-3 px-2" title="" data-bs-toggle="tooltip" data-bs-placement="right"
                 data-bs-original-title="Orders">
                <BootstrapIcon icon="table"/>
              </a>
            </li>
            <li>
              <a href="#" class="nav-link py-3 px-2" title="" data-bs-toggle="tooltip" data-bs-placement="right"
                 data-bs-original-title="Products">
                <BootstrapIcon icon="heart"/>
              </a>
            </li>
            <li>
              <a href="#" class="nav-link py-3 px-2" title="" data-bs-toggle="tooltip" data-bs-placement="right"
                 data-bs-original-title="Customers">
                <BootstrapIcon icon="people"/>
              </a>
            </li>
          </ul>
          <div class="dropdown">
            <a href="#"
               class="d-flex align-items-center justify-content-center p-3 link-dark text-decoration-none dropdown-toggle"
               id="dropdownUser3" data-bs-toggle="dropdown" aria-expanded="false">
              <BootstrapIcon icon="person-circle"/>
            </a>
            <ul class="dropdown-menu text-small shadow" aria-labelledby="dropdownUser3">
              <li><a class="dropdown-item" href="#">New project...</a></li>
              <li><a class="dropdown-item" href="#">Settings</a></li>
              <li><a class="dropdown-item" href="#">Profile</a></li>
            </ul>
          </div>
        </div>
      </div>
      <div class="col-sm p-3 min-vh-100">
        <!-- content -->
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Sidebar'
}
</script>

<style scoped>

</style>
