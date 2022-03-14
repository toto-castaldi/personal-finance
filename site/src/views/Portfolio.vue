<script setup>
import PortfolioTrend from "../components/PortfolioTrend.vue";
</script>

<template>
  <div class="container mt-5">
    <div class="row">
      <div class="col-md-12">
        <div class="card border-primary">
          <div class="card-header">Portfolio</div>
          <portfolio-trend></portfolio-trend>
          <div class="card-body">
            <p class="card-text">This is the trend of your Portfolio</p>
          </div>
          <div class="card-footer text-muted">Updated to yesterday</div>
        </div>
      </div>
    </div>
  </div>
</template>
