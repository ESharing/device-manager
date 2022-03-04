<template>
  <div>
    <h1>Email: <span>{{ email }}</span></h1>
    <button @click="fetchData">Get Random Email</button>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data() {
    return {
      schemas: {},
    };
  },
  methods: {
    async fetchData() {
      const res = (await this.axios.get('https://randomuser.me/api/')).data
        .results[0];
      this.schemas = res;
    },
  },
};
</script>