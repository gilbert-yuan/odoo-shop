<template>
  <StaticPage
    title="Contact Us"
    description="Send a message to the NextPept team."
  >
    <div v-if="submitted" class="thanks">
      <h2>Thanks for reaching out!</h2>
      <p>We received your message and will reply to <strong>{{ form.email }}</strong> shortly.</p>
      <button class="button ghost" type="button" @click="reset">Send another message</button>
    </div>
    <form v-else class="form" @submit.prevent="submit">
      <p class="muted">
        Have a question, partnership idea, or feedback? Drop us a line — we typically reply
        within one business day.
      </p>
      <div class="grid-two">
        <label>
          Your name
          <input v-model="form.name" class="input" required autocomplete="name" />
        </label>
        <label>
          Email
          <input v-model="form.email" class="input" type="email" required autocomplete="email" />
        </label>
        <label>
          Phone <span class="muted small">(optional)</span>
          <input v-model="form.phone" class="input" autocomplete="tel" />
        </label>
        <label>
          Subject
          <input v-model="form.subject" class="input" placeholder="Order #, product, etc." />
        </label>
      </div>
      <label>
        Message
        <textarea
          v-model="form.message"
          class="input textarea"
          rows="6"
          required
          placeholder="Tell us how we can help…"
        />
      </label>
      <p v-if="error" class="error">{{ error }}</p>
      <button class="button primary" type="submit" :disabled="loading">
        {{ loading ? "Sending…" : "Send message" }}
      </button>
    </form>
  </StaticPage>
</template>

<script setup>
import { reactive, ref } from "vue";

import StaticPage from "./StaticPage.vue";
import { odooApi } from "../services/odooApi";

const form = reactive({
  name: "",
  email: "",
  phone: "",
  subject: "",
  message: ""
});
const loading = ref(false);
const error = ref("");
const submitted = ref(false);

async function submit() {
  error.value = "";
  loading.value = true;
  try {
    await odooApi.submitContact({
      name: form.name.trim(),
      email: form.email.trim(),
      phone: form.phone.trim(),
      subject: form.subject.trim(),
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
  form.name = "";
  form.email = "";
  form.phone = "";
  form.subject = "";
  form.message = "";
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
  min-height: 8rem;
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

.small {
  font-size: 0.82rem;
}

@media (max-width: 640px) {
  .grid-two {
    grid-template-columns: 1fr;
  }
}
</style>
