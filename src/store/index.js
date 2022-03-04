import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    selectedSchema: '',
  },
  mutation: {
    setSelectedSchema (state, schema) {
      state.selectedSchema = schema
    },
  getters: {
    selectedSchema (state) {
      return state.selectedSchema
    },
  }

  }
})