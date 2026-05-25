<template>
  <StaticPage
    title="Wholesale Inquiry"
    description="Request bulk pricing and partnership terms from NextPept."
  >
    <div v-if="submitted" class="thanks">
      <h2>Inquiry received</h2>
      <p>
        Our wholesale team will reach out to <strong>{{ form.email }}</strong>
        within 1–2 business days with a custom quote.
      </p>
      <button class="button ghost" type="button" @click="reset">Submit another</button>
    </div>
    <form v-else class="form" @submit.prevent="submit">
      <p class="muted">
        Operating a clinic, lab, distributor, or contract-research org? Tell us a bit about
        your sourcing needs and we'll respond with volume pricing.
      </p>
      <div class="grid-two">
        <label>
          Company / organisation
          <input v-model="form.company" class="input" required autocomplete="organization" />
        </label>
        <label>
          Contact name
          <input v-model="form.name" class="input" required autocomplete="name" />
        </label>
        <label>
          Work email
          <input v-model="form.email" class="input" type="email" required autocomplete="email" />
        </label>
        <label>
          Phone
          <input v-model="form.phone" class="input" autocomplete="tel" />
        </label>
        <label>
          Country
          <input v-model="form.country" class="input" autocomplete="country-name" />
        </label>
        <label>
          Estimated monthly volume
          <input v-model="form.volume" class="input" placeholder="e.g. 50 vials / month" />
        </label>
      </div>
      <label>
        Products of interest
        <input v-model="form.products" class="input" placeholder="BPC-157, TB-500, …" />
      </label>
      <label>
        Notes
        <textarea
          v-model="form.message"
          class="input textarea"
          rows="5"
          placeholder="Anything else we should know (lead times, packaging, certifications…)"
        />
      </label>
      <p v-if="error" class="error">{{ error }}</p>
      <button class="button primary" type="submit" :disabled="loading">
        {{ loading ? "Sending…" : "Send inquiry" }}
      </button>
    </form>
  </StaticPage>
</template>

<script setup>
import { reactive, ref } from "vue";

import StaticPage from "./StaticPage.vue";
import { odooApi } from "../services/odooApi";

const form = reactive({
  company: "",
  name: "",
  email: "",
  phone: "",
  country: "",
  volume: "",
  products: "",
  message: ""
});
const loading = ref(false);
const error = ref("");
const submitted = ref(false);

async function submit() {
  error.value = "";
  loading.value = true;
  try {
    await odooApi.submitWholesale({
      company: form.company.trim(),
      name: form.name.trim(),
      email: form.email.trim(),
      phone: form.phone.trim(),
      country: form.country.trim(),
      products: form.products.trim(),
      volume: form.volume.trim(),
      message: form.message.trim()
    });
    submitted.value = true;
  } catch (e) {
    error.value = e.message || "Submission failed.";
  } finally {
    loading.value = false;
  }
}

function reset() {
  submitted.value = false;
  for (const k of Object.keys(form)) form[k] = "";
}
</script>

<style scoped>
.form {
  display: grid;
  gap: 0.9rem;
}

.grid-two {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.7rem;
}

label {
  display: grid;
  gap: 0.3rem;
}

.textarea {
  min-height: 7rem;
  resize: vertical;
}

.error {
  color: var(--danger);
  margin: 0;
}

.thanks {
  text-align: center;
  display: grid;
  gap: 0.8rem;
  padding: 1rem 0;
}

.thanks h2 {
  margin: 0;
}

@media (max-width: 640px) {
  .grid-two {
    grid-template-columns: 1fr;
  }
}
</style>
