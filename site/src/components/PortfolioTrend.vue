<template>
  <LineChart :chartData="state.data" />
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
      const jConfig = await fetch("/config.json");
      const config = await jConfig.json();
      const uid = getAuth().currentUser.uid;
      const response = await fetch(
        `${config.apiUrl}/portfolio-values/${uid}/EUR`
      );
      const rjson = await response.json();
      const labels = [];
      const dataset = {
        label: "Crypto",
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
