<template>
  <div class="card border-primary border-2">
    <div class="card-header">Crypto APR</div>
    <p class="card-text">{{apr}}</p>
  </div>
</template>

<script>
import { getAuth } from "firebase/auth";

export default {
  data() {
      return {
          apr : "..."
      }
  },
  methods : {
    async updateAmount() {
      const jConfig = await fetch("/config.json");
      const config = await jConfig.json();
      const uid = getAuth().currentUser.uid;
      const response = await fetch(`${config.apiUrl}/crypto-apr/${uid}/EUR`);
      const rjson = await response.json();
      const amount = Number(rjson.apr);

      this.apr = `${amount.toFixed(4)} %`;      
    }
  },
  async mounted() {
    this.updateAmount();
  }
}
</script>
