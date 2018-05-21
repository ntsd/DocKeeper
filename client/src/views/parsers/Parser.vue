<template>
  <div class="animated fadeIn">
    <div class="row">
      <div class="col-4">
        <b-card header="<i class='fa fa-align-justify'></i> Parser Details">
          Name : {{parser.name}} <br>
          Description : {{parser.description}} <br>
          Owner: {{parser.owners[0].username}} <br>
          Editors: <li v-for="editor in parser.editors">{{editor.username}} </li>
          Tags: <li v-for="tag in parser.tags">{{tag}} </li>
          CreateAt: {{moment(parser.created_at.$date).format('YYYY-MM-DD')}}
        </b-card>
      </div>
      <div class="col-8">
        <b-card header="<i class='fa fa-align-justify'></i> Parser Rules">
          <div class="row my-1">
            <div class="col-sm-8">
              <b-pagination :total-rows=parser.parserRules.length :per-page=5 v-model="parserRulesTable.currentPage" />
            </div>
            <div class="col-sm-4 text-md-right">
              <router-link :to="{name: 'Parser Rule', params: {parserId: parserId, parserRuleId: 'new'
                    }}"><b-button >New Rule</b-button></router-link>
            </div>
          </div>
          <b-table striped hover show-empty
                   :items=parser.parserRules
                   :fields="parserRulesTable.parserRuleFields"
                   :current-page="parserRulesTable.currentPage"
                   :per-page="5"
                   :sort-by.sync="parserRulesTable.sortBy"
                   :sort-desc.sync="parserRulesTable.sortDesc"
                   ref="table"
          >
            <template slot="name" scope="row">
              {{row.value}}
            </template>
            <template slot="ruleType" scope="row">{{row.value}}</template>
            <template slot="actions" scope="row">
              <router-link :to="{name: 'Parser Rule', params: {parserId: parserId, parserRuleId: row.item.oid.$oid
                    }}">
                <b-btn >Edit</b-btn>
              </router-link>
              <b-button v-b-modal.deleteParserRuleModal @click.stop="deleteParserRuleButton(row.item,$event.target)" variant="danger">Delete</b-button>
            </template>
          </b-table>
        </b-card>
      </div>
      <div class="col-12">
        <b-card header="<i class='fa fa-align-justify'></i> Documents Table">
          <div class="my-1 row">
            <div class="col-md-6">
              <b-form-group horizontal label="Rows per page" :label-cols="6">
                <b-form-select :options="documentsTable.pageOptions" v-model="documentsTable.perPage" />
              </b-form-group>
            </div>
            <div class="col-md-6">
              <b-form-group horizontal label="Filter" :label-cols="3">
                <b-input-group>
                  <b-form-input v-model="documentsTable.filter" placeholder="Type to Search" />
                  <b-input-group>
                    <b-btn @click="documentsTable.filter = ''">Clear</b-btn>
                  </b-input-group>
                </b-input-group>
              </b-form-group>
            </div>
          </div>

          <div class="row my-1">
            <div class="col-sm-8">
              <b-pagination :total-rows="this.documentsTable.totalRows" :per-page="documentsTable.perPage" v-model="documentsTable.currentPage" />
            </div>
            <div class="col-sm-4 text-md-right">
              <router-link :to="{name: 'Upload Document', params: {parserId: this.parserId}}"><b-button >Upload Document</b-button></router-link>
              <b-button :disabled="!documentsTable.sortBy" @click="documentsTable.sortBy = null">Clear Sort</b-button>
            </div>
          </div>

          <!-- Main table element -->
          <b-table striped hover show-empty
                   :items=documentList
                   :fields="documentsTable.fields"
                   :current-page="documentsTable.currentPage"
                   :per-page="documentsTable.perPage"
                   :filter="documentsTable.filter"
                   :sort-by.sync="documentsTable.sortBy"
                   :sort-desc.sync="documentsTable.sortDesc"
                   @filtered="onFiltered"
                   ref="table"
          >
            <template slot="name" scope="row">
              <router-link :to="{name: 'Document', params: {documentId: row.item._id.$oid}}">
                {{row.value}}
              </router-link>
            </template>
            <template slot="parserRef" scope="row">
              <router-link v-if="row.value" :to="{name: 'Parser', params: {parserId: row.value.id.$oid}}">
                {{row.value.name}}
              </router-link>
            </template>
            <template slot="uploadBy" scope="row">{{row.value.username}}</template>
            <template slot="updated_at" scope="row">{{moment(row.value.$date).format('YYYY-MM-DD')}}</template>
            <template slot="actions" scope="row">
              <b-btn v-b-modal.editModal @click.stop="editButton(row.item,$event.target)">Edit</b-btn>
              <b-button v-b-modal.deleteDocumentModal @click.stop="deleteDocumentButton(row.item,$event.target)" variant="danger">Delete</b-button>
            </template>
          </b-table>

          <p>
            Sort By: {{ documentsTable.sortBy || 'n/a' }}, Direction: {{ documentsTable.sortDesc ? 'descending' : 'ascending' }}
          </p>

          <b-modal id="editModal"
                   centered
                   ref="modal"
                   title="Edit Document"
                   @ok="handleOk"
          >
            <form>
              <b-form-group id="" label="Document Name:">
                <input  type="text"
                              v-model="modalEdit.name"
                              required
                >
              </b-form-group>
              <b-form-group id="" label="Parser:">
                <v-select
                  label="name"
                  :options=this.parserList
                  v-model="modalEdit.parserRef"
                ></v-select>
              </b-form-group>
            </form>
          </b-modal>
          <b-modal id="deleteParserRuleModal"
                   centered
                   ref="deleteParserRuleModal"
                   title="Delete Rule"
                   @ok="deleteParserRuleOk"
          >
            <form @submit.stop.prevent="deleteParserRuleSubmit">
            </form>
          </b-modal>
          <b-modal id="deleteDocumentModal"
                   centered
                   ref="deleteDocumentModal"
                   title="Delete Document"
                   @ok="deleteDocumentOk"
          >
            <form @submit.stop.prevent="deleteSubmit">
            </form>
          </b-modal>
        </b-card>
      </div><!--/.col-->
    </div><!--/.row-->
  </div>
