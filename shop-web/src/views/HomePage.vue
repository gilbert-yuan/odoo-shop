<template>
  <div class="home">
    <!-- Hero -->
    <section class="hero-wrap">
      <div class="container hero">
        <div class="hero-content rise-in">
          <p class="eyebrow">Research-grade peptides</p>
          <h1>{{ t("home.heroTitle") }}</h1>
          <p class="lede muted">{{ t("home.heroSubtitle") }}</p>
          <div class="hero-actions">
            <RouterLink class="button primary" to="/shop">{{ t("home.ctaShop") }}</RouterLink>
            <RouterLink class="button ghost" to="/coa">Verify COA →</RouterLink>
          </div>
          <ul class="bullets muted">
            <li>✓ 3rd-party HPLC + mass-spec on every batch</li>
            <li>✓ Discreet, temperature-controlled shipping</li>
            <li>✓ 14-day hassle-free returns</li>
          </ul>
        </div>
        <div class="hero-art rise-in">
          <div class="art-card">
            <span class="art-badge">FEATURED</span>
            <div class="art-name">Best-selling peptides</div>
            <div class="art-stats">
              <div><strong>{{ totalShown }}</strong><span>Products</span></div>
              <div><strong>≥99%</strong><span>Purity</span></div>
              <div><strong>72h</strong><span>Ships in</span></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <TrustStrip />

    <!-- Categories pills -->
    <section v-if="categories.length" class="container section">
      <header class="sec-head">
        <h2 class="section-title">{{ t("home.browseCategories") }}</h2>
      </header>
      <div class="cats">
        <RouterLink
          v-for="cat in categories.slice(0, 10)"
          :key="cat.id"
          :to="`/shop?category=${cat.id}`"
          class="cat"
        >
          <span class="dot"></span>
          {{ cat.name }}
        </RouterLink>
      </div>
    </section>

    <!-- Trending Now -->
    <section class="container section">
      <ProductCarousel
        title="Trending Now"
        emoji="🔥"
        :products="trending"
        :loading="loadingTrending"
        see-all-to="/shop"
        :wishlist-ids="wishlistStore.ids"
        @add="addToCart"
        @wishlist="toggleWishlist"
      />
    </section>

    <!-- Promo banner -->
    <section class="container section">
      <div class="promo card">
        <div class="promo-text">
          <p class="eyebrow">Member exclusive</p>
          <h3>Save 10% on your first order</h3>
          <p class="muted">Use code <code>WELCOME10</code> at checkout. Auto-applied when logged in.</p>
        </div>
        <RouterLink class="button primary" to="/account/register">Create account →</RouterLink>
      </div>
    </section>

    <!-- Best Sellers -->
    <section class="container section">
      <ProductCarousel
        title="Best Sellers"
        emoji="⭐"
        :products="bestSellers"
        :loading="loadingBestSellers"
        see-all-to="/shop"
        :wishlist-ids="wishlistStore.ids"
        @add="addToCart"
        @wishlist="toggleWishlist"
      />
    </section>

    <!-- New Arrivals -->
    <section class="container section">
      <ProductCarousel
        title="New Arrivals"
        emoji="✨"
        :products="newArrivals"
        :loading="loadingNew"
        see-all-to="/shop"
        :wishlist-ids="wishlistStore.ids"
        @add="addToCart"
        @wishlist="toggleWishlist"
      />
    </section>

    <!-- On Sale -->
    <section class="container section">
      <ProductCarousel
        title="On Sale"
        emoji="🏷"
        :products="onSale"
        :loading="loadingSale"
        see-all-to="/shop"
        :wishlist-ids="wishlistStore.ids"
        @add="addToCart"
        @wishlist="toggleWishlist"
      />
    </section>

    <!-- Why NextPept -->
    <section class="container section">
      <header class="sec-head">
        <h2 class="section-title">Why NextPept</h2>
      </header>
      <div class="why">
        <article class="why-card card">
          <span class="why-ic">🧪</span>
          <h3>Third-party tested</h3>
          <p class="muted">Independent HPLC + mass-spec for every batch. COAs published & searchable by lot.</p>
        </article>
        <article class="why-card card">
          <span class="why-ic">🚀</span>
          <h3>Fast worldwide shipping</h3>
          <p class="muted">Cold-chain packaging, tracked carriers, customs guidance. Most orders ship in 72h.</p>
        </article>
        <article class="why-card card">
          <span class="why-ic">💬</span>
          <h3>Expert support</h3>
          <p class="muted">Real humans, not bots. Response within one business day on any pre-sale question.</p>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useHead } from "@unhead/vue";
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";

import ProductCarousel from "../components/catalog/ProductCarousel.vue";
import TrustStrip from "../components/layout/TrustStrip.vue";
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

const categories = ref([]);
const trending = ref([]);
const bestSellers = ref([]);
const newArrivals = ref([]);
const onSale = ref([]);

const loadingTrending = ref(false);
const loadingBestSellers = ref(false);
const loadingNew = ref(false);
const loadingSale = ref(false);

const totalShown = computed(() =>
  new Set([
    ...trending.value.map((p) => p.id),
    ...bestSellers.value.map((p) => p.id),
    ...newArrivals.value.map((p) => p.id),
    ...onSale.value.map((p) => p.id)
  ]).size
);

