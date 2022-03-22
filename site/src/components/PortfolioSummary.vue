<template>
  <div class="card border-primary">
    <div class="card-header">Portfolio</div>
    <div class="card-body">
      <p class="card-text">Amount : {{ amount }}</p>
    </div>
    <div class="card-footer text-muted">Updated to yesterday</div>
  </div>
</template>

<script>
export default {
    data() {
        return {
            amount : 1234.567
        }
    }
}
</script>
