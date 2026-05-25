<template>
  <div class="container auth">
    <header class="head">
      <h1 class="section-title">Reset password</h1>
      <p class="muted">Choose a new password to log in with.</p>
    </header>

    <section class="card panel">
      <form class="form" @submit.prevent="submit">
        <label>
          Email
          <input v-model="login" class="input" type="email" required autocomplete="username" />
        </label>
        <label>
          Reset token
          <input v-model="token" class="input" required />
          <small class="muted">From the password reset email link.</small>
        </label>
        <label>
          New password
          <input v-model="newPassword" class="input" type="password" minlength="6" required autocomplete="new-password" />
        </label>
        <label>
          Confirm new password
          <input v-model="confirm" class="input" type="password" required autocomplete="new-password" />
        </label>
        <p v-if="error" class="error">{{ error }}</p>
        <button class="button primary" type="submit" :disabled="sessionStore.loading">
          {{ sessionStore.loading ? "Updating…" : "Update password" }}
        </button>
      </form>
    </section>
  </div>
</template>

<script setup>
import { ref, watchEffect } from "vue";
import { useRoute, useRouter } from "vue-router";

import { useSessionStore } from "../stores/session";

const route = useRoute();
const router = useRouter();
const sessionStore = useSessionStore();

const login = ref("");
const token = ref("");
const newPassword = ref("");
const confirm = ref("");
const error = ref("");

watchEffect(() => {
  if (route.query.token) token.value = String(route.query.token);
  if (route.query.login) login.value = String(route.query.login);
});

async function submit() {
  error.value = "";
  if (newPassword.value !== confirm.value) {
    error.value = "Passwords do not match.";
    return;
  }
  try {
    await sessionStore.resetPassword({
      token: token.value.trim(),
      login: login.value.trim(),
      newPassword: newPassword.value
    });
    router.push("/account");
  } catch (e) {
    error.value = e.message || "Reset failed.";
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

.error {
  color: var(--danger);
  margin: 0;
}
</style>
