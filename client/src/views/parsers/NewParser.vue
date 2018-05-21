<template>
  <div class="animated fadeIn">
    <div class="row">
      <div class="col-12">
        <b-card>
          <div slot="header">
            <i class='fa fa-align-justify'></i> New Category
          </div>
          <b-form @reset="onReset" v-if="show">
            <b-form-group id="" label="Category Name:">
              <b-form-input id="nameInput"
                            type="text"
                            v-model="form.name"
                            required
                            placeholder="Enter Category name">
              </b-form-input>
            </b-form-group>
            <b-form-group id="" label="Description:">
              <b-form-input id="descriptionInput"
                            type="text"
                            v-model="form.description"
                            placeholder="Enter Description">
              </b-form-input>
            </b-form-group>
            <b-form-group id="" label="Tags:">
              <input-tag :on-change="changeTags" placeholder="Add Tags" :tags="form.tags"></input-tag>
            </b-form-group>
            <b-button @click.stop="saveParserButton" type="button" variant="primary">Submit</b-button>
          </b-form>
          <!--<b-form-fieldset>-->
            <!--<b-input-group left="Parser Name" right="">-->
              <!--<b-form-input type="text"></b-form-input>-->
            <!--</b-input-group>-->
          <!--</b-form-fieldset>-->
          <!--<b-form-fieldset>-->
            <!--<b-input-group left="Tags" right="">-->
              <!--<input-tag :on-change="callbackMethod" placeholder="Add Tags" :tags="tags"></input-tag>-->
            <!--</b-input-group>-->
          <!--</b-form-fieldset>-->
          <!--<div class="form-group form-actions">-->
            <!--<b-button type="submit" size="sm" variant="primary">Submit</b-button>-->
          <!--</div>-->

        </b-card>
      </div>
    </div>
  </div>
</template>

<script>
  /*eslint-disable */
  import InputTag from 'vue-input-tag'
  import { mapActions } from 'vuex'

  export default {
    data () {
      return {
        form: {
          name: '',
          description: '',
          tags: []
        },
        show: true
      }
    },
    name: 'newparser',
    methods: {
      ...mapActions([
        'addParser'
      ]),
      saveParserButton (evt) {
        // console.log(this.form)
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
      },
      changeTags (){

      }
    },
    components: {
      InputTag
    }
  }
  /*eslint-enable */
</script>

