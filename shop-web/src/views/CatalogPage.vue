<template>
  <div class="container catalog">
    <header class="head">
      <h1 class="section-title">{{ t("nav.shop") }}</h1>
      <p class="muted">{{ catalogStore.products.length }} {{ t("nav.shop").toLowerCase() }}</p>
    </header>

    <div class="layout">
      <CatalogFilters
        :categories="catalogStore.categories"
        :filters="catalogStore.filters"
        @apply="applyFilters"
      />

      <section>
        <div v-if="catalogStore.loading" class="grid cards">
          <SkeletonCard v-for="i in 6" :key="`s${i}`" />
        </div>
        <div v-else-if="!catalogStore.products.length">
          <EmptyState
            title="No products found"
            description="Adjust filters or search another keyword."
          />
        </div>
        <div v-else class="grid cards">
          <ProductCard
            v-for="product in catalogStore.products"
            :key="product.id"
            :product="product"
            :in-wishlist="wishlistStore.ids.includes(product.id)"
            @add="addToCart"
            @wishlist="toggleWishlist"
          />
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useHead } from "@unhead/vue";
import { useI18n } from "vue-i18n";
import { useRoute, useRouter } from "vue-router";

import CatalogFilters from "../components/catalog/CatalogFilters.vue";
import ProductCard from "../components/catalog/ProductCard.vue";
import SkeletonCard from "../components/catalog/SkeletonCard.vue";
import EmptyState from "../components/shared/EmptyState.vue";
import { useCatalogStore } from "../stores/catalog";
import { useCartStore } from "../stores/cart";
import { useCompareStore } from "../stores/compare";
import { useWishlistStore } from "../stores/wishlist";

const { t } = useI18n();
const route = useRoute();
const router = useRouter();

const catalogStore = useCatalogStore();
const cartStore = useCartStore();
const compareStore = useCompareStore();
const wishlistStore = useWishlistStore();

useHead({
  title: () => `${t("nav.shop")} | Northstar Commerce`,
  meta: [{ name: "description", content: () => t("home.heroSubtitle") }]
});

onMounted(async () => {
  await catalogStore.loadCategories();
  const search = String(route.query.search || "");
  if (search) {
    catalogStore.setSearch(search);
  }
  const category = route.query.category ? Number(route.query.category) : null;
  if (category) {
    catalogStore.setCategory(category);
  }
  await catalogStore.loadProducts();
});

async function applyFilters(payload) {
  catalogStore.setSearch(payload.search);
  catalogStore.setCategory(payload.categoryId);
  catalogStore.setPriceRange({
    min: payload.minPrice,
    max: payload.maxPrice
  });
  catalogStore.setOrder(payload.order);

  await catalogStore.loadProducts();
  await router.replace({
    path: "/shop",
    query: payload.search ? { search: payload.search } : {}
  });
}

async function addToCart(product) {
  await cartStore.addToCart(product.id, 1);
}

async function toggleWishlist(product) {
  await wishlistStore.toggle(product.id);
}

async function compareProduct(product) {
  await compareStore.toggle(product.id);
}
</script>

<style scoped>
.catalog {
  display: grid;
  gap: 1rem;
  padding-top: 1rem;
}

.head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.layout {
  display: grid;
  grid-template-columns: 290px 1fr;
  gap: 1rem;
  align-items: start;
}

.cards {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.loading {
  padding: 1rem;
}

@media (max-width: 1160px) {
  .cards {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 900px) {
  .layout {
    grid-template-columns: 1fr;
  }

  .cards {
    grid-template-columns: 1fr;
  }
}
</style>
