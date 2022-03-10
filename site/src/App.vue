<script lang="ts">
import { RouterLink, RouterView } from "vue-router";
import { onMounted, defineComponent } from "vue";

export default defineComponent({
  setup() {
    onMounted(async () => {
      const resp = await fetch("/config.json");
    });
  },
});
</script>

<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-desk bg-dark">
      <div class="container">
        <a class="navbar-brand" href="/">Personal Finance</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <RouterLink class="nav-link active" to="/">Home</RouterLink>
            </li>
            
          </ul>
          
        </div>
      </div>
    </nav>
  </header>

  <RouterView></RouterView>
</template>

<style></style>
