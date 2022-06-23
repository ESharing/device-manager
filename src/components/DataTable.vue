<template>
<div>
  <v-card class="mx-auto" outlined>
    <v-card-actions>
      <v-btn small @click="getSchemaData">Query</v-btn>
      <v-btn disabled text v-show="isSelectedTable" right>{{tableLabel}}</v-btn>
      <!--
      <v-btn small @click="translateColumn" v-if="isUT">Translate</v-btn>
      <v-btn small>Add</v-btn>
      <v-btn small>Edit</v-btn>
      <v-btn small>Delete</v-btn>
      <v-btn small @click="cleanTable">Clear</v-btn>
      -->
    </v-card-actions>
  </v-card>
  <v-data-table 
    dense 
    :headers="headers" 
    :items="items" 
    item-key="name" 
    class="elevation-1" 
    height="600px" 
    fixed-header ></v-data-table>
</div>
</template>

<script>
import axios from 'axios';
import { getUrlKey } from '@/utils/tools';

export default {
  data: () => ({
    isSelectedTable: false,
    tableLabel: '',
    items: [],
    headers: [],
    /*
    items : [
      {
        name: 'Frozen Yogurt',
        calories: 159,
        fat: 6.0,
        carbs: 24,
        protein: 4.0,
        iron: '1%',
      },
      {
        name: 'KitKat',
        calories: 518,
        fat: 26.0,
        carbs: 65,
        protein: 7,
        iron: '6%',
      },
    ],
    headers: [
      {
        text: 'Dessert (100g serving)',
        align: 'start',
        sortable: false,
        value: 'name',
      },
      { text: 'Calories', value: 'calories' },
      { text: 'Fat (g)', value: 'fat' },
      { text: 'Carbs (g)', value: 'carbs' },
      { text: 'Protein (g)', value: 'protein' },
      { text: 'Iron (%)', value: 'iron' },
    ],
    */
  }),
  mounted: function() {
    //this.isUT = getUrlKey('type', window.location.href) === 'UT' ? true : false;
  },
  methods: {
    cleanTable: function () {
      this.items = []
      this.headers = []
    },
    getSchemaData: function () {
      const ip = getUrlKey('ip', window.location.href); 
      const port = getUrlKey('port',window.location.href);
      const type = getUrlKey('type', window.location.href); 
      if (this.$store.state.selectedSchema == '')
        return;
      this.isSelectedTable = true
      const schemaName = this.$store.state.selectedSchema
      this.tableLabel = schemaName[0].slice(schemaName[0].lastIndexOf('\\')+1)
      /*
      console.log(schemaName[0])
      console.log(this.tableLabel)
      */
      this.items = []
      this.headers = []
      return axios({
          method: 'get',
          baseURL: '/api',
          url: `/schema-data?ip=${ip}&port=${port}&type=${type}&schema-name=${schemaName}`,
        })
        .then(response => {
          this.items = response.data.items;
          this.headers = response.data.headers;
        })
        .catch(() => {
          console.log("Get Schema Data ERROR");
        });

    },
  }
}
</script>
