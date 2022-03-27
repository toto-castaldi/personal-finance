<template>
  <div class="card border-primary border-2">
    <div class="card-header">Distribution</div>
    <div class="card-body">
      <div ref="pie"></div>
    </div>
  </div>
</template>

<script>
import { getAuth } from "firebase/auth";
import ApexCharts from 'apexcharts'

export default {
    props : ["levelInfo"],
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
          const jConfig = await fetch("/config.json");
          const config = await jConfig.json();
          const uid = getAuth().currentUser.uid;
          const response = await fetch(
            `${config.apiUrl}/portfolio-summary/${uid}/${this.lastLevelInfo.level}/${this.lastLevelInfo.node}/EUR`
          );
          const rjson = await response.json();

          const consolidated = {};

          for (const asset of rjson.assets) {
            let total = 0;
            let assetType = this.lastLevelInfo.level == 0 ? asset.type : asset.sub_type;
            if (assetType in consolidated) {
              total = consolidated[assetType];
            }
            total += Number(asset.native_amount);
            consolidated[assetType] = total;
          }

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

          if (this.chart) {
            this.chart.destroy();
          }
          this.chart = new ApexCharts(this.$refs.pie, options);
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
