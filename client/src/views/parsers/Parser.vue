<template>
  <div class="animated fadeIn">
    <div class="row">
      <div class="col-4">
        <b-card header="<i class='fa fa-align-justify'></i> Parser Details">
          Name : {{parser.name}} <br>
          Description : {{parser.description}} <br>
          Owner: {{parser.owners[0].username}} <br>
          Tags: {{parser.tags}} <br>
          CreateAt: {{moment(parser.created_at.$date).format('YYYY-MM-DD')}}
        </b-card>
      </div>
      <div class="col-8">
        <b-card header="<i class='fa fa-align-justify'></i> Parser Rules">
          <div class="row my-1">
            <div class="col-sm-8">
              <b-pagination :total-rows=parser.parserRules.length :per-page=5 v-model="parserRuleCurrentPage" />
            </div>
            <div class="col-sm-4 text-md-right">
              <router-link :to="{name: 'Parser Rule', params: {parserId: parserId, parserRuleId: 'new'
                    }}"><b-button >New Rule</b-button></router-link>
            </div>
          </div>
          <b-table striped hover show-empty
                   :items=parser.parserRules
                   :fields="parserRuleFields"
                   :current-page="currentPage"
                   :per-page="perPage"
                   :filter="filter"
                   :sort-by.sync="sortBy"
                   :sort-desc.sync="sortDesc"
                   @filtered="onFiltered"
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
            </template>
          </b-table>
        </b-card>
      </div>
      <div class="col-12">
        <b-card header="<i class='fa fa-align-justify'></i> Documents Table">
          <div class="my-1 row">
            <div class="col-md-6">
              <b-form-group horizontal label="Rows per page" :label-cols="6">
                <b-form-select :options="pageOptions" v-model="perPage" />
              </b-form-group>
            </div>
            <div class="col-md-6">
              <b-form-group horizontal label="Filter" :label-cols="3">
                <b-input-group>
                  <b-form-input v-model="filter" placeholder="Type to Search" />
                  <b-input-group-button>
                    <b-btn @click="filter = ''">Clear</b-btn>
                  </b-input-group-button>
                </b-input-group>
              </b-form-group>
            </div>
          </div>

          <div class="row my-1">
            <div class="col-sm-8">
              <b-pagination :total-rows=documentList.length :per-page="perPage" v-model="currentPage" />
            </div>
            <div class="col-sm-4 text-md-right">
              <router-link :to="{name: 'Upload Document', params: {parserId: this.parserId}}"><b-button >Upload Document</b-button></router-link>
              <b-button :disabled="!sortBy" @click="sortBy = null">Clear Sort</b-button>
            </div>
          </div>

          <!-- Main table element -->
          <b-table striped hover show-empty
                   :items=documentList
                   :fields="fields"
                   :current-page="currentPage"
                   :per-page="perPage"
                   :filter="filter"
                   :sort-by.sync="sortBy"
                   :sort-desc.sync="sortDesc"
                   @filtered="onFiltered"
                   ref="table"
          >
            <template slot="name" scope="row">
              <router-link :to="{name: 'Document', params: {documentId: row.item._id.$oid}}">
                {{row.value}}
              </router-link>
            </template>
            <template slot="parserRef" scope="row">{{row.value.name}}</template>
            <template slot="uploadBy" scope="row">{{row.value.username}}</template>
            <template slot="updated_at" scope="row">{{moment(row.value.$date).format('YYYY-MM-DD')}}</template>
            <template slot="actions" scope="row">
              <b-btn v-b-modal.editModal @click.stop="editButton(row.item,$event.target)">Edit</b-btn>
            </template>
          </b-table>

          <p>
            Sort By: {{ sortBy || 'n/a' }}, Direction: {{ sortDesc ? 'descending' : 'ascending' }}
          </p>

          <b-modal id="editModal"
                   centered
                   ref="modal"
                   title="Edit Document"
                   @ok="handleOk"
          >
            <form @submit.stop.prevent="handleSubmit">
              <b-form-group id="" label="Document Name:">
                <b-form-input id="nameInput"
                              type="text"
                              v-model="modalEdit.name"
                              required
                              placeholder="Enter Document name">
                </b-form-input>
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
    },
    data () {
      return {
//        items: items,
        fields: {
          name: { label: 'File Name', sortable: true },
          parserRef: { label: 'Parser', sortable: true},
          uploadBy: { label: 'upload by', sortable: true, 'class': 'text-center' },
          updated_at: { label: 'last update',sortable: true },
          actions: { label: 'Actions' }
        },
        currentPage: 1,
        perPage: 10,
//        totalRows: items.length,
        pageOptions: [{text: 5, value: 5}, {text: 10, value: 10}, {text: 15, value: 15}],
        sortBy: null,
        sortDesc: false,
        filter: null,
        modalEdit: {
          name: '',
          parserRef: null,
          uploadBy:'',
          updated_at:'',
          image_url:''
        },
        parserRuleFields: {
          name: {label:'Rules'},
          ruleType: {label: 'Type'},
          actions: {label:'Actions'}
        },
        parserRuleCurrentPage: 1,
      }
    },
    methods: {
      ...mapActions([
        'getParserList',
        'getDocumentListByParser',
        'getParser'
      ]),
      initData(){
//        console.log(this.parserId)
        this.getDocumentListByParser(this.parserId)
        this.getParser(this.parserId)
        this.getParserList()
      },
      handleOk (evt) {
//        evt.preventDefault()
      },
      handleSubmit () {
//        this.names.push()this.name
        this.$refs.modal.hide()
      },
      editButton(item, button){
        this.modalEdit = item
//        this.$root.$emit('bv::show::editModal', 'editModal', button)
      },
      onFiltered (filteredItems) {
        this.totalRows = filteredItems.length
        this.currentPage = 1
      }
    },
    components: {
      vSelect
    },
    name:"Parser",
  }
</script>