useHead({
  title: () => `${t("home.heroTitle")} | NextPept`,
  meta: [
    { name: "description", content: () => t("home.heroSubtitle") },
    { property: "og:title", content: () => t("home.heroTitle") },
    { property: "og:description", content: () => t("home.heroSubtitle") },
    { property: "og:type", content: "website" }
  ]
});

async function loadCategory(ref, loadingRef, opts) {
  loadingRef.value = true;
  try {
    ref.value = await odooApi.searchProducts(opts);
  } finally {
    loadingRef.value = false;
  }
}

onMounted(async () => {
  odooApi.getCategories().then((c) => (categories.value = c));
  loadCategory(trending, loadingTrending, { limit: 10, order: "id desc" });
  loadCategory(bestSellers, loadingBestSellers, { limit: 10, order: "list_price desc" });
  loadCategory(newArrivals, loadingNew, { limit: 10, order: "create_date desc" });
  loadCategory(onSale, loadingSale, { limit: 10, order: "list_price asc" });
});

async function addToCart(product) {
  await cartStore.addToCart(product.id, 1);
}

async function toggleWishlist(product) {
  await wishlistStore.toggle(product.id);
}
</script>

<style scoped>
.home {
  display: grid;
  gap: 1.6rem;
}

/* Hero */
.hero-wrap {
  background:
    radial-gradient(circle at 88% 18%, rgba(13, 128, 102, 0.18), transparent 30%),
    radial-gradient(circle at 18% 75%, rgba(245, 166, 35, 0.15), transparent 35%),
    linear-gradient(155deg, #f5fdf6 0%, #fffaf0 100%);
  padding: 2rem 0 1.8rem;
  border-bottom: 1px solid var(--line);
}

:global(html.dark) .hero-wrap {
  background:
    radial-gradient(circle at 88% 18%, rgba(45, 171, 139, 0.2), transparent 30%),
    radial-gradient(circle at 18% 75%, rgba(245, 166, 35, 0.12), transparent 35%),
    linear-gradient(155deg, #182320 0%, #0f1612 100%);
}

.hero {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 2rem;
  align-items: center;
}

.eyebrow {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.72rem;
  color: var(--accent);
  font-weight: 700;
}

.hero-content h1 {
  margin: 0.4rem 0 0.6rem;
  font-size: clamp(1.9rem, 3.4vw, 3rem);
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.lede {
  margin: 0 0 1rem;
  font-size: 1.02rem;
}

.hero-actions {
  display: flex;
  gap: 0.55rem;
  margin-bottom: 1.1rem;
}

.bullets {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 0.3rem;
  font-size: 0.9rem;
}

.hero-art {
  display: grid;
  place-items: center;
}

.art-card {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: var(--radius-lg);
  padding: 1.4rem 1.5rem;
  display: grid;
  gap: 0.85rem;
  position: relative;
  width: 100%;
  max-width: 360px;
  box-shadow: var(--shadow);
}

.art-badge {
  position: absolute;
  top: -0.7rem;
  left: 1.2rem;
  background: var(--accent);
  color: #fff;
  padding: 0.25rem 0.7rem;
  font-size: 0.7rem;
  font-weight: 700;
  border-radius: 4px;
  letter-spacing: 0.06em;
}

.art-name {
  font-size: 1.1rem;
  font-weight: 700;
}

.art-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.6rem;
}

.art-stats div {
  display: grid;
  gap: 0.15rem;
  text-align: center;
  padding: 0.7rem 0.3rem;
  background: var(--accent-soft);
  border-radius: var(--radius-md);
}

.art-stats strong {
  font-size: 1.05rem;
  color: var(--accent);
}

.art-stats span {
  font-size: 0.72rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Sections */
.section {
  display: grid;
  gap: 0.6rem;
}

.sec-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.cats {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.cat {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.45rem 0.85rem;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: var(--panel);
  font-size: 0.88rem;
  font-weight: 600;
  transition: border-color 0.15s, transform 0.15s, color 0.15s;
}

.cat:hover {
  border-color: var(--accent);
  color: var(--accent);
  transform: translateY(-1px);
}

.dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--accent);
}

/* Promo */
.promo {
  padding: 1.2rem 1.4rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  background: linear-gradient(120deg, var(--accent-soft) 0%, var(--panel) 100%);
}

.promo-text h3 {
  margin: 0.25rem 0 0.3rem;
}

.promo-text p {
  margin: 0;
}

.promo code {
  background: var(--ink);
  color: var(--panel);
  padding: 0.1rem 0.5rem;
  border-radius: 4px;
  font-family: ui-monospace, monospace;
  font-size: 0.85rem;
}

/* Why */
.why {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.9rem;
}

.why-card {
  padding: 1.2rem;
  display: grid;
  gap: 0.4rem;
}

.why-ic {
  font-size: 1.7rem;
}

.why-card h3 {
  margin: 0;
}

.why-card p {
  margin: 0;
  font-size: 0.92rem;
  line-height: 1.5;
}

@media (max-width: 900px) {
  .hero {
    grid-template-columns: 1fr;
    gap: 1.2rem;
  }
  .hero-art {
    order: -1;
  }
  .why {
    grid-template-columns: 1fr;
  }
  .promo {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
