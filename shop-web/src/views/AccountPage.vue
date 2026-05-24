<template>
  <div class="container account">
    <header class="head">
      <h1 class="section-title">Account</h1>
      <p class="muted">Sign in to access customer-specific checkout and order flows.</p>
    </header>

    <section class="card panel">
      <template v-if="sessionStore.isLoggedIn">
        <p>You are signed in as <strong>{{ sessionStore.displayName }}</strong>.</p>
        <div class="actions">
          <RouterLink class="button primary" to="/account/orders">View orders</RouterLink>
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
      </form>
    </section>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import { useRouter, RouterLink } from "vue-router";

import { useSessionStore } from "../stores/session";

const router = useRouter();
const sessionStore = useSessionStore();

const loginForm = reactive({
  login: "",
  password: ""
});

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
</style>
