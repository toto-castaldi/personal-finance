<template>
  <div class="container mt-3 overflow-hidden">
    <div class="row gx-5">
      <div class="p-3 col">
          <PortfolioLevel />
      </div>
    </div>
    <div class="row gx-5">
      <div class="p-3 col-md-4">
        <PortfolioSummary />
      </div>
      <div class="p-3 col-md-8">
          <PortfolioDistribution />
      </div>
    </div>
    <div class="row gx-5">
      <div class="p-3 col">
          <PortfolioTrend />
      </div>
    </div>    
  </div>
</template>

<script>
import PortfolioTrend from "../components/PortfolioTrend.vue";
import PortfolioSummary from "../components/PortfolioSummary.vue";
import PortfolioDistribution from "../components/PortfolioDistribution.vue";
import PortfolioLevel from "../components/PortfolioLevel.vue";

export default {
    data() {
        return {}
    },
    components: {
      PortfolioTrend, PortfolioSummary, PortfolioDistribution, PortfolioLevel
    }
}


</script>

