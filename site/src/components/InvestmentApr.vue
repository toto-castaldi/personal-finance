<template>
  <div class="card border-primary border-2">
    <div class="card-header">Ivestment APR</div>
    <div class="card-body">
      <p class="card-text" v-if="apr">Apr : {{ $n(apr/100, 'percent') }}</p>
      <p class="card-text" v-else>Apr : ...</p>
      <p class="card-text" v-if="delta">Delta : {{ $n(delta, 'currency') }}</p>
      <p class="card-text" v-else>Delta : ...</p>
    </div>
  </div>
</template>

<script>
import { getAuth } from "firebase/auth";

export default {
  data() {
      return {
          apr : undefined,
          delta : undefined
      }
  },
  methods : {
    async updateAmount() {
      const jConfig = await fetch("/config.json");
      const config = await jConfig.json();
      const uid = getAuth().currentUser.uid;
      const response = await fetch(`${config.apiUrl}/investment-apr/${uid}/EUR`);
      const rjson = await response.json();
      this.apr = Number(rjson.apr);      
      this.delta = Number(rjson.delta);
    }
  },
  async mounted() {
    this.updateAmount();
  }
}
</script>
