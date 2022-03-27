<template>
  <div class="card border-primary border-2">
    <div class="card-header">Total</div>
    <div class="card-body">
      <p class="card-text">{{ amount }}</p>
    </div>
  </div>
</template>

<script>
import { getAuth } from "firebase/auth";

export default {
    props : ["levelInfo"],
    data() {
        return {
            amount : "...",
            lastLevelInfo : { level : -1, node : undefined}
        }
    },
    methods : {
      async updateAmount() {
        if (this.levelInfo.level != this.lastLevelInfo.level || this.levelInfo.node != this.lastLevelInfo.node) {
          this.lastLevelInfo = this.levelInfo;
          const jConfig = await fetch("/config.json");
          const config = await jConfig.json();
          const uid = getAuth().currentUser.uid;
          const response = await fetch(
            `${config.apiUrl}/portfolio-summary/${uid}/${this.lastLevelInfo.level}/${this.lastLevelInfo.node}/EUR`
          );
          const rjson = await response.json();
          const amount = Number(rjson.total_amount);
          const currency = rjson.total_currency === "EUR" ? "€" : rjson.total_currency;

          this.amount = `${amount.toFixed(2)} ${currency} `;
        }
      }
    },
    async mounted() {
      this.updateAmount();
    },
    updated() {
      this.updateAmount();
    }
}
</script>
