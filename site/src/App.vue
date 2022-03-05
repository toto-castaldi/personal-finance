<script setup>
import { RouterLink, RouterView } from "vue-router";
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
