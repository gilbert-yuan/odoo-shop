<template>
  <section class="card panel">
    <h3>Delivery methods</h3>
    <p class="muted">Select carrier by ID, or pick one from the list.</p>

    <div v-if="items && items.length" class="items">
      <button
        v-for="item in items"
        :key="item.id"
        class="method button ghost"
        type="button"
        @click="$emit('set', item.id)"
      >
        <span>{{ item.name }}</span>
        <small>#{{ item.id }} · {{ item.delivery_type }}</small>
      </button>
    </div>

    <div class="set-row">
      <input v-model.number="carrierId" class="input" type="number" min="1" placeholder="Carrier ID" />
      <button class="button primary" type="button" @click="setMethod">
        Set method
      </button>
    </div>

    <details>
      <summary>Rendered delivery block</summary>
      <div class="raw" v-html="html"></div>
    </details>
  </section>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  html: {
    type: String,
    default: ""
  },
  items: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(["set"]);
const carrierId = ref(null);

function setMethod() {
  if (!carrierId.value) {
    return;
  }
  emit("set", carrierId.value);
}
</script>

<style scoped>
.panel {
  padding: 1rem;
  display: grid;
  gap: 0.8rem;
}

h3 {
  margin: 0;
}

.set-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.6rem;
}

.items {
  display: grid;
  gap: 0.45rem;
}

.method {
  display: grid;
  justify-items: start;
  border-radius: 12px;
  padding: 0.55rem 0.8rem;
}

.method small {
  color: var(--muted);
}

.raw {
  border: 1px dashed var(--line);
  border-radius: 12px;
  padding: 0.8rem;
  background: #fff;
}
</style>
