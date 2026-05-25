<template>
  <section class="card panel">
    <h3>Payment</h3>

    <div v-if="tokens.length" class="tokens">
      <h4>Saved cards</h4>
      <label
        v-for="t in tokens"
        :key="t.id"
        class="option"
        :class="{ active: selectedTokenId === t.id }"
      >
        <input
          type="radio"
          name="payment-token"
          :value="t.id"
          :checked="selectedTokenId === t.id"
          @change="$emit('update:selectedTokenId', t.id); $emit('update:selectedProviderId', t.provider_id);"
        />
        <span class="info">
          <strong>{{ t.name }}</strong>
        </span>
      </label>
    </div>

    <div v-if="providers.length">
      <h4 v-if="tokens.length">Or pay with</h4>
      <div class="providers">
        <label
          v-for="p in providers"
          :key="p.id"
          class="option"
          :class="{ active: !selectedTokenId && selectedProviderId === p.id }"
        >
          <input
            type="radio"
            name="payment-provider"
            :value="p.id"
            :checked="!selectedTokenId && selectedProviderId === p.id"
            @change="$emit('update:selectedProviderId', p.id); $emit('update:selectedTokenId', null);"
          />
          <span class="info">
            <strong>{{ p.display_as || p.name }}</strong>
            <small>{{ p.code }}</small>
            <span v-if="p.pre_msg" class="muted small" v-html="p.pre_msg"></span>
          </span>
        </label>
      </div>
    </div>

    <p v-if="!providers.length && !tokens.length" class="muted">
      No payment provider available. Configure one in Odoo Apps → Payment.
    </p>

    <button
      class="button primary block"
      type="button"
      :disabled="disabled || (!selectedProviderId && !selectedTokenId)"
      @click="$emit('pay')"
    >
      {{ disabled ? "Processing…" : `Pay ${moneyAmount}` }}
    </button>
    <p v-if="error" class="error">{{ error }}</p>
  </section>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  providers: { type: Array, default: () => [] },
  tokens: { type: Array, default: () => [] },
  selectedProviderId: { type: Number, default: null },
  selectedTokenId: { type: Number, default: null },
  amount: { type: Number, default: 0 },
  currency: { type: String, default: "USD" },
  disabled: { type: Boolean, default: false },
  error: { type: String, default: "" }
});

defineEmits([
  "update:selectedProviderId",
  "update:selectedTokenId",
  "pay"
]);

const moneyAmount = computed(() =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: props.currency
  }).format(Number(props.amount || 0))
);
</script>

<style scoped>
.panel {
  padding: 1rem;
  display: grid;
  gap: 0.8rem;
}

h3,
h4 {
  margin: 0;
}

h4 {
  font-size: 0.85rem;
  color: var(--muted);
  font-weight: 500;
}

.tokens,
.providers {
  display: grid;
  gap: 0.45rem;
  margin-top: 0.35rem;
}

.option {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.6rem;
  align-items: center;
  padding: 0.65rem 0.8rem;
  border: 1px solid var(--line);
  border-radius: 12px;
  cursor: pointer;
}

.option:hover {
  border-color: var(--accent);
}

.option.active {
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

.block {
  width: 100%;
  padding: 0.7rem;
  font-size: 0.95rem;
}

.error {
  color: var(--danger);
  margin: 0;
}

.small {
  font-size: 0.78rem;
}
</style>
