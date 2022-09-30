<template>
  <div class="container mt-3 overflow-hidden">
    <div class="row gx-5">
      <div class="p-3 col">
        <InvestmentApr />
      </div>
    </div>
    <div class="row gx-5">
      <div class="p-3 col">
          <PortfolioTrend :levelInfo="newLevel" />
      </div>
    </div>  
  </div>
</template>

<script>
import InvestmentApr from "../components/InvestmentApr.vue";
import PortfolioTrend from "../components/PortfolioTrend.vue";


export default {
    data() {
        return {
          newLevel : { level : 1, node : "INVEST"}
        }
    },
    components: {
      InvestmentApr, PortfolioTrend
    },
    methods : {
    }
}
</script>

