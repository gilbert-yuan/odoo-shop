<template>
  <div class="container orders">
    <header class="head">
      <h1 class="section-title">Orders</h1>
      <p class="muted">Your order history.</p>
    </header>

    <EmptyState
      v-if="!sessionStore.isLoggedIn"
      title="Sign in required"
      description="Order history is only available for authenticated customers."
      cta-to="/account"
      cta-label="Sign in"
    />
    <section v-else class="card list">
      <h3>Recent orders</h3>
      <div v-if="ordersStore.loading" class="muted">Loading orders…</div>
      <EmptyState
        v-else-if="!ordersStore.orders.length"
        title="No orders yet"
        description="Orders will appear here once checkout is completed."
      />
      <RouterLink
        v-for="order in ordersStore.orders"
        v-else
        :key="order.id"
        :to="`/account/orders/${order.id}`"
        class="order-row"
      >
        <div>
          <strong>{{ order.name }}</strong>
          <p class="muted">{{ order.state }} · {{ order.dateOrder || "N/A" }}</p>
        </div>
        <strong>{{ money(order.amountTotal) }}</strong>
      </RouterLink>
    </section>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { RouterLink } from "vue-router";

import EmptyState from "../components/shared/EmptyState.vue";
import { useOrdersStore } from "../stores/orders";
import { useSessionStore } from "../stores/session";

const ordersStore = useOrdersStore();
const sessionStore = useSessionStore();

onMounted(async () => {
  if (sessionStore.isLoggedIn) {
    await ordersStore.refresh();
  }
});

function money(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD"
  }).format(Number(value || 0));
}
</script>

<style scoped>
.orders {
  display: grid;
  gap: 1rem;
  padding-top: 1rem;
}

.head {
  display: grid;
  gap: 0.3rem;
}

.list {
  padding: 1rem;
  display: grid;
  gap: 0.7rem;
  align-content: start;
}

h3 {
  margin: 0;
}

.order-row {
  width: 100%;
  text-align: left;
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 0.7rem 1rem;
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  text-decoration: none;
  color: inherit;
  transition: border-color 0.15s;
}

.order-row:hover {
  border-color: var(--accent);
}

.order-row p {
  margin: 0.22rem 0 0;
}
</style>
