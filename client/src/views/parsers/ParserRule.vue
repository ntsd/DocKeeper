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
                <option value="table">Table</option>
              </select>
            </b-form-group>
            <b-form-group id="" label="Characters White List :">
              <select v-model="parserRule.charWhitelist">
                <option value="" >All</option>
                <option value="0123456789" >Digits</option>
                <option value="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" >Alphabets</option>
                <option value="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" >Digits+Alphabets</option>
                <option value="customs" >Customs</option>
              </select>
              <div v-if="parserRule.charWhitelist === 'customs'">
                <b-form-input type="text"
                              v-model="customsCharWhitelist"
                              placeholder="Enter Characters"></b-form-input>
              </div>
            </b-form-group>
            <!--this.documentList = {{this.documentList}}-->
            <!--<br>-->
            <!--{{apiRoot+documentList[0].path}}-->
            <div v-if="documentList.length > 0 ">
              <b-form-group id="" label="Sample Document:">
              <select v-model="sampleDocumentUrl">
                <option :value="apiRoot+document.imagePaths[0]" v-for="document in documentList">{{document.name}}</option>
              </select>
                <b-button @click.stop="clearDraw">Clear</b-button>
            </b-form-group>
              <b-form-group id="" label="Draw: ">
                <div v-if="parserRule.ruleType==='boundary'">
                  <draw-rectangle-board v-bind:imagesrc="sampleDocumentUrl" :rect="rect"></draw-rectangle-board>
                </div>
                <div v-else-if="parserRule.ruleType==='table'">
                  <TableDrawBoard v-bind:imagesrc="sampleDocumentUrl" :linesX="linesX"></TableDrawBoard>
                </div>
              </b-form-group>
              <b-form-group>
                <b-button @click.stop="extractPreviewButton()" type="button" >Extract Preview</b-button>
                {{extractPreview}}
                <!--<div v-if="parserRule.ruleType === 'table'"> &lt;!&ndash; todo &ndash;&gt;-->
                  <!--<table class="table">-->
                    <!--<thead>-->
                    <!--<tr>-->
                      <!--<th v-for="col in extractPreview[0]">{{col}}</th>-->
                    <!--</tr>-->
                    <!--</thead>-->
                    <!--<tbody>-->
                    <!--<tr v-for="(row,index) in extractPreview">-->
                      <!--<td v-for="col in row" v-if="index!=0">{{col}}</td>-->
                    <!--</tr>-->
                    <!--</tbody>-->
                  <!--</table>-->
                <!--</div>-->
                <!--<div v-if="parserRule.ruleType === 'boundary'">-->
                  <!--{{extractPreview.data}}-->
                <!--</div>-->
              </b-form-group>
              <b-button @click.stop="saveParserRuleButton" type="button" variant="primary">Submit</b-button>
            </div>
            <div v-else>
              <h2 style="color: red">Pls Add Sample Document To Create Parser Rule</h2>
            </div>


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

  import TableDrawBoard from '../components/TableDrawBoard'

  import {API_ROOT} from "../../config"

  import api from "../../api/index"

  export default {
    computed: {
      ...mapState({
        documentList: ({documentList}) => documentList.items,
        parserId: ({route}) => route.params.parserId,
        parserRuleId: ({route}) => route.params.parserRuleId,
        parserRules: ({parser}) => parser.parser.parserRules
      })
    },
    beforeCreate() {
    },
    created(){
      this.getDocumentListByParser(this.parserId)
      if(this.parserRuleId !== "new"){
        //console.log('parser rules',this.parserRules)
        const parserRuleId = this.parserRuleId
        const parserRule = this.parserRules.filter(function( parserRule ) { // get parser Rule from id
          return parserRule.oid.$oid === parserRuleId;
        })[0];
        //console.log('parser rules',parserRule)
        this.parserRule = parserRule
        if(this.parserRule.ruleType === 'boundary'){
          this.rect = this.parserRule.data
        }
        else if(this.parserRule.ruleType === 'table'){
          this.linesX = this.parserRule.data
        }

      }
      this.sampleDocumentUrl = API_ROOT+this.documentList[0].imagePaths[0]
    },
    mounted(){
      // check if not in list mean customs
      if(["",
          "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
          "0123456789",
          "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ","customs"].indexOf(this.parserRule.charWhitelist) === -1){
        this.customsCharWhitelist = ''+this.parserRule.charWhitelist
        this.parserRule.charWhitelist = "customs"
      }
    },
    data () {
      return {
        parserRule:{
          name:'',
          description:'',
          data:null,
          ruleType:'boundary',
          charWhitelist:''
        },
        rect:{
          x:0,
          y:0,
          w:0,
          h:0
        },
        apiRoot: API_ROOT,
        sampleDocumentUrl:'',
        customsCharWhitelist: '',
        linesX: [],
        extractPreview: null
      }
    },
    methods: {
      ...mapActions([
        'getDocumentListByParser',
        'addParserRule'
      ]),
      saveParserRuleButton(){ // do not bug here
        if(this.parserRule.ruleType === 'boundary'){
          this.parserRule.data = this.rect
        }
        else if(this.parserRule.ruleType === 'table'){
          this.parserRule.data = this.linesX
        }
        // console.log(this.parserRule.data)
        if(this.parserRule.charWhitelist === 'customs'){
          this.parserRule.charWhitelist = this.customsCharWhitelist
        }
        this.addParserRule([this.parserId, this.parserRule])
      },
      onReset(){

      },
      clearDraw(){
        this.rect = {x:0,y:0,w:0,h:0}
        this.linesX = []
        if(this.parserRule.ruleType==="boundary"){
          this.parserRule.ruleType = 'table'
        }else{
          this.parserRule.ruleType = 'boundary'
        }
      },
      extractPreviewButton(){
        let parserRuleBackUp = JSON.parse(JSON.stringify(this.parserRule))
        if(parserRuleBackUp.ruleType === 'boundary'){
          parserRuleBackUp.data = this.rect
        }
        else if(parserRuleBackUp.ruleType === 'table'){
          parserRuleBackUp.data = this.linesX
        }
        // console.log(this.parserRule.data)
        if(parserRuleBackUp.charWhitelist === 'customs'){
          parserRuleBackUp.charWhitelist = this.customsCharWhitelist
        }
        api.postExtractPreview(this.documentList[0]._id.$oid, parserRuleBackUp).then((response)=>{
          const json = response.data
          this.extractPreview = json
        }).catch((e) => {
          console.log(e)
        })
      }
    },
    components: {
      vSelect,
      'draw-rectangle-board':RectangleDrawBoard,
      'TableDrawBoard':TableDrawBoard
    },
    updated(){
      //console.log(this.sampleDocumentUrl)
    }
  }
</script>
