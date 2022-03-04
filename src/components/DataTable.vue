<template>
<div>
  <v-card class="mx-auto" outlined>
    <v-card-actions>
      <v-btn small @click="getSchemaData">Query</v-btn>
      <v-btn small>Add</v-btn>
      <v-btn small>Edit</v-btn>
      <v-btn small>Delete</v-btn>
      <v-btn small>Clear</v-btn>
    </v-card-actions>
  </v-card>
  <v-data-table dense :headers="headers" :items="items" item-key="name" class="elevation-1"></v-data-table>
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
        name: 'Ice cream sandwich',
        calories: 237,
        fat: 9.0,
        carbs: 37,
        protein: 4.3,
        iron: '1%',
      },
      {
        name: 'Eclair',
        calories: 262,
        fat: 16.0,
        carbs: 23,
        protein: 6.0,
        iron: '7%',
      },
      {
        name: 'Cupcake',
        calories: 305,
        fat: 3.7,
        carbs: 67,
        protein: 4.3,
        iron: '8%',
      },
      {
        name: 'Gingerbread',
        calories: 356,
        fat: 16.0,
        carbs: 49,
        protein: 3.9,
        iron: '16%',
      },
      {
        name: 'Jelly bean',
        calories: 375,
        fat: 0.0,
        carbs: 94,
        protein: 0.0,
        iron: '0%',
      },
      {
        name: 'Lollipop',
        calories: 392,
        fat: 0.2,
        carbs: 98,
        protein: 0,
        iron: '2%',
      },
      {
        name: 'Honeycomb',
        calories: 408,
        fat: 3.2,
        carbs: 87,
        protein: 6.5,
        iron: '45%',
      },
      {
        name: 'Donut',
        calories: 452,
        fat: 25.0,
        carbs: 51,
        protein: 4.9,
        iron: '22%',
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
    getSchemaData: function () {
      const ip = getUrlKey('ip', window.location.href); 
      const type = getUrlKey('type', window.location.href); 
      if (this.$store.state.selectedSchema == '')
        return;
      return axios({
          method: 'get',
          baseURL: '/api',
          url: `/schema-data?ip=${ip}&type=${type}&schema-name=${this.$store.state.selectedSchema}`,
        })
        .then(response => {
          console.log("Schema Data:" + response.data);
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
