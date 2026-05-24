<template>
  <header class="header">
    <div class="container row">
      <RouterLink class="brand" to="/">
        <span class="badge">N</span>
        Northstar Commerce
      </RouterLink>

      <nav class="nav">
        <RouterLink to="/shop">Shop</RouterLink>
        <RouterLink to="/wishlist">Wishlist</RouterLink>
        <RouterLink to="/compare">Compare</RouterLink>
        <RouterLink to="/account/orders">Orders</RouterLink>
      </nav>

      <div class="actions">
        <button class="button ghost" type="button" @click="toggleSearch">
          Search
        </button>
        <RouterLink class="cart" to="/cart">
          Cart
          <span class="pill">{{ cartStore.quantity }}</span>
        </RouterLink>
        <RouterLink class="button ghost" to="/account">
          {{ sessionStore.isLoggedIn ? sessionStore.displayName : "Sign in" }}
        </RouterLink>
      </div>
    </div>

    <div v-if="searchOpen" class="search-panel">
      <div class="container search-wrap">
        <input
          v-model="keyword"
          class="input"
          type="search"
          placeholder="Search products..."
          @keyup.enter="goSearch"
        />
        <button class="button primary" type="button" @click="goSearch">
          Search
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from "vue";
import { useRouter, RouterLink } from "vue-router";

import { useCartStore } from "../../stores/cart";
import { useSessionStore } from "../../stores/session";

const router = useRouter();
const cartStore = useCartStore();
const sessionStore = useSessionStore();

const searchOpen = ref(false);
const keyword = ref("");

function toggleSearch() {
  searchOpen.value = !searchOpen.value;
}

function goSearch() {
  router.push({
    path: "/shop",
    query: keyword.value ? { search: keyword.value } : {}
  });
  searchOpen.value = false;
}
</script>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 20;
  backdrop-filter: blur(16px);
  background: rgba(246, 244, 239, 0.84);
  border-bottom: 1px solid rgba(217, 211, 199, 0.85);
}

.row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  min-height: 72px;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  font-weight: 700;
  letter-spacing: -0.01em;
}

.badge {
  width: 1.8rem;
  height: 1.8rem;
  border-radius: 0.5rem;
  display: inline-grid;
  place-items: center;
  font-size: 0.95rem;
  color: #fff;
  background: linear-gradient(140deg, #0d8066 0%, #264653 100%);
}

.nav {
  display: flex;
  gap: 1.1rem;
  font-weight: 600;
  color: var(--muted);
}

.nav a.router-link-active {
  color: var(--ink);
}

.actions {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.cart {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 0.5rem 0.8rem;
  background: #fff;
  font-weight: 600;
}

.pill {
  min-width: 1.45rem;
  height: 1.45rem;
  border-radius: 999px;
  display: inline-grid;
  place-items: center;
  font-size: 0.78rem;
  color: #fff;
  background: var(--accent);
}

.search-panel {
  border-top: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.7);
}

.search-wrap {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.7rem;
  padding: 0.7rem 0 1rem;
}

@media (max-width: 980px) {
  .nav {
    display: none;
  }
}
</style>
