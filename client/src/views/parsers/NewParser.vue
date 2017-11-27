<template>
  <div class="animated fadeIn">
    <div class="row">
      <div class="col-12">
        <b-card>
          <div slot="header">
            <i class='fa fa-align-justify'></i> New Parser
          </div>
          <b-form-fieldset>
            <b-input-group left="Parser Name" right="">
              <b-form-input type="text"></b-form-input>
            </b-input-group>
          </b-form-fieldset>
          <b-form-fieldset>
            <b-input-group left="Tags" right="">
              <input-tag :on-change="callbackMethod" placeholder="Add Tags" :tags="tags"></input-tag>
            </b-input-group>
          </b-form-fieldset>
          <div class="form-group form-actions">
            <b-button type="submit" size="sm" variant="primary">Submit</b-button>
          </div>

        </b-card>
      </div>
    </div>
  </div>
</template>

<script>
  /*eslint-disable */
  import InputTag from 'vue-input-tag'

  export default {
    name: 'newparser',
    methods: {
      click () {
        // do nothing
      }
    },
    components: {
      InputTag
    }
  }
  /*eslint-enable */
</script>

