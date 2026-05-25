<template>
  <div class="container checkout">
    <header class="head">
      <div>
        <h1 class="section-title">Checkout</h1>
        <p class="muted">Address, delivery and payment in one place.</p>
      </div>
      <CheckoutSteps
        :current-step="checkoutStore.currentStep"
        :done-steps="doneSteps"
        @jump="goTo"
      />
    </header>

    <EmptyState
      v-if="!checkoutStore.canCheckout"
      title="No items in your cart"
      description="Add products to cart first to continue checkout."
      cta-to="/shop"
      cta-label="Go to catalog"
    />
    <div v-else class="layout">
      <section class="main grid flow">
        <!-- ADDRESS STEP -->
        <template v-if="checkoutStore.currentStep === 'address'">
          <template v-if="sessionStore.isLoggedIn">
            <AddressPicker
              title="Billing address"
              address-type="billing"
              :items="billingAddresses"
              :selected-id="checkoutStore.order?.billing_address?.id || null"
              :default-billing-id="defaultBillingId"
              @use="(id) => useAddress(id, 'billing')"
              @save="(payload) => saveAddress(payload)"
              @delete="deleteAddress"
              @default="(id) => setDefault(id, 'billing')"
            />

            <label class="card row checkbox">
              <input type="checkbox" v-model="useBillingForShipping" @change="onUseSameToggle" />
              <span>Use billing address for shipping</span>
            </label>

            <AddressPicker
              v-if="!useBillingForShipping"
              title="Shipping address"
              address-type="shipping"
              :items="shippingAddresses"
              :selected-id="checkoutStore.order?.shipping_address?.id || null"
              :default-shipping-id="defaultShippingId"
              @use="(id) => useAddress(id, 'shipping')"
              @save="(payload) => saveAddress(payload)"
              @delete="deleteAddress"
              @default="(id) => setDefault(id, 'shipping')"
            />
          </template>
          <template v-else>
            <AddressForm
              title="Billing address"
              address-type="billing"
              :initial="checkoutStore.order?.billing_address || null"
              submit-label="Save billing address"
              @submit="(payload) => saveAddress(payload)"
            />
            <label class="card row checkbox">
              <input type="checkbox" v-model="useBillingForShipping" @change="onUseSameToggle" />
              <span>Use billing address for shipping</span>
            </label>
            <AddressForm
              v-if="!useBillingForShipping"
              title="Shipping address"
              address-type="shipping"
              :initial="checkoutStore.order?.shipping_address || null"
              submit-label="Save shipping address"
              @submit="(payload) => saveAddress(payload)"
            />
          </template>

          <div class="actions">
            <button
              class="button primary"
              type="button"
              :disabled="!canAdvanceFromAddress"
              @click="advanceFromAddress"
            >
              Continue to delivery
            </button>
          </div>
        </template>

        <!-- DELIVERY STEP -->
        <template v-if="checkoutStore.currentStep === 'delivery'">
          <DeliverySelector
            :items="checkoutStore.deliveryMethods"
            :rates="checkoutStore.deliveryRates"
            :model-value="checkoutStore.order?.carrier?.id || null"
            :currency="currencyCode"
            @update:modelValue="setCarrier"
            @rate-request="checkoutStore.loadDeliveryRate"
          />

          <section class="card coupon">
            <h3>Coupon or loyalty code</h3>
            <div class="row">
              <input v-model="couponCode" class="input" placeholder="SPRING25" />
              <button class="button primary" type="button" @click="applyCoupon">Apply</button>
            </div>
            <p v-if="couponMessage" class="muted small">{{ couponMessage }}</p>
          </section>

          <div class="actions">
            <button class="button ghost" type="button" @click="goTo('address')">Back</button>
            <button
              class="button primary"
              type="button"
              :disabled="!checkoutStore.hasDelivery"
              @click="advanceFromDelivery"
            >
              Continue to payment
            </button>
          </div>
        </template>

        <!-- PAYMENT STEP -->
        <template v-if="checkoutStore.currentStep === 'payment'">
          <PaymentSelector
            :providers="checkoutStore.providers"
            :tokens="checkoutStore.tokens"
            :selected-provider-id="checkoutStore.selectedProviderId"
            :selected-token-id="checkoutStore.selectedTokenId"
            :amount="checkoutStore.order?.amount_total || 0"
            :currency="currencyCode"
            :disabled="checkoutStore.loading"
            :error="checkoutStore.error"
            @update:selectedProviderId="checkoutStore.selectedProviderId = $event"
            @update:selectedTokenId="checkoutStore.selectedTokenId = $event"
            @pay="pay"
          />
          <div class="actions">
            <button class="button ghost" type="button" @click="goTo('delivery')">Back</button>
          </div>
        </template>
      </section>

      <aside class="card summary">
        <h3>Order recap</h3>
        <ul>
          <li v-for="line in checkoutStore.order.lines" :key="line.id">
            <span>{{ line.name }} × {{ line.quantity }}</span>
            <strong>{{ money(line.price_total) }}</strong>
          </li>
        </ul>
        <div v-if="checkoutStore.order.amount_delivery" class="subtotal">
          <span>Shipping</span>
          <strong>{{ money(checkoutStore.order.amount_delivery) }}</strong>
        </div>
        <div v-if="checkoutStore.order.amount_tax" class="subtotal">
          <span>Tax</span>
          <strong>{{ money(checkoutStore.order.amount_tax) }}</strong>
        </div>
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
import { computed, onMounted, ref, watch } from "vue";

import AddressForm from "../components/checkout/AddressForm.vue";
import AddressPicker from "../components/checkout/AddressPicker.vue";
import CheckoutSteps from "../components/checkout/CheckoutSteps.vue";
import DeliverySelector from "../components/checkout/DeliverySelector.vue";
import PaymentSelector from "../components/checkout/PaymentSelector.vue";
import EmptyState from "../components/shared/EmptyState.vue";
import { useCheckoutStore } from "../stores/checkout";
import { useSessionStore } from "../stores/session";

