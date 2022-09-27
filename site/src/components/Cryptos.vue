<template>
  <div class="card border-primary border-2">
    <div class="card-header">Cryptos</div>
    <div class="card-body">
      <div class="table-responsive">  
        <p class="card-text">Value : {{amount}}</p>
        <table class="table">
          <thead>
            <tr>
              <th scope="col">Amount</th>
              <th scope="col">Crypto</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in assets" >
              <td>{{m.amount}}</td>
              <td>{{m.sub_type}}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { getAuth } from "firebase/auth";

export default {
  data() {
      return {
          amount : "...",
          assets : []
      }
  },
  methods : {
    async updateAmount() {
      const jConfig = await fetch("/config.json");
      const config = await jConfig.json();
      const uid = getAuth().currentUser.uid;
      const response = await fetch(`${config.apiUrl}/portfolio-summary/${uid}/1/CRYPTO/EUR`);
      const rjson = await response.json();
      const amount = Number(rjson.total_amount);
      const currency = rjson.total_currency === "EUR" ? "€" : rjson.total_currency;

      this.amount = `${amount.toFixed(2)} ${currency} `;
      this.assets = rjson.assets;
      
    }
  },
  async mounted() {
    this.updateAmount();
  }
}
</script>
