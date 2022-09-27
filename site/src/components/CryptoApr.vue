<template>
  <div class="card border-primary border-2">
    <div class="card-header">Crypto APR</div>
    <div class="card-body">
      <p class="card-text">{{ apr }} {{ delta }}</p>
    </div>
  </div>
</template>

<script>
import { getAuth } from "firebase/auth";

export default {
  data() {
      return {
          apr : "...",
          delta : "..."
      }
  },
  methods : {
    async updateAmount() {
      const jConfig = await fetch("/config.json");
      const config = await jConfig.json();
      const uid = getAuth().currentUser.uid;
      const response = await fetch(`${config.apiUrl}/crypto-apr/${uid}/EUR`);
      const rjson = await response.json();
      const currency = rjson.native_amount_currency === "EUR" ? "€" : rjson.native_amount_currency;

      let amount = Number(rjson.apr);
      this.apr = `${amount.toFixed(4)} %`;      

      amount = Number(rjson.delta);
      this.delta = `${amount.toFixed(4)} ${currency}`;      
    }
  },
  async mounted() {
    this.updateAmount();
  }
}
</script>
