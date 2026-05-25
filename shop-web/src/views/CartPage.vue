<template>
  <div class="container cart">
    <header class="head">
      <h1 class="section-title">{{ t("nav.cart") }}</h1>
      <p class="muted">
        {{ cartStore.quantity }} {{ t("nav.cart").toLowerCase() }}
        <span v-if="cartStore.mutating" class="updating">· updating…</span>
      </p>
    </header>

    <div v-if="cartStore.loading && !cartStore.initialized" class="card block">
      {{ t("common.loading") }}
    </div>
    <EmptyState
      v-else-if="!cartStore.lines.length"
      title="Your cart is empty"
      description="Browse products and add them to your cart."
      cta-to="/shop"
      cta-label="Go to shop"
    />
    <div v-else class="layout" :class="{ busy: cartStore.mutating }">
      <section class="grid">
        <CartLineItem
          v-for="line in cartStore.lines"
          :key="line.id"
          :line="line"
          :disabled="cartStore.mutating"
          @increase="increase"
          @decrease="decrease"
          @remove="removeLine"
        />
      </section>

      <aside class="card summary">
        <h3>Order Summary</h3>
        <div class="row">
          <span>{{ t("common.subtotal") }}</span>
          <strong>{{ money(cartStore.subtotal) }}</strong>
        </div>
        <div class="row total">
          <span>{{ t("common.total") }}</span>
          <strong>{{ money(cartStore.total) }}</strong>
        </div>
        <RouterLink class="button primary" to="/checkout">Proceed to checkout</RouterLink>
        <button
          class="button ghost"
          type="button"
          :disabled="cartStore.mutating"
          @click="clearCart"
        >
          Clear cart
        </button>
      </aside>
    </div>
    <p v-if="cartStore.error" class="error">{{ cartStore.error }}</p>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";

import CartLineItem from "../components/cart/CartLineItem.vue";
import EmptyState from "../components/shared/EmptyState.vue";
import { useCartStore } from "../stores/cart";
import { formatMoney } from "../utils/format";

const { t } = useI18n();
const cartStore = useCartStore();

onMounted(async () => {
  if (!cartStore.initialized) {
    await cartStore.refresh();
  }
});

function money(value) {
  return formatMoney(value);
}

async function increase(line) {
  await cartStore.setLineQty(line, line.quantity + 1);
}

async function decrease(line) {
  const next = Math.max(0, line.quantity - 1);
  await cartStore.setLineQty(line, next);
}

async function removeLine(line) {
  await cartStore.setLineQty(line, 0);
}

async function clearCart() {
  await cartStore.clear();
}
</script>

<style scoped>
.cart {
  display: grid;
  gap: 1rem;
  padding-top: 1rem;
}

.head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.updating {
  color: var(--accent);
  font-weight: 600;
  margin-left: 0.3rem;
}

.block {
  padding: 1rem;
}

.layout {
  display: grid;
  grid-template-columns: 1fr 310px;
  gap: 1rem;
  align-items: start;
  transition: opacity 0.2s;
}

.layout.busy {
  opacity: 0.85;
}

.summary {
  padding: 1rem;
  height: fit-content;
  display: grid;
  gap: 0.7rem;
  position: sticky;
  top: 90px;
}

h3 {
  margin: 0;
}

.row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.row.total {
  padding-top: 0.45rem;
  border-top: 1px solid var(--line);
  font-weight: 600;
}

.error {
  color: var(--danger);
  margin: 0;
}

@media (max-width: 980px) {
  .layout {
    grid-template-columns: 1fr;
  }
  .summary {
    position: static;
  }
}
</style>
