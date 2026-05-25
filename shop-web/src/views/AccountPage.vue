<template>
  <div class="container account">
    <header class="head">
      <h1 class="section-title">Account</h1>
      <p class="muted">Sign in to manage addresses and orders.</p>
    </header>

    <section class="card panel">
      <template v-if="sessionStore.isLoggedIn">
        <p>You are signed in as <strong>{{ sessionStore.displayName }}</strong>.</p>
        <div class="actions">
          <RouterLink class="button primary" to="/account/orders">View orders</RouterLink>
          <RouterLink class="button ghost" to="/account/profile">Profile & password</RouterLink>
          <button class="button ghost" type="button" @click="logout">Sign out</button>
        </div>
      </template>

      <form v-else class="form" @submit.prevent="login">
        <label>
          Login
          <input v-model="loginForm.login" class="input" placeholder="user@example.com" required />
        </label>
        <label>
          Password
          <input v-model="loginForm.password" class="input" type="password" required />
        </label>
        <button class="button primary" type="submit" :disabled="sessionStore.loading">
          {{ sessionStore.loading ? "Signing in..." : "Sign in" }}
        </button>
        <p v-if="sessionStore.authError" class="error">{{ sessionStore.authError }}</p>
        <p class="foot muted small">
          <RouterLink to="/account/register">Create account</RouterLink>
          ·
          <RouterLink to="/account/forgot">Forgot password?</RouterLink>
        </p>
      </form>
    </section>

    <template v-if="sessionStore.isLoggedIn">
      <AddressPicker
        title="Billing address book"
        address-type="billing"
        :items="billingAddresses"
        :default-billing-id="defaultBillingId"
        @save="(payload) => saveAddress(payload)"
        @delete="deleteAddress"
        @default="(id) => setDefault(id, 'billing')"
        @use="() => {}"
      />
      <AddressPicker
        title="Shipping address book"
        address-type="shipping"
        :items="shippingAddresses"
        :default-shipping-id="defaultShippingId"
        @save="(payload) => saveAddress(payload)"
        @delete="deleteAddress"
        @default="(id) => setDefault(id, 'shipping')"
        @use="() => {}"
      />
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, watch } from "vue";
import { useRouter, RouterLink } from "vue-router";

import AddressPicker from "../components/checkout/AddressPicker.vue";
import { useCheckoutStore } from "../stores/checkout";
import { useSessionStore } from "../stores/session";

const router = useRouter();
const sessionStore = useSessionStore();
const checkoutStore = useCheckoutStore();

const loginForm = reactive({
  login: "",
  password: ""
});

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

async function bootstrapBook() {
  if (!sessionStore.isLoggedIn) return;
  await checkoutStore.loadCountries();
  await checkoutStore.loadAddresses();
}

onMounted(bootstrapBook);
watch(() => sessionStore.isLoggedIn, bootstrapBook);

async function login() {
  await sessionStore.login({
    login: loginForm.login.trim(),
    password: loginForm.password
  });
  router.push("/account/orders");
}

async function logout() {
  await sessionStore.logout();
}

async function saveAddress(payload) {
  await checkoutStore.saveAddress({
    partnerId: payload.partner_id || null,
    addressType: payload.addressType,
    form: payload.form,
    useOnOrder: false
  });
}

async function deleteAddress(id) {
  if (!confirm("Delete this address?")) return;
  await checkoutStore.deleteAddress(id);
}

async function setDefault(id, type) {
  await checkoutStore.setDefaultAddress(id, type);
}
</script>

<style scoped>
.account {
  display: grid;
  gap: 1rem;
  padding-top: 1rem;
}

.head {
  display: grid;
  gap: 0.3rem;
}

.panel {
  padding: 1rem;
  max-width: 560px;
}

.form {
  display: grid;
  gap: 0.8rem;
}

label {
  display: grid;
  gap: 0.3rem;
}

.actions {
  display: flex;
  gap: 0.6rem;
}

.error {
  color: var(--danger);
  margin: 0;
}

.foot {
  margin: 0;
  text-align: center;
}

.foot a {
  color: var(--accent);
  font-weight: 600;
}

.small {
  font-size: 0.85rem;
}
</style>
