<template>
  <div class="container page">
    <EmptyState
      title="Page not found"
      description="The page you are looking for does not exist."
      cta-to="/"
      cta-label="Back home"
    />
  </div>
</template>

<script setup>
import EmptyState from "../components/shared/EmptyState.vue";
</script>

<style scoped>
.page {
  padding-top: 1rem;
}
</style>
