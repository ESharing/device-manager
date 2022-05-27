<template>
<v-card class="mx-auto" max-width="1000" height="6000">
  <v-text-field v-model="search" label="Search Schema" solo dense hide-details clearable clear-icon="mdi-close-circle-outline"></v-text-field>
  <v-card-text>
    <v-treeview activatable hoverable :dense="true" :multiple-active="false" :items="items" :search="search" :filter="filter" :open.sync="open" :active.sync="active">
      <template v-slot:prepend="{ item }">
        <v-icon v-if="item.children" v-text="`mdi-table-multiple`"></v-icon>
        <v-icon v-else v-text="`mdi-table`"></v-icon>
      </template>
    </v-treeview>
  </v-card-text>
</v-card>
</template>

<script>
import axios from 'axios';

import {
  isValidIPv4,
  isValidPort,
  getUrlKey
} from '@/utils/tools';

export default {
  name: "schema-tree-navi",
  data() {
    return {
      node_IP: '',
      node_type: '',
      items: [],
      active: [],
      open: [1, 2],
      search: null,
      caseSensitive: false,
    };
  },
  mounted() {
    //for element manager, ip from url; for network manager, ip from url query
    this.node_IP = getUrlKey('ip', window.location.href); // for network manager access, http://nms/?ip=x.x.x.x
    this.node_port = getUrlKey('port', window.location.href);
    this.node_type = getUrlKey('type', window.location.href);
    if (!isValidPort(this.node_port)) {
      alert('Port should be 1-65535')
    }
    if (this.node_IP === '')
      this.node_IP = window.location.hostname; // for element manager access, http://x.x.x.x
    if (isValidIPv4(this.node_IP)) {
      this.items = [];
      this.getSchema();
    } else
      alert('Please add valid IP address of the access Node in the url')
    if (this.node_type === '')
      alert('Please add type parameter in url')
  },
  watch: {
    active: function (newValue) {
      /*
      if (!this.active.length) 
        return 
      */
      //console.log("selected schema:" + this.items[newValue].name)
      //this.$store.state.selectedSchema = this.items[newValue].name;
      console.log("selected schema:" + newValue)
      this.$store.state.selectedSchema = newValue;
    }
  },
  computed: {
    filter() {
      return this.caseSensitive ?
        (item, search, textKey) => item[textKey].indexOf(search) > -1 :
        undefined
    },
  },
  methods: {
    async getSchema() {

      return axios({
          method: 'get',
          baseURL: '/api',
          url: `/yang-schemas?ip=${this.node_IP}&port=${this.node_port}&type=${this.node_type}`,
        })
        .then(response => {
          console.log("xxxxxx" + response.data);
          this.items = response.data.items;
        })
        .catch(() => {
          console.log("ERROR");
        });
    },
  },
  /*
  return
  },
  },
  */
}
</script>
