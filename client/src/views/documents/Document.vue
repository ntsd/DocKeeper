<template>
  <div class="animated fadeIn">
    <div class="row">
      <div class="col-6">
        <b-card header="<i class='fa fa-align-justify'></i> Document Details">
          Name: {{document.name}} <br>
          Upload By: {{document.uploadBy.username}} <br>
          Updated At: {{moment(document.created_at.$date).format('YYYY-MM-DD')}} <br>
          Path: {{apiRoot+ document.path}} <br>
        </b-card>
      </div>
      <div class="col-6">
        <b-card header="<i class='fa fa-align-justify'></i> Extract">
          <b-btn @click="extract(documentId)">Extract</b-btn><br>
          {{document.extracted || ''}}
        </b-card>
      </div>
      <div class="col-12">
        <b-card header="<i class='fa fa-align-justify'></i> Preview">
          <!--<img v-bind:src="'http://127.0.0.1:8000/' +document.path" alt="preview"/>-->
          <img v-bind:src="apiRoot +document.path" class="img-fluid" alt="Responsive image" ref="imagePreview"/>
        </b-card>
      </div><!--/.col-->
    </div><!--/.row-->
  </div>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  import vSelect from "vue-select"

  import {API_ROOT} from "../../config"

  export default {
    computed: {
      ...mapState({
        document: ({document}) => document.document,
        parserList: ({parserList}) => parserList.items,
        documentId: ({route}) => route.params.documentId,
      })
    },
    beforeCreate() {
    },
    created(){
      this.getDocument(this.documentId)
    },
    data () {
      return {
        apiRoot:API_ROOT
      }
    },
    methods: {
      ...mapActions([
        'getDocument',
        'extractDocument'
      ]),
      extract(documentId){
        this.extractDocument(documentId)
      },
    },
    components: {
      vSelect
    },
  }
</script>
