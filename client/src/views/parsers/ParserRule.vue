<template>
  <div class="animated fadeIn">
    <div class="row">
      <div class="col-12">
        <b-card header="<i class='fa fa-align-justify'></i> Parser Rule">

        </b-card>
      </div><!--/.col-->
    </div><!--/.row-->
  </div>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  import vSelect from "vue-select"

  export default {
    computed: {
      ...mapState({
        document: ({document}) => document.document,
      })
    },
    beforeCreate() {
    },
    created(){
    },
    data () {
      return {
      }
    },
    methods: {
      ...mapActions([
        'getDocument'
      ]),
    },
    components: {
      vSelect
    },
  }
</script>
