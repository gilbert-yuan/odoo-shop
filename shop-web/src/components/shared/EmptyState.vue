<template>
  <div class="card empty">
    <h3>{{ title }}</h3>
    <p class="muted">{{ description }}</p>
    <RouterLink v-if="ctaTo" :to="ctaTo" class="button primary">
      {{ ctaLabel }}
    </RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";

defineProps({
  title: {
    type: String,
    default: "Nothing here yet"
  },
  description: {
    type: String,
    default: "Once data is available, it will appear here."
  },
  ctaTo: {
    type: String,
    default: ""
  },
  ctaLabel: {
    type: String,
    default: "Browse shop"
  }
});
</script>

<style scoped>
.empty {
  padding: 1.3rem;
  display: grid;
  gap: 0.7rem;
  justify-items: start;
}

h3 {
  margin: 0;
}

p {
  margin: 0;
}
</style>
