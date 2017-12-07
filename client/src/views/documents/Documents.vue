<template>
  <div class="animated fadeIn">
    <div class="row">
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
              <router-link to="uploadDocument"><b-button >Upload Document</b-button></router-link>
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
            <template slot="name" scope="row">{{row.value}}</template>
            <template slot="parserRef" scope="row">{{row.value.name}}</template>
            <template slot="uploadBy" scope="row">{{row.value.username}}</template>
            <template slot="updated_at" scope="row">{{moment(row.value.$date).format('YYYY-MM-DD')}}</template>
            <template slot="actions" scope="row">
              <!-- We use click.stop here to prevent a 'row-clicked' event from also happening -->
              <b-btn size="sm" @click.stop="details(row.item,row.index,$event.target)">Details</b-btn>
            </template>
          </b-table>

          <p>
            Sort By: {{ sortBy || 'n/a' }}, Direction: {{ sortDesc ? 'descending' : 'ascending' }}
          </p>

          <!-- Details modal -->
          <b-modal id="modal1" @hide="resetModal" ok-only>
            <h4 class="my-1 py-1" slot="modal-header">Index: {{ modalDetails.index }}</h4>
            <pre>{{ modalDetails.data }}</pre>
          </b-modal>
        </b-card>
      </div><!--/.col-->
    </div><!--/.row-->
  </div>
</template>

<script>
  const documentList = [ ]

  import { mapState, mapActions } from 'vuex'

  export default {
    computed: {
      ...mapState({
        documentList: ({documentList}) => documentList.items
      })
    },
    beforeCreate() {
    },
    created(){
      this.getDocumentList({})
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
        perPage: 5,
//        totalRows: items.length,
        pageOptions: [{text: 5, value: 5}, {text: 10, value: 10}, {text: 15, value: 15}],
        sortBy: null,
        sortDesc: false,
        filter: null,
        modalDetails: { index: '', data: '' }
      }
    },
    methods: {
      ...mapActions([
        'getDocumentList'
      ]),
      details (item, index, button) {
        this.modalDetails.data = JSON.stringify(item, null, 2)
        this.modalDetails.index = index
        this.$root.$emit('bv::show::modal', 'modal1', button)
      },
      resetModal () {
        this.modalDetails.data = ''
        this.modalDetails.index = ''
      },
      onFiltered (filteredItems) {
        // Trigger pagination to update the number of buttons/pages due to filtering
        this.totalRows = filteredItems.length
        this.currentPage = 1
      }
    }
  }
</script>
