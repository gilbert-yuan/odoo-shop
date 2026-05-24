<template>
  <div class="container compare">
    <header class="head">
      <h1 class="section-title">Compare</h1>
      <p class="muted">Compare up to 4 products side by side.</p>
    </header>

    <EmptyState
      v-if="!compareStore.ids.length"
      title="No products in compare list"
      description="Use the compare action from catalog cards."
      cta-to="/shop"
      cta-label="Browse catalog"
    />
    <section v-else class="grid cards">
      <article v-for="entry in compareStore.entries" :key="entry.id" class="card item">
        <h3>{{ entry.display_name || entry.name }}</h3>
        <p class="muted">ID: {{ entry.id }}</p>
        <RouterLink class="button ghost" :to="`/product/${entry.id}`">View product</RouterLink>
      </article>
    </section>

    <button v-if="compareStore.ids.length" class="button ghost" type="button" @click="compareStore.clear">
      Clear compare list
    </button>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { RouterLink } from "vue-router";

import EmptyState from "../components/shared/EmptyState.vue";
import { useCompareStore } from "../stores/compare";

const compareStore = useCompareStore();

onMounted(async () => {
  await compareStore.refreshData();
});
</script>

<style scoped>
.compare {
  display: grid;
  gap: 1rem;
  padding-top: 1rem;
}

.head {
  display: grid;
  gap: 0.3rem;
}

.cards {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.item {
  padding: 0.9rem;
  display: grid;
  gap: 0.6rem;
}

.item h3 {
  margin: 0;
}

.item p {
  margin: 0;
}

@media (max-width: 1120px) {
  .cards {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .cards {
    grid-template-columns: 1fr;
  }
}
</style>
