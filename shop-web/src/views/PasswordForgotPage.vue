<template>
  <div class="container auth">
    <header class="head">
      <h1 class="section-title">Forgot password</h1>
      <p class="muted">We'll send you a reset link.</p>
    </header>

    <section class="card panel">
      <form v-if="!sent" class="form" @submit.prevent="submit">
        <label>
          Email
          <input v-model="login" class="input" type="email" required autocomplete="email" />
        </label>
        <p v-if="error" class="error">{{ error }}</p>
        <button class="button primary" type="submit" :disabled="busy">
          {{ busy ? "Sending…" : "Send reset link" }}
        </button>
      </form>
      <div v-else class="confirm">
        <p>✉ If an account exists for <strong>{{ login }}</strong>, a reset email is on its way.</p>
        <RouterLink class="button ghost" to="/account">Back to sign in</RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { RouterLink } from "vue-router";

import { useSessionStore } from "../stores/session";

const sessionStore = useSessionStore();

const login = ref("");
const sent = ref(false);
const busy = ref(false);
const error = ref("");

async function submit() {
  error.value = "";
  busy.value = true;
  try {
    await sessionStore.forgotPassword(login.value.trim());
    sent.value = true;
  } catch (e) {
    error.value = e.message || "Request failed.";
  } finally {
    busy.value = false;
  }
}
</script>

<style scoped>
.auth {
  display: grid;
  gap: 1rem;
  padding-top: 1rem;
  max-width: 480px;
  margin-left: auto;
  margin-right: auto;
}

.head {
  display: grid;
  gap: 0.3rem;
  text-align: center;
}

.panel {
  padding: 1.4rem;
}

.form {
  display: grid;
  gap: 0.8rem;
}

label {
  display: grid;
  gap: 0.3rem;
}

.confirm {
  display: grid;
  gap: 1rem;
  justify-items: center;
  text-align: center;
}

.confirm p {
  margin: 0;
}

.error {
  color: var(--danger);
  margin: 0;
}
</style>
