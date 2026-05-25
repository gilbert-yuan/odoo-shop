<template>
  <section class="card panel">
    <h3>Delivery method</h3>
    <p v-if="!items.length" class="muted">No delivery methods available.</p>
    <div v-else class="items">
      <label
        v-for="item in items"
        :key="item.id"
        class="method"
        :class="{ active: modelValue === item.id }"
      >
        <input
          :checked="modelValue === item.id"
          :value="item.id"
          name="delivery-method"
          type="radio"
          @change="$emit('update:modelValue', item.id)"
        />
        <span class="info">
          <strong>{{ item.name }}</strong>
          <small>{{ item.delivery_type || "" }}</small>
        </span>
        <span class="price">
          <template v-if="rates[item.id]?.success">{{ money(rates[item.id].price) }}</template>
          <template v-else-if="rates[item.id]?.error_message">
            <span class="error">{{ rates[item.id].error_message }}</span>
          </template>
          <template v-else>—</template>
        </span>
      </label>
    </div>
  </section>
</template>

<script setup>
import { onMounted, watch } from "vue";

const props = defineProps({
  items: { type: Array, default: () => [] },
  rates: { type: Object, default: () => ({}) },
  modelValue: { type: Number, default: null },
  currency: { type: String, default: "USD" }
});

const emit = defineEmits(["update:modelValue", "rate-request"]);

function money(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: props.currency
  }).format(Number(value || 0));
}

function requestRatesForAll() {
  props.items.forEach((item) => {
    if (!props.rates[item.id]) {
      emit("rate-request", item.id);
    }
  });
}

onMounted(requestRatesForAll);
watch(() => props.items.map((i) => i.id).join(","), requestRatesForAll);
</script>

<style scoped>
.panel {
  padding: 1rem;
  display: grid;
  gap: 0.7rem;
}

h3 {
  margin: 0;
}

.items {
  display: grid;
  gap: 0.5rem;
}

.method {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 0.7rem;
  align-items: center;
  padding: 0.7rem 0.9rem;
  border: 1px solid var(--line);
  border-radius: 12px;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
}

.method:hover {
  border-color: var(--accent);
}

.method.active {
  border-color: var(--accent);
  background: var(--accent-soft, #f0f7f4);
}

.info {
  display: grid;
  gap: 0.15rem;
}

.info small {
  color: var(--muted);
}

.price {
  font-weight: 600;
}

.price .error {
  color: var(--danger);
  font-weight: 400;
  font-size: 0.8rem;
}
</style>
