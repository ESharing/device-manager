<template>
<div>
  <v-card class="mx-auto" outlined>
    <v-card-actions>
      <v-btn small @click="getSchemaData">Query</v-btn>
      <v-btn small>Add</v-btn>
      <v-btn small>Edit</v-btn>
      <v-btn small>Delete</v-btn>
      <v-btn small @click="cleanTable">Clear</v-btn>
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
      this.items = []
      this.headers = []
      return axios({
          method: 'get',
          baseURL: '/api',
          url: `/schema-data?ip=${ip}&port=${port}&type=${type}&schema-name=${this.$store.state.selectedSchema}`,
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
