<template>
  <div class="container done">
    <header class="hero card">
      <div class="badge" :class="statusClass">{{ statusBadge }}</div>
      <h1>{{ statusTitle }}</h1>
      <p class="muted">{{ statusSubtitle }}</p>
    </header>

    <div v-if="order" class="layout">
      <section class="card">
        <header class="row between">
          <h3>Order {{ order.name }}</h3>
          <span class="muted small">{{ order.date_order || "" }}</span>
        </header>
        <ul class="lines">
          <li v-for="line in order.lines || []" :key="line.id">
            <span>{{ line.name }} × {{ line.quantity }}</span>
            <strong>{{ money(line.price_total) }}</strong>
          </li>
        </ul>
        <div class="row total">
          <span>Total</span>
          <strong>{{ money(order.amount_total) }}</strong>
        </div>
      </section>

      <section v-if="order.billing_address || order.shipping_address" class="card addr-grid">
        <div v-if="order.billing_address">
          <h4>Billing</h4>
          <AddressDisplay :address="order.billing_address" />
        </div>
        <div v-if="order.shipping_address">
          <h4>Shipping</h4>
          <AddressDisplay :address="order.shipping_address" />
        </div>
      </section>

      <section v-if="order.carrier" class="card row between">
        <span><strong>Delivery:</strong> {{ order.carrier.name }}</span>
        <span class="muted small">{{ order.carrier.delivery_type }}</span>
      </section>

      <section v-if="order.payment" class="card row between">
        <span>
          <strong>Payment:</strong> {{ order.payment.provider_name || order.payment.provider_code }}
        </span>
        <span :class="['tag', `tag-${order.payment.state}`]">{{ order.payment.state }}</span>
      </section>
    </div>

    <div class="actions">
      <RouterLink class="button primary" :to="`/account/orders/${orderId}`">View order</RouterLink>
      <RouterLink class="button ghost" to="/shop">Continue shopping</RouterLink>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue";
import { RouterLink, useRoute } from "vue-router";

import { odooApi } from "../services/odooApi";

const DONE_STATES = ["done", "authorized"];
const FINAL_STATES = ["done", "authorized", "cancel", "error"];

const AddressDisplay = {
  props: { address: { type: Object, required: true } },
  template: `
    <p class="addr">
      <strong>{{ address.name }}</strong><br />
      {{ address.street }}<template v-if="address.street2">, {{ address.street2 }}</template><br />
      {{ address.city }} {{ address.zip }} {{ address.state_name }}<br />
      {{ address.country_name }}
      <template v-if="address.phone"><br />{{ address.phone }}</template>
    </p>
  `
};

const route = useRoute();
const orderId = computed(() => Number(route.params.orderId));
const accessToken = computed(() => route.query.access_token || null);

const order = ref(null);
const txState = ref("");
const error = ref("");
let pollTimer = null;
let pollCount = 0;

const statusBadge = computed(() => {
  if (DONE_STATES.includes(txState.value)) return "Paid";
  if (txState.value === "pending") return "Pending";
  if (txState.value === "error") return "Failed";
  if (txState.value === "cancel") return "Cancelled";
  return "Processing";
});

const statusClass = computed(() => {
  if (DONE_STATES.includes(txState.value)) return "success";
  if (txState.value === "error") return "danger";
  if (txState.value === "cancel") return "warn";
  return "info";
});

const statusTitle = computed(() => {
  if (DONE_STATES.includes(txState.value)) return "Thank you for your order!";
  if (txState.value === "pending") return "Payment pending confirmation";
  if (txState.value === "error") return "Payment failed";
  if (txState.value === "cancel") return "Payment cancelled";
  return "Processing payment…";
});

const statusSubtitle = computed(() => {
  if (DONE_STATES.includes(txState.value)) return "We've received your order and will start preparing it.";
  if (txState.value === "pending") return "Your payment is awaiting confirmation. You'll receive an email when it clears.";
  if (txState.value === "error") return "Something went wrong with the payment provider. You can retry from the cart.";
  if (txState.value === "cancel") return "You can return to the cart and try again.";
  return "Hang tight — we're confirming with the payment provider.";
});

function money(value) {
  const currency = order.value?.currency?.name || "USD";
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency
  }).format(Number(value || 0));
}

async function loadOrderAndStatus() {
  try {
    const detail = await odooApi.getOrderDetail(orderId.value, accessToken.value);
    if (detail) {
      order.value = detail;
      txState.value = detail.payment?.state || "";
    }
    const status = await odooApi.getPaymentStatus(orderId.value, accessToken.value);
    if (status?.tx?.state) {
      txState.value = status.tx.state;
    }
  } catch (e) {
    error.value = e.message || "Failed to load order status.";
  }
}

async function poll() {
  pollCount += 1;
  await loadOrderAndStatus();
  if (FINAL_STATES.includes(txState.value) || pollCount >= 30) {
    stopPolling();
  }
}

function startPolling() {
  if (pollTimer) return;
  poll();
  pollTimer = setInterval(poll, 2000);
}

function stopPolling() {
  if (pollTimer) {
    clearInterval(pollTimer);
    pollTimer = null;
  }
}

onMounted(startPolling);
onUnmounted(stopPolling);
</script>

<style scoped>
.done {
  display: grid;
  gap: 1rem;
  padding-top: 1rem;
}

.hero {
  padding: 1.4rem;
  text-align: center;
  display: grid;
  gap: 0.4rem;
}

.hero h1 {
  margin: 0.2rem 0 0;
}

.badge {
  display: inline-block;
  justify-self: center;
  padding: 0.25rem 0.7rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 600;
}

.badge.success {
  background: #e7f6ee;
  color: #1f7a47;
}

.badge.info {
  background: #e8f1fb;
  color: #2566c2;
}

.badge.warn {
  background: #fff4e0;
  color: #a35c00;
}

.badge.danger {
  background: #fde7e7;
  color: #b32424;
}

.layout {
  display: grid;
  gap: 1rem;
}

.card {
  padding: 1rem;
  display: grid;
  gap: 0.5rem;
}

.row.between {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.lines {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 0.4rem;
}

.lines li {
  display: flex;
  justify-content: space-between;
  font-size: 0.92rem;
}

.total {
  border-top: 1px solid var(--line);
  padding-top: 0.5rem;
  font-weight: 600;
}

.addr-grid {
  grid-template-columns: 1fr 1fr;
}

.addr {
  margin: 0;
  line-height: 1.45;
  font-size: 0.9rem;
}

.tag {
  text-transform: capitalize;
  padding: 0.2rem 0.55rem;
  border-radius: 999px;
  font-size: 0.78rem;
  background: #f0f3f1;
}

.tag-done,
.tag-authorized {
  background: #e7f6ee;
  color: #1f7a47;
}

.tag-error {
  background: #fde7e7;
  color: #b32424;
}

.tag-pending {
  background: #e8f1fb;
  color: #2566c2;
}

.actions {
  display: flex;
  gap: 0.6rem;
  justify-content: center;
}

.error {
  color: var(--danger);
  text-align: center;
}

.small {
  font-size: 0.82rem;
}

h3,
h4 {
  margin: 0;
}

@media (max-width: 720px) {
  .addr-grid {
    grid-template-columns: 1fr;
  }
}
</style>
