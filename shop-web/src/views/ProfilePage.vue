<template>
  <div class="container profile">
    <header class="head">
      <h1 class="section-title">My profile</h1>
      <p class="muted">Update your account information and password.</p>
    </header>

    <EmptyState
      v-if="!sessionStore.isLoggedIn"
      title="Sign in required"
      description="Sign in to access your profile."
      cta-to="/account"
      cta-label="Sign in"
    />
    <div v-else class="layout">
      <section class="card panel">
        <h3>Account information</h3>
        <form class="form" @submit.prevent="saveProfile">
          <label>
            Full name
            <input v-model="profileForm.name" class="input" required />
          </label>
          <label>
            Email
            <input v-model="profileForm.email" class="input" type="email" required />
          </label>
          <label>
            Phone
            <input v-model="profileForm.phone" class="input" />
          </label>
          <label>
            Language
            <select v-model="profileForm.lang" class="input">
              <option value="">— Keep current —</option>
              <option v-for="l in languages" :key="l.code" :value="l.code">{{ l.name }}</option>
            </select>
          </label>
          <p v-if="profileMsg" class="msg">{{ profileMsg }}</p>
          <button class="button primary" type="submit" :disabled="sessionStore.loading">
            Save profile
          </button>
        </form>
      </section>

      <section class="card panel">
        <h3>Change password</h3>
        <form class="form" @submit.prevent="changePassword">
          <label>
            Current password
            <input v-model="pwForm.current" class="input" type="password" required autocomplete="current-password" />
          </label>
          <label>
            New password
            <input v-model="pwForm.next" class="input" type="password" minlength="6" required autocomplete="new-password" />
          </label>
          <label>
            Confirm new password
            <input v-model="pwForm.confirm" class="input" type="password" required autocomplete="new-password" />
          </label>
          <p v-if="pwError" class="error">{{ pwError }}</p>
          <p v-if="pwMsg" class="msg">{{ pwMsg }}</p>
          <button class="button primary" type="submit" :disabled="sessionStore.loading">
            Update password
          </button>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref, watch } from "vue";

import EmptyState from "../components/shared/EmptyState.vue";
import { odooApi } from "../services/odooApi";
import { useSessionStore } from "../stores/session";

const sessionStore = useSessionStore();

const profileForm = reactive({ name: "", email: "", phone: "", lang: "" });
const pwForm = reactive({ current: "", next: "", confirm: "" });
const profileMsg = ref("");
const pwMsg = ref("");
const pwError = ref("");
const languages = ref([]);

async function loadAll() {
  if (!sessionStore.isLoggedIn) return;
  const profile = await sessionStore.loadProfile();
  if (profile) {
    profileForm.name = profile.name || "";
    profileForm.email = profile.email || "";
    profileForm.phone = profile.phone || "";
    profileForm.lang = profile.lang || "";
  }
  try {
    const langs = await odooApi.getLanguages();
    languages.value = langs.items || [];
  } catch {
    languages.value = [];
  }
}

onMounted(loadAll);
watch(() => sessionStore.isLoggedIn, loadAll);

async function saveProfile() {
  profileMsg.value = "";
  try {
    await sessionStore.updateProfile({
      name: profileForm.name,
      email: profileForm.email,
      phone: profileForm.phone,
      lang: profileForm.lang || null
    });
    profileMsg.value = "Profile updated.";
  } catch (e) {
    profileMsg.value = e.message || "Update failed.";
  }
}

async function changePassword() {
  pwError.value = "";
  pwMsg.value = "";
  if (pwForm.next !== pwForm.confirm) {
    pwError.value = "Passwords do not match.";
    return;
  }
  try {
    await sessionStore.changePassword({
      currentPassword: pwForm.current,
      newPassword: pwForm.next
    });
    pwMsg.value = "Password updated.";
    pwForm.current = "";
    pwForm.next = "";
    pwForm.confirm = "";
  } catch (e) {
    pwError.value = e.message || "Change failed.";
  }
}
</script>

<style scoped>
.profile {
  display: grid;
  gap: 1rem;
  padding-top: 1rem;
}

.head {
  display: grid;
  gap: 0.3rem;
}

.layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.panel {
  padding: 1rem;
  display: grid;
  gap: 0.6rem;
}

.form {
  display: grid;
  gap: 0.7rem;
}

label {
  display: grid;
  gap: 0.3rem;
}

h3 {
  margin: 0;
}

.msg {
  color: var(--accent);
  margin: 0;
  font-weight: 600;
}

.error {
  color: var(--danger);
  margin: 0;
}

@media (max-width: 900px) {
  .layout {
    grid-template-columns: 1fr;
  }
}
</style>
