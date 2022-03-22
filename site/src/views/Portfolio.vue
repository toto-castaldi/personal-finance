<template>
  <div class="container mt-5">
    <div class="row mb-5">
      <div class="col-md-12">
        <PortfolioSummary />
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <div class="card border-primary">
          <div class="card-header">Trend</div>
          <PortfolioTrend />
          <div class="card-body">
            <p class="card-text">This is the trend of your Portfolio</p>
          </div>
          <div class="card-footer text-muted">Updated to yesterday</div>
        </div>
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

