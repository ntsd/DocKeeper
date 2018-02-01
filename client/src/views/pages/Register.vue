<template>
  <div class="app flex-row align-items-center">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card mx-4">
            <div class="card-body p-4">
              <h1>Register</h1>
              <p class="text-muted">Create your account</p>
              <div class="input-group mb-3">
                <span class="input-group-addon"><i class="icon-user"></i></span>
                <input type="text" class="form-control" placeholder="Username" v-model="user.username">
              </div>

              <div class="input-group mb-3">
                <span class="input-group-addon">@</span>
                <input type="text" class="form-control" placeholder="Email" v-model="user.email">
              </div>

              <div class="input-group mb-3">
                <span class="input-group-addon"><i class="icon-lock"></i></span>
                <input type="password" class="form-control" placeholder="Password" v-model="user.password">
              </div>

              <div class="input-group mb-4">
                <span class="input-group-addon"><i class="icon-lock"></i></span>
                <input type="password" class="form-control" placeholder="Repeat password">
              </div>

              <button type="button" class="btn btn-block btn-success" v-on:click="registerButton()">Create Account</button>
            </div>
            <!--<div class="card-footer p-4">-->
              <!--<div class="row">-->
                <!--<div class="col-6">-->
                  <!--<button class="btn btn-block btn-facebook" type="button"><span>facebook</span></button>-->
                <!--</div>-->
                <!--<div class="col-6">-->
                  <!--<button class="btn btn-block btn-twitter" type="button"><span>twitter</span></button>-->
                <!--</div>-->
              <!--</div>-->
            <!--</div>-->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import api from '../../api'
  import router from '../../router'

export default {
  name: 'Register',
  data(){
    return {
      user: {
        username: '',
        password: '',
        email: ''
      }
    }
  },
  methods: {
    registerButton(){
      api.register(this.user).then(
        response => {
          router.push({path:'/pages/login'})
        }
      )
    }
  },
}
</script>
