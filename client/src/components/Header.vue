<template>
  <header class="app-header navbar">
    <button class="navbar-toggler mobile-sidebar-toggler d-lg-none" type="button" @click="mobileSidebarToggle">&#9776;</button>
    <b-link class="navbar-brand" to="#"></b-link>
    <button class="navbar-toggler sidebar-toggler d-md-down-none" type="button" @click="sidebarMinimize">&#9776;</button>
    <b-nav is-nav-bar class="d-md-down-none">
      <b-nav-item class="px-3">Dashboard</b-nav-item>
    </b-nav>
    <b-nav is-nav-bar class="ml-auto">
      <!--<b-nav-item class="d-md-down-none">-->
        <!--<i class="icon-bell"></i><span class="badge badge-pill badge-danger">5</span>-->
      <!--</b-nav-item>-->
      <b-nav-item-dropdown right>
        <template slot="button-content">
          <img :src="defaultAvatar" class="img-avatar" alt="">
          <span class="d-md-down-none">{{auth.user.username}}</span><!--auth.user.username-->
        </template>
        <b-dropdown-header tag="div" class="text-center"><strong>Account</strong></b-dropdown-header>
        <a href="javascript:;" class="shrink-logout" @click="logout()">
          <b-dropdown-item >
            <i class="fa fa-lock" ></i> Logout
          </b-dropdown-item>
        </a>
      </b-nav-item-dropdown>
    </b-nav>
    <button class="navbar-toggler aside-menu-toggler d-md-down-none" type="button" @click="asideToggle">&#9776;</button>
  </header>
</template>
<script>
  import defaultAvatar from '../assets/images/avatar.png'
  import { mapState,mapActions } from 'vuex'
  export default {
    computed: {
      ...mapState({
        auth: state => state.auth
      }),
      defaultAvatar() {
        return defaultAvatar
      }
    },
    beforeCreate() {
    },
    created (){
      // if(this.auth.token){  /// move to full containers
      //   // console.log(this.auth.token)
      //   this.getUserInfo()
      // }else{
      //
      // }
    },
    methods: {
      ...mapActions([
        'changeStyleMode',
        'logout',
      ]),
      sidebarToggle (e) {
        e.preventDefault()
        document.body.classList.toggle('sidebar-hidden')
      },
      sidebarMinimize (e) {
        e.preventDefault()
        document.body.classList.toggle('sidebar-minimized')
      },
      mobileSidebarToggle (e) {
        e.preventDefault()
        document.body.classList.toggle('sidebar-mobile-show')
      },
      asideToggle (e) {
        e.preventDefault()
        document.body.classList.toggle('aside-menu-hidden')
      }
    }
  }
</script>
