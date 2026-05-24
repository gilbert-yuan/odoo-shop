<template>
  <div class="container cart">
    <header class="head">
      <h1 class="section-title">Cart</h1>
      <p class="muted">{{ cartStore.quantity }} items</p>
    </header>

    <div v-if="cartStore.loading" class="card block">Loading cart...</div>
    <EmptyState
      v-else-if="!cartStore.lines.length"
      title="Your cart is empty"
      description="Browse products and add them to your cart."
      cta-to="/shop"
      cta-label="Go to shop"
    />
    <div v-else class="layout">
      <section class="grid">
        <CartLineItem
          v-for="line in cartStore.lines"
          :key="line.id"
          :line="line"
          @increase="increase"
          @decrease="decrease"
          @remove="removeLine"
        />
      </section>

      <aside class="card summary">
        <h3>Order Summary</h3>
        <div class="row">
          <span>Subtotal</span>
          <strong>{{ money(cartStore.subtotal) }}</strong>
        </div>
        <div class="row total">
          <span>Total</span>
          <strong>{{ money(cartStore.total) }}</strong>
        </div>
        <RouterLink class="button primary" to="/checkout">Proceed to checkout</RouterLink>
        <button class="button ghost" type="button" @click="clearCart">Clear cart</button>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { RouterLink } from "vue-router";

import CartLineItem from "../components/cart/CartLineItem.vue";
import EmptyState from "../components/shared/EmptyState.vue";
import { useCartStore } from "../stores/cart";

const cartStore = useCartStore();

onMounted(async () => {
  await cartStore.refresh();
});

function money(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD"
  }).format(Number(value || 0));
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

.block {
  padding: 1rem;
}

.layout {
  display: grid;
  grid-template-columns: 1fr 310px;
  gap: 1rem;
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
}

@media (max-width: 980px) {
  .layout {
    grid-template-columns: 1fr;
  }
}
</style>
