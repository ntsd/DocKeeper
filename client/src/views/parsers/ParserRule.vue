<template>
  <div class="animated fadeIn">
    <div class="row">
      <div class="col-12">
        <b-card header="<i class='fa fa-align-justify'></i> Parser Rule">
          <b-form @reset="onReset" >
            <b-form-group id="" label="Parser Name:">
              <b-form-input id="nameInput"
                            type="text"
                            v-model="parserRule.name"
                            required
                            placeholder="Enter Rule name">
              </b-form-input>
            </b-form-group>
            <b-form-group id="" label="Description:">
              <b-form-input id="descriptionInput"
                            type="text"
                            v-model="parserRule.description"
                            required
                            placeholder="Enter Description">
              </b-form-input>
            </b-form-group>
            <b-form-group id="" label="Rule Type:">
              <select v-model="parserRule.ruleType">
                <option value="boundary">Boundary</option>
              </select>
            </b-form-group>
            <!--this.documentList = {{this.documentList}}-->
            <!--<br>-->
            <!--{{apiRoot+documentList[0].path}}-->
            <b-form-group id="" label="Choose: ">
              <draw-rectangle-board v-bind:imagesrc="apiRoot+documentList[0].imagePaths[0]" :rect="rect"></draw-rectangle-board>
            </b-form-group>
            <b-button @click.stop="saveParserRuleButton" type="button" variant="primary">Submit</b-button>
          </b-form>
        </b-card>
      </div><!--/.col-->
    </div><!--/.row-->
  </div>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  import vSelect from "vue-select"

  import RectangleDrawBoard from '../components/RectangleDrawBoard.vue'

  import {API_ROOT} from "../../config"

  export default {  // todo fix refresh at first time and data not sent
    computed: {
      ...mapState({
        documentList: ({documentList}) => documentList.items,
        parserId: ({route}) => route.params.parserId,
      })
    },
    beforeCreate() {
    },
    created(){
      this.getDocumentListByParser(this.parserId)
    },
    data () {
      return {
        parserRule:{
          name:'',
          description:'',
          data:'',
          ruleType:'boundary'
        },
        rect:{
          startX:100,
          startY:200,
          w:100,
          h:200
        },
        apiRoot: API_ROOT
      }
    },
    methods: {
      ...mapActions([
        'getDocumentListByParser',
        'addParserRule'
      ]),
      saveParserRuleButton(){ // do not bug here
        this.parserRule.data = this.rect.startX+","+this.rect.startY+","+this.rect.w+","+this.rect.h
        // console.log(this.parserId, this.parserRule)
        this.addParserRule([this.parserId, this.parserRule])
      },
      onReset(){

      }
    },
    components: {
      vSelect,
      'draw-rectangle-board':RectangleDrawBoard
    },
    updated(){
      //console.log(this.rect)
    }
  }
</script>
