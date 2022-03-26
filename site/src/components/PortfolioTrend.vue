<template>
  <div class="card border-primary">
    <div class="card-header">Trend</div>
      <LineChart :chartData="state.data" />
    <div class="card-body">
    </div>
    <div class="card-footer text-muted">Updated to yesterday</div>
  </div>
</template>

<script lang="ts">
import { onMounted, reactive, defineComponent } from "vue";
import { LineChart } from "vue-chart-3";
import { Chart, registerables } from "chart.js";
import { getAuth } from "firebase/auth";
import utils from "../utils.js";


Chart.register(...registerables);

export default defineComponent({
  components: { LineChart },
  setup() {
    const state = reactive({
      data: null,
    });

    onMounted(async () => {
      const ratio = Math.floor(utils.mathMap(window.screen.availWidth, 300, 1920, 30, 120));
      const jConfig = await fetch("/config.json");
      const config = await jConfig.json();
      const uid = getAuth().currentUser.uid;
      const response = await fetch(
        `${config.apiUrl}/portfolio-values/${uid}/EUR/${ratio}`
      );
      const rjson = await response.json();
      const labels = [];
      const dataset = {
        label: "",
        data: [],
        fill: false,
        borderColor: "rgb(75, 192, 192)",
        tension: 0.1,
      };
      if (utils.isIterable(rjson)) {
        for (const r of rjson) {
          if (r.total_amount != null) {
            labels.push(r.the_date);
            dataset.data.push(r.total_amount);
          }
        }
      }

      state.data = {
        datasets: [dataset],
        labels,
      };
    });

    return {
      state,
    };
  },
});
</script>
