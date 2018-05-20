<template>
  <b-table striped hover show-empty
           :items=extractedRules
           :fields="fields"
           ref="table"
  >
    <template slot="name" scope="row">{{row.item.name}}</template>
    <template slot="ruleType" scope="row">{{row.item.ruleType}}</template>
    <template slot="data" scope="row">
      <div v-if="row.item.ruleType === 'table'"> <!-- todo -->
        <table class="table">
          <thead>
          <tr>
            <th v-for="col in row.item.data[0]">{{col}}</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(row,index) in row.item.data">
            <td v-for="col in row" v-if="index!=0">{{col}}</td>
          </tr>
          </tbody>
        </table>
      </div>
      <div v-if="row.item.ruleType === 'boundary'">
        {{row.item.data}}
      </div>

    </template>
  </b-table>
  <!--<b-card header="Extracted Data">-->
    <!--<b-nav pills v-b-scrollspy:nav-scroller>-->
      <!--<li v-for="(extractData, index) in extractedDataList">-->
        <!--<b-nav-item href="#extracted" @click="scrollIntoView">{{ index }}</b-nav-item>-->
      <!--</li>-->
    <!--</b-nav>-->
    <!--<div id="nav-scroller"-->
                 <!--ref="content"-->
                 <!--style="position:relative; height:300px; overflow-y:scroll;">-->
      <!--<div v-for="(extractData, index) in extractedDataList">-->
        <!--<h4 id="extracted">{{index}}</h4>-->
        <!--<p>{{ extractData }}</p>-->
      <!--</div>-->
    <!--</div>-->
  <!--</b-card>-->
</template>

<script>
  export default {
    name: "extracted-table",
    props: {
      extractedRules:null
    },
    data: function () {
      return{
        fields: {
          name: { label: 'Name', sortable: true },
          ruleType: { label: 'Rule Type', sortable: true},
          data: { label: 'Extracted Data', sortable: true,}
        },
        // extractedRulesList: this.extractedRules,
      }
    },
    mounted(){
      // this.extractedRulesList = [ { "_cls": "ExtractedRule", "data": "PO# PO-00005", "name": "PO Number", "ruleType": "boundary" }, { "_cls": "ExtractedRule", "data": "AAA Company\n\n81/12 No 9 Lampakchee\nNongjok\n\nThailand", "name": "Adress", "ruleType": "boundary" } ]
    },
    methods: {
      // Convenience method to scroll a heading into view.
      // Not required for scrollspy to work
      // scrollIntoView (evt) {
      //   evt.preventDefault()
      //   const href = evt.target.getAttribute('href')
      //   const el = href ? document.querySelector(href) : null
      //   if (el) {
      //     this.$refs.content.scrollTop = el.offsetTop
      //   }
      // }
    }
  }
</script>

<style scoped>

</style>
