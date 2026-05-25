<template>
  <div class="container home">
    <section class="hero card rise-in">
      <div class="hero-content">
        <p class="eyebrow">Northstar Commerce</p>
        <h1>{{ t("home.heroTitle") }}</h1>
        <p class="muted">{{ t("home.heroSubtitle") }}</p>
        <div class="hero-actions">
          <RouterLink class="button primary" to="/shop">{{ t("home.ctaShop") }}</RouterLink>
          <RouterLink v-if="!sessionStore.isLoggedIn" class="button ghost" to="/account">
            {{ t("home.ctaSignIn") }}
          </RouterLink>
          <RouterLink v-else class="button ghost" to="/account/profile">
            {{ t("nav.profile") }}
          </RouterLink>
        </div>
      </div>
      <div class="hero-stat">
        <div>
          <strong>{{ cartStore.quantity }}</strong>
          <span>{{ t("nav.cart") }}</span>
        </div>
        <div>
          <strong>{{ wishlistStore.ids.length }}</strong>
          <span>{{ t("nav.wishlist") }}</span>
        </div>
        <div>
          <strong>{{ compareStore.ids.length }}</strong>
          <span>{{ t("nav.compare") }}</span>
        </div>
      </div>
    </section>

    <section v-if="categories.length" class="block">
      <h2 class="section-title">{{ t("home.browseCategories") }}</h2>
      <div class="categories">
        <RouterLink
          v-for="cat in categories.slice(0, 8)"
          :key="cat.id"
          class="cat-tile card"
          :to="`/shop?category=${cat.id}`"
        >
          <span>{{ cat.name }}</span>
        </RouterLink>
      </div>
    </section>

    <section class="block">
      <h2 class="section-title">{{ t("home.featured") }}</h2>
      <div class="cards">
        <template v-if="loading">
          <SkeletonCard v-for="i in 4" :key="`s${i}`" />
        </template>
        <template v-else>
          <ProductCard
            v-for="product in products"
            :key="product.id"
            :product="product"
            @add="addToCart"
            @compare="toggleCompare"
          />
        </template>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useHead } from "@unhead/vue";
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";

import ProductCard from "../components/catalog/ProductCard.vue";
import SkeletonCard from "../components/catalog/SkeletonCard.vue";
import { odooApi } from "../services/odooApi";
import { useCartStore } from "../stores/cart";
import { useCompareStore } from "../stores/compare";
import { useSessionStore } from "../stores/session";
import { useWishlistStore } from "../stores/wishlist";

const { t } = useI18n();

const cartStore = useCartStore();
const compareStore = useCompareStore();
const sessionStore = useSessionStore();
const wishlistStore = useWishlistStore();

const products = ref([]);
const categories = ref([]);
const loading = ref(false);

useHead({
  title: () => `${t("home.heroTitle")} | Northstar Commerce`,
  meta: [
    { name: "description", content: () => t("home.heroSubtitle") },
    { property: "og:title", content: () => t("home.heroTitle") },
    { property: "og:description", content: () => t("home.heroSubtitle") },
    { property: "og:type", content: "website" }
  ]
});

onMounted(async () => {
  loading.value = true;
  try {
    const [items, cats] = await Promise.all([
      odooApi.searchProducts({ limit: 8 }),
      odooApi.getCategories()
    ]);
    products.value = items;
    categories.value = cats;
  } finally {
    loading.value = false;
  }
});

async function addToCart(product) {
  await cartStore.addToCart(product.id, 1);
}

async function toggleCompare(product) {
  await compareStore.toggle(product.id);
}
</script>

<style scoped>
.home {
  display: grid;
  gap: 1.5rem;
  padding-top: 1.1rem;
}

.hero {
  padding: clamp(1rem, 3vw, 2.2rem);
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.2rem;
  background:
    radial-gradient(circle at 80% 10%, rgba(13, 128, 102, 0.18), transparent 30%),
    linear-gradient(160deg, #fffef7 0%, #f6fbf8 100%);
}

:global(html.dark) .hero {
  background:
    radial-gradient(circle at 80% 10%, rgba(45, 171, 139, 0.2), transparent 30%),
    linear-gradient(160deg, #1a2620 0%, #0f1612 100%);
}

.hero-content h1 {
  margin: 0.3rem 0 0.7rem;
  font-size: clamp(1.8rem, 3.2vw, 3rem);
  line-height: 1.08;
}

.eyebrow {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-size: 0.74rem;
  color: var(--muted);
  font-weight: 700;
}

.hero-actions {
  margin-top: 1rem;
  display: flex;
  gap: 0.6rem;
}

.hero-stat {
  display: grid;
  gap: 0.8rem;
  align-content: start;
}

.hero-stat div {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 0.9rem;
  display: grid;
  gap: 0.2rem;
}

.hero-stat strong {
  font-size: 1.5rem;
}

.hero-stat span {
  color: var(--muted);
  font-size: 0.9rem;
  text-transform: lowercase;
}

.block {
  display: grid;
  gap: 0.9rem;
}

.categories {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  gap: 0.7rem;
}

.cat-tile {
  padding: 1.1rem 1rem;
  display: grid;
  place-items: center;
  text-align: center;
  font-weight: 600;
  transition: transform 0.2s, border-color 0.2s;
}

.cat-tile:hover {
  transform: translateY(-2px);
  border-color: var(--accent);
}

.cards {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
}

@media (max-width: 1160px) {
  .cards {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 900px) {
  .hero {
    grid-template-columns: 1fr;
  }
  .cards {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 540px) {
  .cards {
    grid-template-columns: 1fr;
  }
}
</style>
