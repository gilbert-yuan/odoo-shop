<template>
  <footer class="footer">
    <div class="container footer-row">
      <nav class="links">
        <RouterLink to="/about">About NextPept</RouterLink>
        <RouterLink to="/terms">Terms And Conditions</RouterLink>
        <RouterLink to="/shipping-returns">Shipping And Returns</RouterLink>
        <RouterLink to="/refund-policy">Refund And Returns Policy</RouterLink>
        <RouterLink to="/privacy">Privacy Policy</RouterLink>
      </nav>
      <p class="copy muted">© {{ year }} NextPept. All rights reserved.</p>
    </div>
  </footer>
</template>

<script setup>
import { computed } from "vue";
import { RouterLink } from "vue-router";

const year = computed(() => new Date().getFullYear());
</script>

<style scoped>
.footer {
  border-top: 1px solid var(--line);
  margin-top: 2rem;
  padding: 1.8rem 0;
  background: #f2eee3;
}

:global(html.dark) .footer {
  background: #131c18;
}

.footer-row {
  display: grid;
  gap: 0.9rem;
  justify-items: center;
  text-align: center;
}

.links {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.4rem 1.6rem;
  font-size: 0.92rem;
}

.links a {
  color: var(--muted);
  transition: color 0.15s;
}

.links a:hover,
.links a.router-link-active {
  color: var(--ink);
}

.copy {
  margin: 0;
  font-size: 0.82rem;
}

@media (max-width: 640px) {
  .links {
    gap: 0.35rem 1rem;
  }
}
</style>
