<template>
  <div class="card border-primary border-2">
    <div class="card-header">Crypto buiyng</div>
    <div class="card-body">
      <div class="table-responsive">
        <p class="card-text">Total : {{ amount }}</p>
        <table class="table">
          <thead>
            <tr>
              <th scope="col">Date</th>
              <th scope="col">Provider</th>
              <th scope="col">Fiat</th>
              <th scope="col">Crypto amount</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in movements" :key="m.id">
              <th scope="row">{{m.updated_at}}</th>
              <td>{{m.provider}}</td>
              <td>{{m.native_amount_amount}}</td>
              <td>{{m.crypto_amount_currency}} {{m.crypto_amount_amount}}</td>
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
          movements : []
        }
    },
    methods : {
      async update() {
        this.lastLevelInfo = this.levelInfo;
        const jConfig = await fetch("/config.json");
        const config = await jConfig.json();
        const uid = getAuth().currentUser.uid;
        const response = await fetch(
          `${config.apiUrl}/crypto-buying/${uid}/EUR`
        );
        const rjson = await response.json();

        console.log(rjson);

        const amount = Number(rjson.total_amount);
        const currency = rjson.total_currency === "EUR" ? "€" : rjson.total_currency;
        this.amount = `${amount.toFixed(2)} ${currency} `;

        this.movements = rjson.movements.map(m => {
          const amount = Number(m.native_amount_amount);
          const currency = m.native_amount_currency === "EUR" ? "€" : m.native_amount_currency;
          m.native_amount_amount = `${amount.toFixed(2)} ${currency} `;
          return m;
        });
      }
    },
    async mounted() {
      this.update();
    }
}
</script>
