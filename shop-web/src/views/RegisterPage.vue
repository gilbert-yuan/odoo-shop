<template>
  <div class="container auth">
    <header class="head">
      <h1 class="section-title">Create an account</h1>
      <p class="muted">Sign up to track orders and save addresses.</p>
    </header>

    <section class="card panel">
      <form class="form" @submit.prevent="submit">
        <label>
          Full name
          <input v-model="form.name" class="input" required autocomplete="name" />
        </label>
        <label>
          Email
          <input v-model="form.login" class="input" type="email" required autocomplete="email" />
        </label>
        <label>
          Phone <span class="muted small">(optional)</span>
          <input v-model="form.phone" class="input" autocomplete="tel" />
        </label>
        <label>
          Password
          <input
            v-model="form.password"
            class="input"
            type="password"
            required
            autocomplete="new-password"
            minlength="6"
          />
          <small class="muted">At least 6 characters.</small>
        </label>
        <label>
          Confirm password
          <input
            v-model="confirmPassword"
            class="input"
            type="password"
            required
            autocomplete="new-password"
          />
        </label>

        <p v-if="error" class="error">{{ error }}</p>

        <button class="button primary" type="submit" :disabled="sessionStore.loading">
          {{ sessionStore.loading ? "Creating…" : "Create account" }}
        </button>
      </form>
      <p class="muted small foot">
        Already have an account?
        <RouterLink to="/account">Sign in</RouterLink>
      </p>
    </section>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { RouterLink, useRouter } from "vue-router";

import { useSessionStore } from "../stores/session";

const router = useRouter();
const sessionStore = useSessionStore();

const form = reactive({
  name: "",
  login: "",
  password: "",
  phone: ""
});
const confirmPassword = ref("");
const error = ref("");

async function submit() {
  error.value = "";
  if (form.password !== confirmPassword.value) {
    error.value = "Passwords do not match.";
    return;
  }
  try {
    await sessionStore.register({
      name: form.name.trim(),
      login: form.login.trim(),
      password: form.password,
      phone: form.phone.trim() || null
    });
    router.push("/account");
  } catch (e) {
    error.value = e.message || "Registration failed.";
  }
}
</script>

<style scoped>
.auth {
  display: grid;
  gap: 1rem;
  padding-top: 1rem;
  max-width: 520px;
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
  display: grid;
  gap: 0.6rem;
}

.form {
  display: grid;
  gap: 0.8rem;
}

label {
  display: grid;
  gap: 0.3rem;
}

.error {
  color: var(--danger);
  margin: 0;
}

.foot {
  text-align: center;
  margin: 0.6rem 0 0;
}

.foot a {
  color: var(--accent);
  font-weight: 600;
}

.small {
  font-size: 0.82rem;
}
</style>
