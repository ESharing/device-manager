<template>
  <v-card
    class="mx-auto"
    max-width="1000"
    height="3000"
  >
      <v-text-field
        v-model="search"
        label="Search Object"
        solo
        dense
        hide-details
        clearable
        clear-icon="mdi-close-circle-outline"
      ></v-text-field>
    <v-card-text>
      <v-treeview
        activatable
        hoverable
        :dense="true"
        :items="items"
        :search="search"
        :filter="filter"
        :open.sync="open"
      >
        <template v-slot:prepend="{ item }">
          <!--v-icon
            v-if="item.name.indexOf('Slot') === 0"
            v-text="`mdi-pine-tree`"
          ></v-icon>
          <v-icon
            v-else
            v-text="`mdi-leaf`"
          ></v-icon-->
          <v-icon
            v-if="item.name.indexOf('Slot') === 0"
            v-text="`mdi-folder`"
          ></v-icon>
          <v-icon
            v-else
          >{{ svgPath }}</v-icon>
        </template>
      </v-treeview>
    </v-card-text>
  </v-card>
</template>

<script>
import axios from 'axios';
import { isValidIPv4,getUrlKey } from '@/utils/tools';
import { mdiEthernet } from '@mdi/js';

  export default {
    name: "object-tree-navi",
    data() {
      return {
      node_IP: '',
      node_type: '',
      svgPath: mdiEthernet,
      items: [],
      open: [1, 2],
      search: null,
      caseSensitive: false,
    };
  },
  mounted() {
    this.node_IP = getUrlKey('ip',window.location.href);
    this.node_type = getUrlKey('type',window.location.href); 
    if ( isValidIPv4(this.node_IP) ) { 
      this.items = [];
      this.getObjects();
    }
    else
      alert('Please input valid IP address of the access Node.')
    if ( this.node_type === '') 
      alert('Please add type parameter in url')
  },
    computed: {
      filter () {
        return this.caseSensitive
          ? (item, search, textKey) => item[textKey].indexOf(search) > -1
          : undefined
      },
    },
    methods: {
    async getObjects() {
      return axios({
        method: 'get',
        baseURL: '/api',
        url: `/objects?ip=${this.node_IP}&type=${this.node_type}`,
      })
        .then( response => {
          console.log("xxxxxx" + response.data );
          this.items = response.data.items;
        })
        .catch(() => {
          console.log("ERROR");
        });
    },
    },
  }
</script>