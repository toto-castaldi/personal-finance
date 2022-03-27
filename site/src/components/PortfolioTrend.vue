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
    props: ["levelInfo"],
    data() {
        return {
            amount : "...",
            lastLevelInfo : { level : -1, node : undefined},
            chart : null
        }
    },
    methods : {
      async update() {
        if (this.levelInfo.level != this.lastLevelInfo.level || this.levelInfo.node != this.lastLevelInfo.node) {
          this.lastLevelInfo = this.levelInfo;
          const ratio = Math.floor(utils.mathMap(window.screen.availWidth, 300, 1920, 30, 120));
          const jConfig = await fetch("/config.json");
          const config = await jConfig.json();
          const uid = getAuth().currentUser.uid;
          const response = await fetch(
            `${config.apiUrl}/portfolio-values/${uid}/${this.lastLevelInfo.level}/${this.lastLevelInfo.node}/EUR/${ratio}`
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

          if (this.chart) {
              this.chart.destroy();
            }
          this.chart = new ApexCharts(this.$refs.chart, options);
          this.chart.render();
        }
      }
    },
    async mounted() {
      this.update();
    },
    updated() {
      this.update();
    }
}
</script>
<style scoped>
  div.card-body {
    min-height: 200px
  }
</style>
