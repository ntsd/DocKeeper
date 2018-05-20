<template>
  <div class="animated fadeIn">
    <div class="row">
      <div class="col-12">
        <b-card>
          <div slot="header">
            <i class='fa fa-align-justify'></i> Upload Document
          </div>
          <b-form @reset="onReset" v-if="show">
            <b-form-group id="" label="Document Name:">
              <b-form-input id="nameInput"
                            type="text"
                            v-model="form.name"
                            required
                            placeholder="Enter Document name">
              </b-form-input>
            </b-form-group>
            <b-form-group id="" label="Parser:">
              <v-select
                label="name"
                :options=this.parserList
                v-model="form.parserRef"
              ></v-select>
            </b-form-group>

            <b-form-group id="" label="Select File:">
              <!-- Customized labels -->
              <b-form-file id="file_input2" v-model="form.file" placeholder="Choose a file..." plain></b-form-file>
              <!--<div class="mt-3">Selected file: {{form.file && form.file.name}}</div>-->
            </b-form-group>

            <b-button @click.stop="saveDocumentButton" type="button" variant="primary">Save</b-button>

          </b-form>
        </b-card>
      </div><!--/.col-->
    </div><!--/.row-->
  </div>
</template>

<script>
  /*eslint-disable */
  import { mapState, mapActions } from 'vuex'
  import vSelect from "vue-select"

  export default {
    computed: {
      ...mapState({
        parserList: ({parserList}) => parserList.items,
        parserIdParam: ({route}) => route.params.parserId
      })
    },
    data () {
      return {
        form: {
          name: '',
          parserRef: null,
          file: null
        },
        show: true
      }
    },
    mounted(){

    },
    created(){
//      this.getParserList()
      this.$store.dispatch("getParserList").then(response => {
//        console.log(JSON.parse(JSON.stringify(this.parserList)))
      }, error => {
        console.error("Got nothing from server. Prompt user to check internet connection and try again")
      })
    },
    name: 'uploaddocument',
    methods: {
      ...mapActions([
        'getParserList',
        'addDocument'
      ]),
      saveDocumentButton () {
        //evt.preventDefault();
//        console.log(this.form);
        if(this.form.file){
          this.addDocument(this.form)
        }

      },
      onReset (evt) {
        evt.preventDefault();
        // Reset our form values
        this.form.name = '';
        this.form.parserRef = null;
        this.form.file = null;
        // Trick to reset/clear native browser form validation state
        this.show = false;
        this.$nextTick(() => { this.show = true });
      }
    },
    components: {
      vSelect
    },
  }
  /*eslint-enable */
</script>
