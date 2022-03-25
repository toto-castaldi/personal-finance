<template>
  <div class="container mt-5">
    <div class="row mb-5">
      <div class="col-md-12">
        <PortfolioSummary />
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
          <PortfolioTrend />
      </div>
    </div>
  </div>
</template>

<script>
import PortfolioTrend from "../components/PortfolioTrend.vue";
import PortfolioSummary from "../components/PortfolioSummary.vue";

export default {
    data() {
        return {}
    },
    components: {
      PortfolioTrend, PortfolioSummary
    }
}


</script>

