<template>
  <div class="app flex-row align-items-center">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card-group mb-0">
            <div class="card p-4">
              <div class="card-body">
                <form  @submit.prevent="loginButton()" novalidate>
                  <h1>Login</h1>
                  <p class="text-muted">Sign In to your account</p>
                  <div class="input-group mb-3">
                    <span class="input-group-addon"><i class="icon-user"></i></span>
                    <input type="text" name="username" v-model="user.username" class="form-control" placeholder="Username">
                  </div>
                  <div class="input-group mb-4">
                    <span class="input-group-addon"><i class="icon-lock"></i></span>
                    <input type="password" name="password" v-model="user.password" class="form-control" placeholder="Password">
                  </div>
                  <div class="row">
                    <div class="col-6">
                      <button class="btn btn-primary px-4" type="submit" id="signin_btn">Login</button>
                    </div>
                    <div class="col-6 text-right">
                      <button type="button" class="btn btn-link px-0">Forgot password?</button>
                    </div>
                  </div>
                </form>
              </div>
            </div>
            <div class="card text-white bg-primary py-5 d-md-down-none" style="width:44%">
              <div class="card-body text-center">
                <div>
                  <h2>Sign up</h2>
                  <!--<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>-->
                  <router-link to="register">
                  <button type="button" class="btn btn-primary active mt-3" >Register Now!</button>
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  /* eslint-disable */
  import { mapState, mapActions } from 'vuex'
  export default {
    name: 'Login',
    computed: {
      ...mapState({
        token: ({ auth }) => auth.token
      })
    },
    data(){
      return {
        user: {
          username: '',
          password: ''
        }
      }
    },
    methods: {
      ...mapActions([
        'localLogin'
      ]),
      loginButton(){
        this.localLogin(this.user)
      }
    },
  }
</script>
