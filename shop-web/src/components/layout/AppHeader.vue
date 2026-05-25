<template>
  <header class="header">
    <div class="container row">
      <RouterLink class="brand" to="/" @click="closeMenu">
        <span class="badge">N</span>
        <span class="brand-text">NextPept</span>
      </RouterLink>

      <nav class="nav desktop">
        <RouterLink to="/shop">{{ t("nav.shop") }}</RouterLink>
        <RouterLink to="/wishlist">{{ t("nav.wishlist") }}</RouterLink>
        <RouterLink to="/compare">{{ t("nav.compare") }}</RouterLink>
        <RouterLink to="/account/orders">{{ t("nav.orders") }}</RouterLink>
      </nav>

      <div class="actions">
        <button class="icon" type="button" :aria-label="t('common.search')" @click="toggleSearch">
          🔍
        </button>
        <button
          class="icon desktop-only"
          type="button"
          :aria-label="darkMode ? 'Light mode' : 'Dark mode'"
          @click="toggleDark"
        >
          {{ darkMode ? "☀️" : "🌙" }}
        </button>
        <LangSwitcher class="desktop-only" />
        <RouterLink class="cart" to="/cart">
          <span class="cart-label">{{ t("nav.cart") }}</span>
          <span class="pill">{{ cartStore.quantity }}</span>
        </RouterLink>
        <RouterLink class="button ghost desktop-only" to="/account">
          {{ sessionStore.isLoggedIn ? sessionStore.displayName : t("nav.signIn") }}
        </RouterLink>
        <button
          class="icon hamburger mobile-only"
          type="button"
          :aria-label="menuOpen ? 'Close menu' : 'Open menu'"
          :aria-expanded="menuOpen"
          @click="toggleMenu"
        >
          <span class="bars" :class="{ open: menuOpen }">
            <span></span><span></span><span></span>
          </span>
        </button>
      </div>
    </div>

    <div v-if="searchOpen" class="search-panel">
      <div class="container search-wrap">
        <input
          v-model="keyword"
          class="input"
          type="search"
          :placeholder="t('common.search')"
          @keyup.enter="goSearch"
        />
        <button class="button primary" type="button" @click="goSearch">
          {{ t("common.search") }}
        </button>
      </div>
    </div>

    <!-- Mobile drawer -->
    <transition name="fade">
      <div v-if="menuOpen" class="drawer-overlay" @click="closeMenu"></div>
    </transition>
    <transition name="slide">
      <aside v-if="menuOpen" class="drawer" @click.stop>
        <div class="drawer-head">
          <strong>{{ sessionStore.isLoggedIn ? sessionStore.displayName : t("nav.account") }}</strong>
          <button class="icon" type="button" aria-label="Close" @click="closeMenu">✕</button>
        </div>

        <nav class="drawer-nav">
          <RouterLink to="/" @click="closeMenu">{{ t("nav.home") }}</RouterLink>
          <RouterLink to="/shop" @click="closeMenu">{{ t("nav.shop") }}</RouterLink>
          <RouterLink to="/wishlist" @click="closeMenu">{{ t("nav.wishlist") }}</RouterLink>
          <RouterLink to="/compare" @click="closeMenu">{{ t("nav.compare") }}</RouterLink>
          <RouterLink to="/cart" @click="closeMenu">
            {{ t("nav.cart") }} <span class="count">{{ cartStore.quantity }}</span>
          </RouterLink>
          <RouterLink v-if="sessionStore.isLoggedIn" to="/account/orders" @click="closeMenu">
            {{ t("nav.orders") }}
          </RouterLink>
          <RouterLink v-if="sessionStore.isLoggedIn" to="/account/profile" @click="closeMenu">
            {{ t("nav.profile") }}
          </RouterLink>
          <RouterLink v-if="!sessionStore.isLoggedIn" to="/account" @click="closeMenu">
            {{ t("nav.signIn") }}
          </RouterLink>
          <RouterLink v-if="!sessionStore.isLoggedIn" to="/account/register" @click="closeMenu">
            {{ t("auth.register") }}
          </RouterLink>
        </nav>

        <div class="drawer-section">
          <span class="muted small">Language</span>
          <LangSwitcher />
        </div>

        <div class="drawer-section">
          <span class="muted small">Theme</span>
          <button class="button ghost wide" type="button" @click="toggleDark">
            {{ darkMode ? "☀️ Light mode" : "🌙 Dark mode" }}
          </button>
        </div>

        <nav class="drawer-footer">
          <RouterLink to="/faq" @click="closeMenu">FAQ</RouterLink>
          <RouterLink to="/contact" @click="closeMenu">Contact</RouterLink>
          <RouterLink to="/about" @click="closeMenu">About</RouterLink>
        </nav>

        <button
          v-if="sessionStore.isLoggedIn"
          class="button ghost wide signout"
          type="button"
          @click="signOut"
        >
          {{ t("nav.signOut") }}
        </button>
      </aside>
    </transition>
  </header>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useRoute, useRouter, RouterLink } from "vue-router";

import LangSwitcher from "./LangSwitcher.vue";
import { useCartStore } from "../../stores/cart";
import { useSessionStore } from "../../stores/session";

const { t } = useI18n();
const route = useRoute();
const router = useRouter();
const cartStore = useCartStore();
const sessionStore = useSessionStore();

const searchOpen = ref(false);
const keyword = ref("");
const darkMode = ref(false);
const menuOpen = ref(false);

onMounted(() => {
  const saved = localStorage.getItem("odoo_shop_theme");
  if (saved === "dark") {
    darkMode.value = true;
    document.documentElement.classList.add("dark");
  }
});

