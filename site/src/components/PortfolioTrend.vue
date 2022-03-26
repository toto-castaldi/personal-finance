<template>
  <div class="card border-primary border-2">
    <div class="card-header">Trend</div>
    <div class="card-body">
      <div ref="chart"></div>
    </div>
  </div>
</template>

<script>
import { getAuth } from "firebase/auth";
import ApexCharts from 'apexcharts'
import utils from "../utils.js";

export default {
    data() {
        return {
            amount : "..."
        }
    },
    async mounted() {
      const ratio = Math.floor(utils.mathMap(window.screen.availWidth, 300, 1920, 30, 120));
      const jConfig = await fetch("/config.json");
      const config = await jConfig.json();
      const uid = getAuth().currentUser.uid;
      const response = await fetch(
        `${config.apiUrl}/portfolio-values/${uid}/EUR/${ratio}`
      );
      const rjson = await response.json();

      const data = [];
      const categories = [];

      if (utils.isIterable(rjson)) {
        for (const r of rjson) {
          if (r.total_amount != null) {
            categories.push(r.the_date);
            data.push(Number(r.total_amount).toFixed(0));
          }
        }
      }

      const options = {
        series: [{
            name: "Total",
            data
        }],
          chart: {
          height: 350,
          type: 'line',
          zoom: {
            enabled: false
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: 'straight'
        },
        grid: {
          row: {
            colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
          },
        },
        xaxis: {
          categories
        }
      };

      const chart = new ApexCharts(this.$refs.chart, options);
      chart.render();
    }
}
</script>
<style scoped>
  div.card-body {
    min-height: 200px
  }
</style>
