<template>
  <form class="card form" @submit.prevent="submit">
    <header class="head">
      <h3>{{ title }}</h3>
      <button v-if="cancelable" class="button link" type="button" @click="$emit('cancel')">
        Cancel
      </button>
    </header>
    <div class="grid two">
      <label>
        Full name
        <input v-model="local.name" class="input" required />
      </label>
      <label>
        Email
        <input v-model="local.email" class="input" type="email" required />
      </label>
      <label>
        Phone
        <input v-model="local.phone" class="input" />
      </label>
      <label>
        Country
        <select v-model.number="local.country_id" class="input" required @change="onCountryChange">
          <option :value="null" disabled>Select a country</option>
          <option v-for="c in countries" :key="c.id" :value="c.id">
            {{ c.name }}
          </option>
        </select>
      </label>
      <label>
        Street
        <input v-model="local.street" class="input" required />
      </label>
      <label>
        Street 2
        <input v-model="local.street2" class="input" />
      </label>
      <label>
        City
        <input v-model="local.city" class="input" required />
      </label>
      <label>
        ZIP
        <input v-model="local.zip" class="input" :required="zipRequired" />
      </label>
      <label v-if="states.length">
        State
        <select v-model.number="local.state_id" class="input" :required="stateRequired">
          <option :value="null">— None —</option>
          <option v-for="s in states" :key="s.id" :value="s.id">
            {{ s.name }}
          </option>
        </select>
      </label>
      <label>
        {{ vatLabel }}
        <input v-model="local.vat" class="input" />
      </label>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
    <button class="button primary" type="submit" :disabled="loading">
      {{ submitLabel }}
    </button>
  </form>
</template>

<script setup>
import { computed, reactive, ref, watch } from "vue";

import { useCheckoutStore } from "../../stores/checkout";

const props = defineProps({
  title: { type: String, default: "Address" },
  addressType: { type: String, default: "billing" },
  initial: { type: Object, default: null },
  cancelable: { type: Boolean, default: false },
  submitLabel: { type: String, default: "Save address" }
});

const emit = defineEmits(["submit", "cancel"]);

const checkoutStore = useCheckoutStore();
const error = ref("");
const loading = ref(false);

const empty = {
  name: "",
  email: "",
  phone: "",
  country_id: null,
  street: "",
  street2: "",
  city: "",
  zip: "",
  state_id: null,
  vat: ""
};

const local = reactive({ ...empty });
const partnerId = ref(null);

watch(
  () => props.initial,
  (value) => {
    if (value) {
      partnerId.value = value.id || null;
      Object.assign(local, empty, {
        name: value.name || "",
        email: value.email || "",
        phone: value.phone || "",
        country_id: value.country_id || null,
        street: value.street || "",
        street2: value.street2 || "",
        city: value.city || "",
        zip: value.zip || "",
        state_id: value.state_id || null,
        vat: value.vat || ""
      });
      if (value.country_id) {
        checkoutStore.loadStates(value.country_id);
      }
    } else {
      partnerId.value = null;
      Object.assign(local, empty);
    }
  },
  { immediate: true }
);

const countries = computed(() => checkoutStore.countries);
const states = computed(() => {
  const cid = local.country_id;
  return cid ? checkoutStore.statesByCountry[cid] || [] : [];
});
const country = computed(() => countries.value.find((c) => c.id === local.country_id) || null);
const zipRequired = computed(() => Boolean(country.value?.zip_required));
const stateRequired = computed(() => Boolean(country.value?.state_required));
const vatLabel = computed(() => country.value?.vat_label || "VAT");

async function onCountryChange() {
  local.state_id = null;
  if (local.country_id) {
    await checkoutStore.loadStates(local.country_id);
  }
}

async function submit() {
  error.value = "";
  loading.value = true;
  try {
    emit("submit", {
      partner_id: partnerId.value,
      addressType: props.addressType,
      form: { ...local }
    });
  } catch (e) {
    error.value = e.message || "Failed.";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.form {
  padding: 1rem;
  display: grid;
  gap: 0.9rem;
}

.head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

h3 {
  margin: 0;
}

.two {
  grid-template-columns: 1fr 1fr;
}

label {
  display: grid;
  gap: 0.35rem;
}

.error {
  color: var(--danger);
  margin: 0;
}

.button.link {
  background: transparent;
  border: none;
  color: var(--muted);
  cursor: pointer;
  padding: 0;
  font-size: 0.85rem;
}

.button.link:hover {
  color: var(--text);
}

@media (max-width: 860px) {
  .two {
    grid-template-columns: 1fr;
  }
}
</style>
