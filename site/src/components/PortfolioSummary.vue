<template>
  <div class="card border-primary">
    <div class="card-header">Total</div>
    <div class="card-body">
      <p class="card-text">Amount : {{ amount }}</p>
    </div>
  </div>
</template>

<script>
import { getAuth } from "firebase/auth";

export default {
    data() {
        return {
            amount : "..."
        }
    },
    async mounted() {
      const jConfig = await fetch("/config.json");
      const config = await jConfig.json();
      const uid = getAuth().currentUser.uid;
      const response = await fetch(
        `${config.apiUrl}/portfolio-summary/${uid}/EUR`
      );
      const rjson = await response.json();
      const amount = Number(rjson.total_amount);
      const currency = rjson.total_currency === "EUR" ? "€" : rjson.total_currency;

      this.amount = `${amount.toFixed(2)} ${currency} `;
    }
}
</script>
