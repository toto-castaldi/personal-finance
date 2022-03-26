<template>
  <div class="card border-primary">
    <div class="card-header">Distribution</div>
    <div class="card-body">
      <div ref="pie"></div>
    </div>
    <div class="card-footer text-muted">Updated to yesterday</div>
  </div>
</template>

<script>
import { getAuth } from "firebase/auth";
import ApexCharts from 'apexcharts'

export default {
    data() {
        return {
            amount : "..."
        }
    },
    async mounted() {
      const jConfig = await fetch("/config.json");
      const config = await jConfig.json();
      const uid = getAuth().currentUser.uid;
      const response = await fetch(
        `${config.apiUrl}/portfolio-summary/${uid}/EUR`
      );
      const rjson = await response.json();

      const consolidated = {};

      for (const asset of rjson.assets) {
        console.log(asset);
        let total = 0;
        let assetType = asset.type;
        if (assetType in consolidated) {
          total = consolidated[assetType];
        }
        total += Number(asset.native_amount);
        consolidated[assetType] = total;
      }

      console.log(consolidated);

      const options = {
        series: Object.values(consolidated),
        chart: {
          height: 200,
          type: 'pie',
        },
        labels: Object.keys(consolidated),
        responsive: [{
          breakpoint: 480,
          options: {
            chart: {
            
            },
            legend: {
              position: 'bottom'
            }
          }
        }]
        };

        const chart = new ApexCharts(this.$refs.pie, options);
        chart.render();
    }
}
</script>
<style scoped>
  div.card-body {
    min-height: 200px
  }
</style>
