<script lang="ts">
import { RouterLink, RouterView } from "vue-router";
import { onMounted, defineComponent } from "vue";

export default defineComponent({
  setup() {
    onMounted(async () => {
      const resp = await fetch("/config.json");
    })
  }
})
</script>

<template>
  <header>
    
    <div>
      <h1>Personal Finance</h1>

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/portfolio">Portfolio</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView></RouterView>
</template>

<style>


</style>
