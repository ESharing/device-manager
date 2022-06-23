<template>
<v-app>
  <v-main>
<splitpanes class="default-theme" :dbl-click-splitter="false" style="height: 960px ">
    <pane size="15" min-size="10" max-size="50">
        <splitpanes horizontal>
            <pane min-size="10" max-size="90">
                <vuescroll :ops="ops">
                    <schema-tree-navi></schema-tree-navi>
                </vuescroll>
            </pane>
            <pane min-size="10">
                <vuescroll :ops="ops">
                    <object-tree-navi></object-tree-navi>
                </vuescroll>
            </pane>
        </splitpanes>
    </pane>
    <pane size="85" min-size="10" max-size="90">
        <splitpanes horizontal>
            <pane size=75 min-size=40>
                <splitpanes>
                    <pane size=100 min-size=40>
                      <data-table></data-table>
                    </pane>
                    <pane size=0>
                      <data-table></data-table>
                    </pane>
                    <pane size=0>
                    </pane>
                </splitpanes>
            </pane>
            <pane size=27>
                <p>TBD</p>
            </pane>
        </splitpanes>
    </pane>
</splitpanes>
  </v-main>
</v-app>
</template>

<script>
import {
    Splitpanes,
    Pane
} from 'splitpanes'
import 'splitpanes/dist/splitpanes.css'
import SchemaTreeNavi from './components/SchemaTreeNavi.vue'
import ObjectTreeNavi from './components/ObjectTreeNavi.vue'
import vuescroll from 'vuescroll'
import DataTable from './components/DataTable.vue'

export default {
    name: 'App',
    data() {
        return {
            ops: {
                vuescroll: {},
                scrollPanel: {},
                rail: {},
                bar: {
                    background: '#bbbebb',
                }
            }
        }
    },
    components: {
        Splitpanes,
        Pane,
        SchemaTreeNavi,
        ObjectTreeNavi,
        vuescroll,
        DataTable
    },
}
</script>