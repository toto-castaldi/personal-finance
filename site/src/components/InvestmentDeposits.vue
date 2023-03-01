<template>
  <div class="card border-primary border-2">
    <div class="card-header">Investment deposits</div>
    <div class="card-body">
      <div class="table-responsive">
        <p class="card-text" v-if="amount">Total : {{ $n(amount, 'currency') }}</p>
        <p class="card-text" v-else>Total : ...</p>
        <table class="table">
          <thead>
            <tr>
              <th scope="col">Date</th>
              <th scope="col">Amount</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in movements" >
              <th scope="row">{{m.updated_at}}</th>
              <td>{{ $n(m.amount, 'currency') }}</td>
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
          `${config.apiUrl}/investment-deposit/${uid}/EUR`
        );
        const rjson = await response.json();

        this.amount = Number(rjson.total_amount);

        this.movements = rjson.movements.map(m => {
          m.updated_at = new Date(Date.parse(m.updated_at)).toLocaleDateString(navigator.language, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
          m.amount = Number(m.amount);
          return m;
        });
      }
    },
    async mounted() {
      this.update();
    }
}
</script>
