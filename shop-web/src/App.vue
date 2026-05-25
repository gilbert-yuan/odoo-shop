<template>
  <div class="shell">
    <AppHeader />
    <main>
      <RouterView />
    </main>
    <AppFooter />
    <CookieBanner />
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { RouterView } from "vue-router";

import AppHeader from "./components/layout/AppHeader.vue";
import AppFooter from "./components/layout/AppFooter.vue";
import CookieBanner from "./components/layout/CookieBanner.vue";
import { useSessionStore } from "./stores/session";
import { useCartStore } from "./stores/cart";
import { useWishlistStore } from "./stores/wishlist";
import { useCompareStore } from "./stores/compare";

const sessionStore = useSessionStore();
const cartStore = useCartStore();
const wishlistStore = useWishlistStore();
const compareStore = useCompareStore();

onMounted(async () => {
  await sessionStore.bootstrap();
  await Promise.all([
    cartStore.refresh(),
    wishlistStore.refresh(),
    compareStore.restoreFromStorage()
  ]);
});
</script>

<style scoped>
.shell {
  min-height: 100vh;
  display: grid;
  grid-template-rows: auto 1fr auto;
}

main {
  padding-bottom: 2rem;
}
</style>
