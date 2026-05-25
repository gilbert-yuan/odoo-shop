<template>
  <article class="container page rise-in">
    <header class="head">
      <h1>{{ title }}</h1>
      <p v-if="updated" class="muted small">Last updated: {{ updated }}</p>
    </header>
    <section class="card body">
      <slot>
        <p class="muted">Content coming soon.</p>
      </slot>
    </section>
  </article>
</template>

<script setup>
import { useHead } from "@unhead/vue";

const props = defineProps({
  title: { type: String, required: true },
  updated: { type: String, default: "" },
  description: { type: String, default: "" }
});

useHead({
  title: () => `${props.title} | NextPept`,
  meta: [
    { name: "description", content: () => props.description || props.title }
  ]
});
</script>

<style scoped>
.page {
  display: grid;
  gap: 1rem;
  padding-top: 1.5rem;
  max-width: 820px;
  margin-left: auto;
  margin-right: auto;
}

.head {
  display: grid;
  gap: 0.3rem;
}

h1 {
  margin: 0;
  font-size: clamp(1.6rem, 2.4vw, 2.2rem);
  letter-spacing: -0.02em;
}

.body {
  padding: 1.4rem clamp(1rem, 3vw, 2rem);
  line-height: 1.65;
}

.body :deep(h2) {
  margin: 1.4rem 0 0.5rem;
  font-size: 1.15rem;
}

.body :deep(h2:first-child) {
  margin-top: 0;
}

.body :deep(p) {
  margin: 0 0 0.9rem;
}

.body :deep(ul) {
  margin: 0 0 0.9rem;
  padding-left: 1.3rem;
}

.body :deep(li) {
  margin-bottom: 0.35rem;
}

.body :deep(a) {
  color: var(--accent);
}

.small {
  font-size: 0.82rem;
}
</style>
