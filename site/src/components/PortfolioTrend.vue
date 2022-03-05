<template>
  <LineChart :chartData="state.data" />
</template>

<script lang="ts">
import { onMounted, reactive, defineComponent } from "vue";
import { LineChart } from 'vue-chart-3';
import { Chart, registerables } from "chart.js";


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
      const response = await fetch(`${config.apiUrl}/portfolio-values/nhriZ1orHofgLw72aiEmZoBBEOs2/EUR`);
      const rjson = await response.json();
      const labels = [];
      const dataset = {
        label: 'Porfolio',
        data : [],
        fill : false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      };
      for (const r of rjson) {
        labels.push(r.the_date);
        dataset.data.push(r.total_amount ? r.total_amount : 0);
      }
      
      state.data = {
        datasets: [dataset],
        labels
      };
    });

    

    return {
      state
    };
  },
});
</script>