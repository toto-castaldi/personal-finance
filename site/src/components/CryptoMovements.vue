<template>
  <div class="card border-primary border-2">
    <div class="card-header">Crypto buiyng</div>
    <div class="card-body">
      <div class="table-responsive">
        <p class="card-text" v-if="amount">Total : {{ $n(amount, 'currency') }}</p>
        <p class="card-text" v-else>Total : ...</p>
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
              <td>{{ $n(m.native_amount_amount, 'currency') }}</td>
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
          amount : undefined,
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

        this.amount = Number(rjson.total_amount);

        this.movements = rjson.movements.map(m => {
          m.updated_at = new Date(Date.parse(m.updated_at)).toLocaleDateString(navigator.language, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
          m.native_amount_amount = Number(m.native_amount_amount);
          return m;
        });
      }
    },
    async mounted() {
      this.update();
    }
}
</script>