const checkoutStore = useCheckoutStore();
const sessionStore = useSessionStore();

const couponCode = ref("");
const couponMessage = ref("");
const useBillingForShipping = ref(false);

const currencyCode = computed(() => checkoutStore.order?.currency?.name || "USD");
const billingAddresses = computed(() =>
  checkoutStore.addresses.filter((a) => ["contact", "invoice", "other"].includes(a.type))
);
const shippingAddresses = computed(() =>
  checkoutStore.addresses.filter((a) => ["contact", "delivery", "other"].includes(a.type))
);
const defaultBillingId = computed(() => {
  const direct = checkoutStore.addresses.find((a) => a.type === "invoice");
  return direct ? direct.id : null;
});
const defaultShippingId = computed(() => {
  const direct = checkoutStore.addresses.find((a) => a.type === "delivery");
  return direct ? direct.id : null;
});

const doneSteps = computed(() => {
  const done = [];
  if (checkoutStore.hasBilling && checkoutStore.hasShipping) done.push("address");
  if (checkoutStore.hasDelivery) done.push("delivery");
  return done;
});

const canAdvanceFromAddress = computed(() => checkoutStore.hasBilling && checkoutStore.hasShipping);

onMounted(async () => {
  await checkoutStore.refreshOrder();
  await checkoutStore.loadCountries();
  if (sessionStore.isLoggedIn) {
    await checkoutStore.loadAddresses();
  }
  // preload states for current billing country
  const cid = checkoutStore.order?.billing_address?.country_id;
  if (cid) await checkoutStore.loadStates(cid);
});

watch(
  () => checkoutStore.order?.billing_address?.id,
  (bid) => {
    const sid = checkoutStore.order?.shipping_address?.id;
    if (bid && sid && bid === sid) {
      useBillingForShipping.value = true;
    }
  }
);

function money(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: currencyCode.value
  }).format(Number(value || 0));
}

function goTo(step) {
  if (step === "delivery" && !canAdvanceFromAddress.value) return;
  if (step === "payment" && (!canAdvanceFromAddress.value || !checkoutStore.hasDelivery)) return;
  checkoutStore.setStep(step);
}

async function saveAddress(payload) {
  await checkoutStore.saveAddress({
    partnerId: payload.partner_id || null,
    addressType: payload.addressType,
    form: payload.form,
    useOnOrder: true
  });
  if (payload.addressType === "billing" && useBillingForShipping.value) {
    const newBillingId = checkoutStore.order?.billing_address?.id;
    if (newBillingId) {
      await checkoutStore.useAddress(newBillingId, "shipping");
    }
  }
}

async function useAddress(partnerId, addressType) {
  await checkoutStore.useAddress(partnerId, addressType);
  if (addressType === "billing" && useBillingForShipping.value) {
    await checkoutStore.useAddress(partnerId, "shipping");
  }
}

async function deleteAddress(id) {
  if (!confirm("Delete this address?")) return;
  await checkoutStore.deleteAddress(id);
}

async function setDefault(id, type) {
  await checkoutStore.setDefaultAddress(id, type);
}

async function onUseSameToggle() {
  if (useBillingForShipping.value) {
    const billingId = checkoutStore.order?.billing_address?.id;
    if (billingId) {
      await checkoutStore.useAddress(billingId, "shipping");
    }
  }
}

async function advanceFromAddress() {
  await checkoutStore.loadDeliveryMethods();
  checkoutStore.setStep("delivery");
}

async function setCarrier(carrierId) {
  await checkoutStore.setDeliveryMethod(carrierId);
}

async function advanceFromDelivery() {
  try {
    await checkoutStore.confirm();
    await checkoutStore.loadProviders();
    checkoutStore.setStep("payment");
  } catch (e) {
    /* error already in store.error */
  }
}

async function applyCoupon() {
  if (!couponCode.value.trim()) return;
  try {
    const res = await checkoutStore.applyCoupon(couponCode.value.trim());
    couponMessage.value = res?.result?.success || res?.result?.notification || "Coupon applied.";
  } catch (e) {
    couponMessage.value = e.message || "Coupon failed.";
  }
}

async function pay() {
  await checkoutStore.payNow();
}
</script>

<style scoped>
.checkout {
  display: grid;
  gap: 1rem;
  padding-top: 1rem;
}

.head {
  display: grid;
  gap: 0.7rem;
  align-items: end;
}

.head > div {
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

.actions {
  display: flex;
  justify-content: space-between;
  gap: 0.7rem;
}

.coupon {
  padding: 1rem;
  display: grid;
  gap: 0.6rem;
}

.row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.6rem;
}

.row.checkbox {
  grid-template-columns: auto 1fr;
  padding: 0.7rem 1rem;
  align-items: center;
  cursor: pointer;
}

.summary {
  padding: 1rem;
  height: fit-content;
  position: sticky;
  top: 90px;
  display: grid;
  gap: 0.5rem;
}

h3 {
  margin: 0;
}

ul {
  margin: 0.5rem 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 0.4rem;
}

li {
  display: flex;
  justify-content: space-between;
  gap: 0.7rem;
  font-size: 0.92rem;
}

.subtotal,
.total {
  display: flex;
  justify-content: space-between;
  padding-top: 0.4rem;
  border-top: 1px solid var(--line);
  font-size: 0.92rem;
}

.total {
  font-size: 1rem;
  font-weight: 600;
}

.error {
  color: var(--danger);
  margin: 0.4rem 0 0;
}

.small {
  font-size: 0.82rem;
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
