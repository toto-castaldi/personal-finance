<template>
  <div class="card border-primary">
    <div class="card-header">Portfolio</div>
    <div class="card-body">
      <p class="card-text">Amount : {{ amount }}</p>
    </div>
    <div class="card-footer text-muted">Updated to yesterday</div>
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

      this.amount = `${amount} ${rjson.total_currency} `;
    }
}
</script>
