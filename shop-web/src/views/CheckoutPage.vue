<template>
  <div class="container checkout">
    <header class="head">
      <h1 class="section-title">Checkout</h1>
      <p class="muted">Address, shipping, loyalty and payment</p>
    </header>

    <EmptyState
      v-if="!checkoutStore.order?.lines?.length"
      title="No checkout order yet"
      description="Add products to cart first."
      cta-to="/shop"
      cta-label="Go to catalog"
    />
    <div v-else class="layout">
      <section class="grid flow">
        <AddressForm
          title="Billing address"
          address-type="billing"
          @submit="submitAddress"
        />
        <AddressForm
          title="Delivery address"
          address-type="delivery"
          @submit="submitAddress"
        />

        <section class="card coupon">
          <h3>Coupon or loyalty code</h3>
          <div class="row">
            <input v-model="couponCode" class="input" placeholder="SPRING25" />
            <button class="button primary" type="button" @click="applyCoupon">
              Apply
            </button>
          </div>
        </section>

        <DeliverySelector
          :html="checkoutStore.deliveryHtml"
          :items="checkoutStore.deliverySummary?.items || []"
          @set="setDeliveryMethod"
        />

        <section class="card payment">
          <h3>Payment</h3>
          <p class="muted">
            Use provider code from your Odoo payment provider (example: `stripe`, `paypal`).
          </p>
          <div class="row">
            <input v-model="providerCode" class="input" placeholder="stripe" />
            <button class="button primary" type="button" @click="createPayment">
              Create transaction
            </button>
          </div>
          <pre v-if="checkoutStore.lastPaymentValues" class="json">{{
            JSON.stringify(checkoutStore.lastPaymentValues, null, 2)
          }}</pre>
        </section>
      </section>

      <aside class="card summary">
        <h3>Order recap</h3>
        <ul>
          <li v-for="line in checkoutStore.order.lines" :key="line.id">
            <span>{{ line.name }} x{{ line.quantity }}</span>
            <strong>{{ money(line.total) }}</strong>
          </li>
        </ul>
        <div class="total">
          <span>Total</span>
          <strong>{{ money(checkoutStore.order.amount_total) }}</strong>
        </div>
        <p v-if="checkoutStore.error" class="error">{{ checkoutStore.error }}</p>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";

import AddressForm from "../components/checkout/AddressForm.vue";
import DeliverySelector from "../components/checkout/DeliverySelector.vue";
import EmptyState from "../components/shared/EmptyState.vue";
import { useCheckoutStore } from "../stores/checkout";

const checkoutStore = useCheckoutStore();
const couponCode = ref("");
const providerCode = ref("stripe");

onMounted(async () => {
  await checkoutStore.refresh();
  if (checkoutStore.order) {
    await checkoutStore.loadDeliveryMethods();
  }
});

function money(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD"
  }).format(Number(value || 0));
}

async function submitAddress(payload) {
  await checkoutStore.submitAddress(payload);
}

async function applyCoupon() {
  if (!couponCode.value.trim()) {
    return;
  }
  await checkoutStore.applyCoupon(couponCode.value.trim());
}

async function setDeliveryMethod(dmId) {
  await checkoutStore.setDeliveryMethod(dmId);
}

async function createPayment() {
  await checkoutStore.createPaymentTransaction({
    providerCode: providerCode.value.trim() || "stripe"
  });
}
</script>

<style scoped>
.checkout {
  display: grid;
  gap: 1rem;
  padding-top: 1rem;
}

.head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.layout {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 1rem;
}

.flow {
  align-content: start;
}

.coupon,
.payment {
  padding: 1rem;
  display: grid;
  gap: 0.7rem;
}

.row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.6rem;
}

.summary {
  padding: 1rem;
  height: fit-content;
  position: sticky;
  top: 90px;
}

h3 {
  margin: 0;
}

ul {
  margin: 0.6rem 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 0.45rem;
}

li {
  display: flex;
  justify-content: space-between;
  gap: 0.7rem;
  font-size: 0.93rem;
}

.total {
  display: flex;
  justify-content: space-between;
  padding-top: 0.5rem;
  border-top: 1px solid var(--line);
}

.json {
  margin: 0;
  background: #f1f7f5;
  border: 1px solid var(--line);
  padding: 0.7rem;
  border-radius: 12px;
  overflow: auto;
  font-size: 0.82rem;
}

.error {
  color: var(--danger);
  margin: 0.5rem 0 0;
}

@media (max-width: 980px) {
  .layout {
    grid-template-columns: 1fr;
  }
}
</style>
