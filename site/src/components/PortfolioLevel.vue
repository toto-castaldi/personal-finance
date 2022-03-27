<template>
  <div class="card border-primary border-2">
    <div class="card-header">Components</div>
    <div class="card-body">
      <p class="card-text">
        <div class="btn-toolbar" role="toolbar" aria-label="Toolbar with button groups">
          <div class="btn-group me-2" role="group" aria-label="Navigation">
            <button type="button" class="btn btn-success" :disabled="level == 0" @click="decLevel" ><i class="bi bi-box-arrow-up"></i></button>
          </div>
          <div class="btn-group me-2" role="group" aria-label="Nodes">
            <button v-for="node in nodes" type="button" class="btn btn-secondary" @click="incLevel(node)" :disabled="level == 2 || nodes.length < 2" >{{node}}</button>
          </div>
          
        </div>
      </p>
    </div>
  </div>
</template>

<script>
import { getAuth } from "firebase/auth";

export default {
    data() {
        return {
            level : 0,
            nodes : [],
            parent : null
        }
    },
    methods: {
      async decLevel() {
        if (this.level == 1) this.parent = null;
        this.level --;
        this.updateNodes(this.parent);
      },
      async incLevel(node) {
        if (this.level == 0) this.parent = node;
        this.level ++;
        this.updateNodes(node);
      },
      async updateNodes(node) {
        this.$emit("changeLevel", { level : this.level, node });
        if (this.level == 2) {
          this.nodes = [node];
        } else {
          const jConfig = await fetch("/config.json");
          const config = await jConfig.json();
          const uid = getAuth().currentUser.uid;
          const n = node ? node : 'fake';
          const response = await fetch(
            `${config.apiUrl}/portfolio-level/${uid}/${this.level}/${n}`
          );
          const rjson = await response.json();
          this.nodes = rjson;
        }
      }
    },
    async mounted() {
      this.updateNodes()
    }
}
</script>