</template>

<script>
  const documentList = [ ]

  import { mapState, mapActions } from 'vuex'

  import vSelect from "vue-select"

  export default {
    computed: {
      ...mapState({
        documentList: ({documentList}) => documentList.items,
        parserList: ({parserList}) => parserList.items,
        parserId: ({route}) => route.params.parserId,
        parser: ({parser}) => parser.parser,
      })
    },
    beforeCreate() {
    },
    created(){
      this.initData()
      this.documentsTable.totalRows = this.parserList.length
    },
    data () {
      return {
//        items: items,
        documentsTable: {
          fields: {
            name: { label: 'File Name', sortable: true },
            parserRef: { label: 'Parser', sortable: true},
            uploadBy: { label: 'upload by', sortable: true, 'class': 'text-center' },
            updated_at: { label: 'last update',sortable: true },
            actions: { label: 'Actions' }
          },
          currentPage: 1,
          perPage: 10,
         // totalRows: items.length,
          pageOptions: [{text: 5, value: 5}, {text: 10, value: 10}, {text: 15, value: 15}],
          sortBy: null,
          sortDesc: false,
          filter: null,
        },
        modalEdit: {
          name: '',
          parserRef: null,
          uploadBy:'',
          updated_at:''
        },
        parserRulesTable: {
          parserRuleFields: {
            name: {label: 'Rules'},
            ruleType: {label: 'Type'},
            actions: {label: 'Actions'}
          },
          currentPage: 1,
          perPage: 5,
          sortBy: null,
          sortDesc: false,
          filter: null,
        },
        parserRuleToDelete: null,
        documentToDelete:null
      }
    },
    methods: {
      ...mapActions([
        'getParserList',
        'getDocumentListByParser',
        'updateDocument',
        'deleteDocument',
        'getParser',
        'deleteParserRule'
      ]),
      initData(){
//        console.log(this.parserId)
        this.getDocumentListByParser(this.parserId)
        this.getParser(this.parserId)
        this.getParserList()
      },
      handleOk (evt) {
        // console.log(this.modalEdit.parserRef)
        if(this.modalEdit.parserRef._id){
          // difference from documents.vue cuz parserlist get difference documents this get by parserId look in back-end
          this.modalEdit.parserRef = {
            "id": {
              "$oid": this.modalEdit.parserRef._id.$oid
            },
            "name": this.modalEdit.parserRef.name
          }
        }
        this.updateDocument([this.modalEdit._id.$oid, this.modalEdit])
      },
      editButton(item, button){
        this.modalEdit = JSON.parse(JSON.stringify(item)) // for deep
      },
      onFiltered (filteredItems) {
        this.documentsTable.totalRows = filteredItems.length
        this.documentsTable.currentPage = 1
      },
      deleteParserRuleButton(item, button){
        this.parserRuleToDelete = item
      },
      deleteParserRuleOk(){
        this.deleteParserRule([this.parserId, this.parserRuleToDelete])
        this.deleteParserRuleSubmit()
      },
      deleteParserRuleSubmit(){
        this.$refs.deleteParserRuleModal.hide()
      },
      deleteDocumentButton(item, button){
        this.documentToDelete = item
      },
      deleteDocumentOk(){
        this.deleteDocument(this.documentToDelete._id.$oid)
        this.deleteDocumentSubmit()
      },
      deleteDocumentSubmit(){
        this.$refs.deleteDocumentModal.hide()
      }

    },
    components: {
      vSelect
    },
    name:"Parser",
  }
</script>
