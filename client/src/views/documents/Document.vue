<template>
  <div class="animated fadeIn">
    <div class="row">
      <div class="col-4">
        <b-card header="<i class='fa fa-align-justify'></i> Document Details">
          Name: {{document.name}} <br>
          Upload By: {{document.uploadBy.username}} <br>
          Updated At: {{moment(document.created_at.$date).format('YYYY-MM-DD')}} <br>
          Path: <a :href="apiRoot+ document.path">{{apiRoot+ document.path}}</a> <br>
        </b-card>
      </div>
      <div class="col-8">
        <b-card header="<i class='fa fa-align-justify'></i> Extract">
          <div class="row">
            <div class="col-2">
              <b-btn @click="extract(documentId)">Extract</b-btn>
            </div>
            <div class="col-2">
              <b-btn @click="exportCSV()">Export to csv</b-btn>
            </div>
            <div class="col-2">
              <b-btn @click="copyToClipboard()">Copy To Clipboard</b-btn>
            </div>
          </div>
          <br>
          <div class="row">
            <textarea class="js-copytextarea" rows="10" style="width: 100%;">{{document.extracted||'pls extract'}}</textarea>
          </div>
        </b-card>
      </div>
      <div class="col-12">
        <b-card no-body header-tag="header" >
          <div slot="header">
            <i class='fa fa-align-justify'></i> Preview <b-btn @click='saveButton' style='float: right' danger>save</b-btn>
          </div>
          <b-tabs card>
            <!--<b-tab title="Tab 1" active>-->
              <!--Tab Contents 1-->
            <!--</b-tab>-->
            <!--<b-tab title="Tab 2">-->
              <!--Tab Contents 2-->
            <!--</b-tab>-->
            <!--<div v-for="(imagePath, index) in document.imagePaths"> {{imagePath}} </div>-->
            <b-tab :title="'Page '+(index+1).toString()" v-for="(imagePath, index) in document.imagePaths" :key="document.id">
              <!--{{Object.keys(document.extracted).length}}-->
              <div class="col-12" v-if="Object.keys(document.extracted && document.extracted).length !== 0">
                <!--{{document.extracted[index].extractedRules}}-->
                <ExtractedTable :extractedRules="document.extracted[index].extractedRules"></ExtractedTable>
              </div>
              <hr>
              <div class="col-12">
                <img v-bind:src="apiRoot + imagePath" class="img-fluid" alt="Responsive image" ref="imagePreview"/>
              </div>
            </b-tab>
          </b-tabs>
        </b-card>
      </div>
      <!--/.col-->
    </div><!--/.row-->
  </div>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  import vSelect from "vue-select"

  import ExtractedTable from '../components/ExtractedTable.vue'

  import {API_ROOT} from "../../config"

  import api from "../../api/index"

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
      saveButton(){
        console.log(this.document)
        api.putDocument(this.document._id.$oid, this.document)
      },
      extract(documentId){
        this.extractDocument(documentId)
      },
      exportCSV(){
        const items = this.document.extracted[0].extractedRules
        const replacer = (key, value) => value === null ? '' : value // specify how you want to handle null values here

        let headSet = []
        let dataDict={}
        for(let i=0;i<items.length;i++){
          headSet.push(items[i].name)
          dataDict[items[i].name] = []
        }
        // console.log(headSet)
        let docExtracts = this.document.extracted
        for(let i=0;i<docExtracts.length;i++){
          // headSet.push(items[i].name)
          let extractRules = this.document.extracted[i].extractedRules
          for(let j=0;j<extractRules.length;j++){
            // headSet.push(items[i].name)
            dataDict[extractRules[j].name].push(extractRules[j].data.replace(/,/g,''))
          }
        }
        console.log(dataDict)
        let csv_list=[]
        csv_list.push(headSet.join(','))
        for(let i=0;i<dataDict[headSet[0]].length;i++) {
          let rows=[]
          for(let j=0;j<headSet.length;j++) {
            rows.push(dataDict[headSet[j]][i])
          }
          csv_list.push(rows.join(','))
        }
        console.log(csv_list)
        let csv = csv_list.join('\r\n')


        // const header = Object.keys(items[0])
        // let many_items = []
        // for(let i=0;i<this.document.extracted.length;i++){
        //   for(let j=0;j<this.document.extracted[i].extractedRules.length;j++){
        //     if(this.document.extracted[i].extractedRules[j].ruleType != 'table'){
        //       many_items.push(this.document.extracted[i].extractedRules[j])
        //     }
        //   }
        // }
        // console.log(many_items)
        // let csv = many_items.map(row => header.map(fieldName => JSON.stringify(row[fieldName].replace(',', ''), replacer)).join(','))
        // csv.unshift(header.join(','))
        // csv = csv.join('\r\n')

        console.log(csv)

        var file = new Blob([csv], {type: 'text/plain'});
        if (window.navigator.msSaveOrOpenBlob) // IE10+
          window.navigator.msSaveOrOpenBlob(file, this.document.name+'.csv');
        else { // Others
          var a = document.createElement("a"),
            url = URL.createObjectURL(file);
          a.href = url;
          a.download = this.document.name+'.csv';
          document.body.appendChild(a);
          a.click();
          setTimeout(function() {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
          }, 0);
        }
      },
      copyToClipboard(){
        const copyTextarea = document.querySelector('.js-copytextarea');
        copyTextarea.select();

        try {
          document.execCommand('copy');
        } catch (err) {
          console.log('Oops, unable to copy');
        }
      }
    },
    components: {
      vSelect,
      'ExtractedTable':ExtractedTable
    },
  }
</script>
