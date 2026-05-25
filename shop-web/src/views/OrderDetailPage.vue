<template>
  <div class="container detail">
    <header class="row between">
      <div>
        <h1 class="section-title">Order {{ order?.name || "" }}</h1>
        <p class="muted">{{ order?.date_order || "" }}</p>
      </div>
      <RouterLink class="button ghost" to="/account/orders">All orders</RouterLink>
    </header>

    <p v-if="loading" class="muted">Loading…</p>
    <p v-if="error" class="error">{{ error }}</p>

    <div v-if="order" class="layout">
      <section class="card">
        <header class="row between">
          <h3>Items</h3>
          <span :class="['tag', `tag-${order.state}`]">{{ order.state }}</span>
        </header>
        <ul class="lines">
          <li v-for="line in order.lines || []" :key="line.id">
            <span>{{ line.name }} × {{ line.quantity }}</span>
            <strong>{{ money(line.price_total) }}</strong>
          </li>
        </ul>
        <div v-if="order.amount_delivery" class="row sub">
          <span>Shipping</span><strong>{{ money(order.amount_delivery) }}</strong>
        </div>
        <div v-if="order.amount_tax" class="row sub">
          <span>Tax</span><strong>{{ money(order.amount_tax) }}</strong>
        </div>
        <div class="row total">
          <span>Total</span><strong>{{ money(order.amount_total) }}</strong>
        </div>
      </section>

      <section v-if="order.billing_address || order.shipping_address" class="card addr-grid">
        <div v-if="order.billing_address">
          <h4>Billing</h4>
          <p class="addr">
            <strong>{{ order.billing_address.name }}</strong><br />
            {{ order.billing_address.street }}<template v-if="order.billing_address.street2">, {{ order.billing_address.street2 }}</template><br />
            {{ order.billing_address.city }} {{ order.billing_address.zip }} {{ order.billing_address.state_name }}<br />
            {{ order.billing_address.country_name }}
          </p>
        </div>
        <div v-if="order.shipping_address">
          <h4>Shipping</h4>
          <p class="addr">
            <strong>{{ order.shipping_address.name }}</strong><br />
            {{ order.shipping_address.street }}<template v-if="order.shipping_address.street2">, {{ order.shipping_address.street2 }}</template><br />
            {{ order.shipping_address.city }} {{ order.shipping_address.zip }} {{ order.shipping_address.state_name }}<br />
            {{ order.shipping_address.country_name }}
          </p>
        </div>
      </section>

      <section v-if="order.carrier" class="card row between">
        <span><strong>Delivery:</strong> {{ order.carrier.name }}</span>
        <span class="muted small">{{ order.carrier.delivery_type }}</span>
      </section>

      <section v-if="order.payment" class="card row between">
        <span><strong>Payment:</strong> {{ order.payment.provider_name || order.payment.provider_code }}</span>
        <span :class="['tag', `tag-${order.payment.state}`]">{{ order.payment.state }}</span>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { RouterLink, useRoute } from "vue-router";

import { odooApi } from "../services/odooApi";

const route = useRoute();
const orderId = computed(() => Number(route.params.id));

const order = ref(null);
const loading = ref(false);
const error = ref("");

function money(value) {
  const currency = order.value?.currency?.name || "USD";
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency
  }).format(Number(value || 0));
}

onMounted(async () => {
  loading.value = true;
  error.value = "";
  try {
    order.value = await odooApi.getOrderDetail(orderId.value);
  } catch (e) {
    error.value = e.message || "Failed to load order.";
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.detail {
  display: grid;
  gap: 1rem;
  padding-top: 1rem;
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

.row.sub,
.row.total {
  display: flex;
  justify-content: space-between;
  padding-top: 0.4rem;
  border-top: 1px solid var(--line);
}

.row.total {
  font-weight: 600;
}

.tag {
  text-transform: capitalize;
  padding: 0.2rem 0.55rem;
  border-radius: 999px;
  font-size: 0.78rem;
  background: #f0f3f1;
}

.tag-sale,
.tag-done,
.tag-authorized {
  background: #e7f6ee;
  color: #1f7a47;
}

.tag-draft,
.tag-pending {
  background: #e8f1fb;
  color: #2566c2;
}

.tag-cancel,
.tag-error {
  background: #fde7e7;
  color: #b32424;
}

.addr-grid {
  grid-template-columns: 1fr 1fr;
}

.addr {
  margin: 0;
  line-height: 1.45;
  font-size: 0.9rem;
}

.error {
  color: var(--danger);
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
