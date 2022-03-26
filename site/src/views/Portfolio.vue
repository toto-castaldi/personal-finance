<template>
  <div class="container mt-5">
    <div class="row mb-5">
      <div class="col-md-6">
        <PortfolioSummary />
      </div>
      <div class="col-md-6">
          <PortfolioDistribution />
      </div>
    </div>
    <div class="row mb-5">
      <div class="col-md-12">
          <PortfolioTrend />
      </div>
    </div>
  </div>
</template>

<script>
import PortfolioTrend from "../components/PortfolioTrend.vue";
import PortfolioSummary from "../components/PortfolioSummary.vue";
import PortfolioDistribution from "../components/PortfolioDistribution.vue";

export default {
    data() {
        return {}
    },
    components: {
      PortfolioTrend, PortfolioSummary, PortfolioDistribution
    }
}


</script>

