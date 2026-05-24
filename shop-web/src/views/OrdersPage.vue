<template>
  <div class="container orders">
    <header class="head">
      <h1 class="section-title">Orders</h1>
      <p class="muted">Customer order history from Odoo.</p>
    </header>

    <EmptyState
      v-if="!sessionStore.isLoggedIn"
      title="Sign in required"
      description="Order history is only available for authenticated customers."
      cta-to="/account"
      cta-label="Sign in"
    />
    <div v-else class="layout">
      <section class="card list">
        <h3>Recent orders</h3>
        <div v-if="ordersStore.loading" class="muted">Loading orders...</div>
        <EmptyState
          v-else-if="!ordersStore.orders.length"
          title="No orders yet"
          description="Orders will appear here once checkout is completed."
        />
        <button
          v-for="order in ordersStore.orders"
          v-else
          :key="order.id"
          class="order-row"
          type="button"
          @click="selectOrder(order.id)"
        >
          <div>
            <strong>{{ order.name }}</strong>
            <p class="muted">{{ order.state }} • {{ order.dateOrder || "N/A" }}</p>
          </div>
          <strong>{{ money(order.amountTotal) }}</strong>
        </button>
      </section>

      <section class="card detail">
        <h3>Order lines</h3>
        <div v-if="!ordersStore.selectedOrderId" class="muted">
          Select an order to inspect lines.
        </div>
        <ul v-else-if="ordersStore.selectedOrderLines.length">
          <li v-for="line in ordersStore.selectedOrderLines" :key="line.id">
            <span>{{ line.name }} x{{ line.quantity }}</span>
            <strong>{{ money(line.total) }}</strong>
          </li>
        </ul>
        <p v-else class="muted">No lines found.</p>
      </section>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";

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

async function selectOrder(orderId) {
  await ordersStore.selectOrder(orderId);
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

.layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.list,
.detail {
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
  padding: 0.7rem;
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  cursor: pointer;
}

.order-row p {
  margin: 0.22rem 0 0;
}

ul {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 0.5rem;
}

li {
  display: flex;
  justify-content: space-between;
}

@media (max-width: 960px) {
  .layout {
    grid-template-columns: 1fr;
  }
}
</style>
