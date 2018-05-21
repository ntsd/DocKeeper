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
              <div style="padding: 3rem 0.7rem;text-align: center;">
              <b-form-file id="file_input2" v-model="form.file" class="inputfile inputfile-5" placeholder="Choose a file..." plain />
              <!--<label for="file_input2"><span style="width: 300px;">{{form.file && form.file.name}}</span> <strong><svg xmlns="http://www.w3.org/2000/svg" width="20" height="17" viewBox="0 0 20 17"><path d="M10 0l-5.2 4.9h3.3v5.1h3.8v-5.1h3.3l-5.2-4.9zm9.3 11.5l-3.2-2.1h-2l3.4 2.6h-3.5c-.1 0-.2.1-.2.1l-.8 2.3h-6l-.8-2.2c-.1-.1-.1-.2-.2-.2h-3.6l3.4-2.6h-2l-3.2 2.1c-.4.3-.7 1-.6 1.5l.6 3.1c.1.5.7.9 1.2.9h16.3c.6 0 1.1-.4 1.3-.9l.6-3.1c.1-.5-.2-1.2-.7-1.5z"/></svg> Choose a file&hellip;</strong></label>-->
              <label for="file_input2"><figure><svg xmlns="http://www.w3.org/2000/svg" width="20" height="17" viewBox="0 0 20 17"><path d="M10 0l-5.2 4.9h3.3v5.1h3.8v-5.1h3.3l-5.2-4.9zm9.3 11.5l-3.2-2.1h-2l3.4 2.6h-3.5c-.1 0-.2.1-.2.1l-.8 2.3h-6l-.8-2.2c-.1-.1-.1-.2-.2-.2h-3.6l3.4-2.6h-2l-3.2 2.1c-.4.3-.7 1-.6 1.5l.6 3.1c.1.5.7.9 1.2.9h16.3c.6 0 1.1-.4 1.3-.9l.6-3.1c.1-.5-.2-1.2-.7-1.5z"/></svg></figure> <span v-if="form.file">{{form.file && form.file.name}}</span><span v-else>Choose a file&hellip;</span></label>
              </div>
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
