<template>
  <transition name="slide-up">
    <div v-if="visible" class="cookie">
      <div class="container row">
        <div class="text">
          <strong>We use cookies</strong>
          <p class="muted">
            Essential cookies keep your cart and login working. Optional cookies help us
            understand traffic and improve the storefront. Read more in our
            <RouterLink to="/privacy">Privacy Policy</RouterLink>.
          </p>
        </div>
        <div class="actions">
          <button class="button ghost" type="button" @click="setChoice('reject')">
            Reject optional
          </button>
          <button class="button primary" type="button" @click="setChoice('accept')">
            Accept all
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { RouterLink } from "vue-router";

const STORAGE_KEY = "nextpept_cookie_consent";
const visible = ref(false);

onMounted(() => {
  if (typeof window === "undefined") return;
  const existing = localStorage.getItem(STORAGE_KEY);
  if (!existing) {
    visible.value = true;
  }
});

function setChoice(choice) {
  try {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({ choice, at: new Date().toISOString() })
    );
  } catch {
    /* ignore quota errors */
  }
  visible.value = false;
}
</script>

<style scoped>
.cookie {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 1rem;
  z-index: 90;
  pointer-events: none;
}

.row {
  pointer-events: auto;
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  padding: 1rem 1.2rem;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.9rem 1.4rem;
  align-items: center;
}

.text strong {
  display: block;
  margin-bottom: 0.2rem;
}

.text p {
  margin: 0;
  font-size: 0.92rem;
  line-height: 1.5;
}

.text a {
  color: var(--accent);
  font-weight: 600;
}

.actions {
  display: flex;
  gap: 0.45rem;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.actions .button {
  padding: 0.55rem 1.1rem;
  font-size: 0.9rem;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.35s ease, opacity 0.35s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(20px);
  opacity: 0;
}

@media (max-width: 720px) {
  .row {
    grid-template-columns: 1fr;
  }
  .actions {
    justify-content: stretch;
  }
  .actions .button {
    flex: 1;
  }
}
</style>
