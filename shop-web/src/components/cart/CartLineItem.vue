<template>
  <article class="line card" :class="{ disabled }">
    <div class="meta">
      <h4>{{ line.name }}</h4>
      <p class="muted">Unit {{ money(line.unitPrice) }}</p>
    </div>
    <div class="qty">
      <button class="button ghost qty-btn" type="button" :disabled="disabled" @click="$emit('decrease', line)">-</button>
      <span>{{ line.quantity }}</span>
      <button class="button ghost qty-btn" type="button" :disabled="disabled" @click="$emit('increase', line)">+</button>
    </div>
    <div class="total">{{ money(line.total) }}</div>
    <button class="button ghost" type="button" :disabled="disabled" @click="$emit('remove', line)">Remove</button>
  </article>
</template>

<script setup>
import { formatMoney } from "../../utils/format";

defineProps({
  line: {
    type: Object,
    required: true
  },
  disabled: {
    type: Boolean,
    default: false
  }
});

defineEmits(["increase", "decrease", "remove"]);

function money(value) {
  return formatMoney(value);
}
</script>

<style scoped>
.line {
  padding: 1rem;
  display: grid;
  grid-template-columns: 2fr auto auto auto;
  gap: 0.8rem;
  align-items: center;
  transition: opacity 0.2s;
}

.line.disabled {
  opacity: 0.7;
}

.meta h4 {
  margin: 0;
}

.meta p {
  margin: 0.3rem 0 0;
}

.qty {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

.qty-btn {
  width: 34px;
  height: 34px;
  padding: 0;
  border-radius: 8px;
}

.total {
  font-weight: 700;
}

@media (max-width: 860px) {
  .line {
    grid-template-columns: 1fr;
  }
}
</style>
