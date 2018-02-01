<template>
  <div class="animated fadeIn">
    <div class="row">
      <div class="col-12" >
        <!--<b-card header="<i class='fa fa-align-justify'></i> Parsers Table">-->
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
              <b-pagination :total-rows=parserList.length :per-page="perPage" v-model="currentPage" />
            </div>
            <div class="col-sm-4 text-md-right">
              <router-link to="newparser"><b-button @click="">New Parser</b-button></router-link>
              <b-button :disabled="!sortBy" @click="sortBy = null">Clear Sort</b-button>
            </div>
          </div>

          <!-- Main table element -->
          <b-table striped hover show-empty
                   :items=parserList
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
                <router-link :to="{name: 'Parser', params: {parserId: row.item._id.$oid}}">
                  {{row.value}}
                </router-link>
              </template>

            <template slot="owners" scope="row">
              <div v-for="user in row.value">
                {{user.username}}
              </div>
            </template>
            <template slot="tags" scope="row">
              <div v-for="tag in row.value">
                {{tag}}
              </div>
            </template>
            <template slot="updated_at" scope="row">
              {{moment(row.value.$date).format('YYYY-MM-DD')}}
            </template>
            <template slot="actions" scope="row">
              <b-btn v-b-modal.editModal @click.stop="editButton(row.item)">Edit</b-btn>
              <b-button v-b-modal.deleteModal @click.stop="deleteButton(row.item,$event.target)" variant="danger">Delete</b-button>
            </template>
          </b-table>

          <p>
            Sort By: {{ sortBy || 'n/a' }}, Direction: {{ sortDesc ? 'descending' : 'ascending' }}
          </p>

          <!-- Details modal -->
          <b-modal id="editModal"
                   centered
                   ref="modal"
                   title="Edit Document"
                   @ok="handleOk"
          >
            <form @submit.stop.prevent="handleSubmit">
              <b-form-group id="" label="Parser Name:">
                <b-form-input id="nameInput"
                              type="text"
                              v-model="modalEdit.name"
                              required
                              placeholder="Enter Parser name">
                </b-form-input>
              </b-form-group>
              <b-form-group id="" label="Description:">
                <b-form-input id="descriptionInput"
                              type="text"
                              v-model="modalEdit.description"
                              required
                              placeholder="Enter Description">
                </b-form-input>
              </b-form-group>
              <b-form-group id="" label="Tags:">
                <input-tag placeholder="Add Tags" :tags="modalEdit.tags"></input-tag>
              </b-form-group>
            </form>
          </b-modal>
        <b-modal id="deleteModal"
                 centered
                 ref="deleteModal"
                 title="Delete Document"
                 @ok="deleteOk"
        >
          <form @submit.stop.prevent="deleteSubmit">
          </form>
        </b-modal>

        <!--</b-card>-->
      </div><!--/.col-->
    </div><!--/.row-->
  </div>
</template>

<script>
  /*eslint-disable */
  import InputTag from 'vue-input-tag'
  import { mapState, mapActions } from 'vuex'
  const parserList = [];

  export default {
    computed: {
      ...mapState({
        parserList: ({parserList}) => parserList.items
      })
    },
    beforeCreate() {
    },
    created(){
      this.getParserList({})
    },
    data () {
      return {
//        items: parserList,
        fields: {
          name: { label: 'parser name', sortable: true },
          owners: { label: 'owners', sortable: true, 'class': 'text-center' },
          tags: { label: 'tags', sortable: true },
          updated_at: {label: 'last updated', sortable: true },
          actions: { label: 'Actions' }
        },
        currentPage: 1,
        perPage: 10,
//        totalRows: parserList.length,
        pageOptions: [{text: 5, value: 5}, {text: 10, value: 10}, {text: 15, value: 15}],
        sortBy: null,
        sortDesc: false,
        filter: null,
        modalEdit: {
          name: '',
          owners: null,
          tags:[],
          description:''
        },
        deleteModal: null
      }
    },
    methods: {
      ...mapActions([
        'getParserList',
        'deleteParser'
      ]),
      handleOk (evt) {
        evt.preventDefault()
        this.handleSubmit()
      },
      handleSubmit () {
        this.$refs.modal.hide()
      },
      editButton(item){
        this.modalEdit = item
      },
      onFiltered (filteredItems) {
        // Trigger pagination to update the number of buttons/pages due to filtering
        this.totalRows = filteredItems.length
        this.currentPage = 1
      },
      deleteButton(item, button){
        // todo delete button
        this.modalDelete = item
      },
      deleteOk(){
        this.deleteParser(this.modalDelete._id.$oid)
        this.deleteSubmit()
      },
      deleteSubmit(){
        this.$refs.deleteModal.hide()
      }
    },
    components:{
      InputTag
    }
  }

  /*eslint-enable */
</script>