watch(() => route.fullPath, () => {
  menuOpen.value = false;
});

watch(menuOpen, (open) => {
  document.body.style.overflow = open ? "hidden" : "";
});

function toggleSearch() {
  searchOpen.value = !searchOpen.value;
  if (searchOpen.value) menuOpen.value = false;
}

function toggleMenu() {
  menuOpen.value = !menuOpen.value;
  if (menuOpen.value) searchOpen.value = false;
}

function closeMenu() {
  menuOpen.value = false;
}

function toggleDark() {
  darkMode.value = !darkMode.value;
  document.documentElement.classList.toggle("dark", darkMode.value);
  localStorage.setItem("odoo_shop_theme", darkMode.value ? "dark" : "light");
}

function goSearch() {
  router.push({
    path: "/shop",
    query: keyword.value ? { search: keyword.value } : {}
  });
  searchOpen.value = false;
}

async function signOut() {
  await sessionStore.logout();
  closeMenu();
  router.push("/account");
}
</script>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 30;
  backdrop-filter: blur(16px);
  background: rgba(246, 244, 239, 0.86);
  border-bottom: 1px solid rgba(217, 211, 199, 0.85);
}

:global(html.dark) .header {
  background: rgba(20, 30, 26, 0.86);
  border-bottom-color: rgba(60, 75, 70, 0.5);
}

.row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.6rem;
  min-height: 64px;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  flex-shrink: 0;
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

.nav.desktop {
  display: flex;
  gap: 1.1rem;
  font-weight: 600;
  color: var(--muted);
}

.nav.desktop a.router-link-active {
  color: var(--ink);
}

.actions {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.icon {
  border: 0;
  background: transparent;
  cursor: pointer;
  font-size: 1.05rem;
  padding: 0.4rem;
  border-radius: 8px;
  color: var(--ink);
  line-height: 1;
}

.icon:hover {
  background: rgba(13, 128, 102, 0.08);
}

.cart {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 0.45rem 0.75rem;
  background: #fff;
  font-weight: 600;
}

:global(html.dark) .cart {
  background: rgba(255, 255, 255, 0.06);
}

.pill {
  min-width: 1.4rem;
  height: 1.4rem;
  border-radius: 999px;
  display: inline-grid;
  place-items: center;
  font-size: 0.76rem;
  color: #fff;
  background: var(--accent);
  padding: 0 0.4rem;
}

.search-panel {
  border-top: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.7);
}

:global(html.dark) .search-panel {
  background: rgba(20, 30, 26, 0.6);
}

.search-wrap {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.7rem;
  padding: 0.7rem 0 1rem;
}

/* Hamburger */
.hamburger {
  display: none;
}

.bars {
  display: inline-block;
  width: 22px;
  height: 16px;
  position: relative;
}

.bars span {
  position: absolute;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--ink);
  border-radius: 2px;
  transition: transform 0.25s, opacity 0.2s, top 0.25s;
}

.bars span:nth-child(1) { top: 0; }
.bars span:nth-child(2) { top: 7px; }
.bars span:nth-child(3) { top: 14px; }

.bars.open span:nth-child(1) { top: 7px; transform: rotate(45deg); }
.bars.open span:nth-child(2) { opacity: 0; }
.bars.open span:nth-child(3) { top: 7px; transform: rotate(-45deg); }

/* Drawer */
.drawer-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 40;
}

.drawer {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: min(86vw, 340px);
  background: var(--panel);
  z-index: 50;
  box-shadow: -20px 0 40px rgba(0, 0, 0, 0.18);
  display: grid;
  grid-template-rows: auto 1fr auto auto auto auto;
  padding: 0;
  overflow-y: auto;
}

.drawer-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.2rem;
  border-bottom: 1px solid var(--line);
}

.drawer-head strong {
  font-size: 1.05rem;
}

.drawer-nav {
  display: grid;
  padding: 0.5rem 0.5rem;
}

.drawer-nav a {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.85rem 0.8rem;
  border-radius: 10px;
  font-weight: 600;
  color: var(--ink);
}

.drawer-nav a:hover,
.drawer-nav a.router-link-exact-active {
  background: var(--accent-soft);
  color: var(--accent);
}

.count {
  background: var(--accent);
  color: #fff;
  border-radius: 999px;
  padding: 0.1rem 0.55rem;
  font-size: 0.78rem;
}

.drawer-section {
  padding: 0.7rem 1.2rem;
  border-top: 1px solid var(--line);
  display: grid;
  gap: 0.45rem;
}

.drawer-footer {
  border-top: 1px solid var(--line);
  padding: 0.6rem 0.5rem;
  display: grid;
}

.drawer-footer a {
  padding: 0.7rem 0.8rem;
  border-radius: 10px;
  font-size: 0.9rem;
  color: var(--muted);
}

.drawer-footer a:hover {
  color: var(--ink);
}

.wide {
  width: 100%;
}

.signout {
  margin: 0.8rem 1.2rem 1.2rem;
}

.small {
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.28s ease;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
}

/* Responsive */
.mobile-only { display: none; }

@media (max-width: 980px) {
  .nav.desktop { display: none; }
  .desktop-only { display: none; }
  .mobile-only { display: inline-flex; }
  .hamburger { display: inline-flex; }
  .row { min-height: 60px; }
}

@media (max-width: 520px) {
  .brand-text { display: none; }
  .cart-label { display: none; }
  .cart { padding: 0.4rem 0.55rem; }
  .actions { gap: 0.25rem; }
}
</style>
