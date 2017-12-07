<template>
  <div class="animated fadeIn">
    <div class="row">
      <div class="col-12">
        <b-card>
          <div slot="header">
            <i class='fa fa-align-justify'></i> Upload Document
          </div>
          <b-form @submit="onSubmit" @reset="onReset" v-if="show">
            <b-form-group id="" label="Document Name:">
              <b-form-input id="nameInput"
                            type="text"
                            v-model="form.name"
                            required
                            placeholder="Enter Document name">
              </b-form-input>
            </b-form-group>
            <b-form-group id="" label="Parser:">
              <b-form-select id="parserInput"
                             :options="parsers"
                             required
                             v-model="form.parserRef">
              </b-form-select>
            </b-form-group>

            <b-form-group id="" label="Select File:">
              <!-- Customized labels -->
              <b-form-file id="file_input2" v-model="form.path" choose-label="Attachment2"></b-form-file>
               {{form.path && form.path.name}}
            </b-form-group>

            <b-button type="submit" variant="primary">Submit</b-button>

          </b-form>
        </b-card>
      </div><!--/.col-->
    </div><!--/.row-->
  </div>
</template>

<script>
  /*eslint-disable */
  import { mapState, mapActions } from 'vuex'

  export default {
    computed: {
      ...mapState({
        parserList: ({parserList}) => parserList.items
      })
    },
    data () {
      return {
        form: {
          name: '',
          parserRef: {},
          path: null
        },
        show: true,
        parsers: [
          { text: 'Select One', value: null },
          { text: 'Select TWO', value: null },
          { text: 'Select Three', value: null }
        ]
      }
    },
    name: 'uploaddocument',
    methods: {
      ...mapActions([
        'getParserList',
        'addParser'
      ]),
      onSubmit (evt) {
        evt.preventDefault();
        this.addParser(this.form)
      },
      onReset (evt) {
        evt.preventDefault();
        // Reset our form values
        this.form.name = '';
        this.form.description = null;
        this.form.tags = [];
        // Trick to reset/clear native browser form validation state
        this.show = false;
        this.$nextTick(() => { this.show = true });
      }
    },
    components: {

    }
  }
  /*eslint-enable */
</script>
