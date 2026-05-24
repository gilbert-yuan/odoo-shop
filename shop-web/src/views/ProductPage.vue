<template>
  <div class="container page">
    <div v-if="loading" class="card block">Loading product...</div>
    <EmptyState
      v-else-if="!product"
      title="Product not found"
      description="This product might be unpublished or unavailable."
      cta-to="/shop"
      cta-label="Back to catalog"
    />
    <div v-else class="product-layout">
      <section class="card gallery">
        <img v-if="product.imageUrl" :src="product.imageUrl" :alt="product.displayName" />
        <div v-else class="placeholder">No image available</div>
      </section>
      <section class="card details">
        <p class="muted">Product #{{ product.id }}</p>
        <h1>{{ product.displayName }}</h1>
        <p class="price">{{ money(product.salePrice || product.listPrice) }}</p>
        <p class="muted desc">{{ plainDescription }}</p>

        <div v-if="combinationInfo" class="combo card">
          <h3>Variant info</h3>
          <p class="muted">
            Selected product variant: {{ combinationInfo.product_id || "N/A" }}
          </p>
        </div>

        <div class="actions">
          <label>
            Qty
            <input v-model.number="qty" class="input qty" type="number" min="1" />
          </label>
          <button class="button primary" type="button" @click="addToCart">Add to cart</button>
          <button class="button ghost" type="button" @click="addToWishlist">Wishlist</button>
          <button class="button ghost" type="button" @click="compare">Compare</button>
        </div>

        <div class="notify">
          <input
            v-model="stockEmail"
            class="input"
            type="email"
            placeholder="Email for back in stock alerts"
          />
          <button class="button ghost" type="button" @click="notifyStock">
            Notify me
          </button>
        </div>

        <p v-if="message" class="message">{{ message }}</p>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";

import EmptyState from "../components/shared/EmptyState.vue";
import { odooApi } from "../services/odooApi";
import { useCartStore } from "../stores/cart";
import { useWishlistStore } from "../stores/wishlist";
import { useCompareStore } from "../stores/compare";

const route = useRoute();
const cartStore = useCartStore();
const wishlistStore = useWishlistStore();
const compareStore = useCompareStore();

const loading = ref(false);
const product = ref(null);
const qty = ref(1);
const message = ref("");
const stockEmail = ref("");
const combinationInfo = ref(null);

const plainDescription = computed(() =>
  String(product.value?.description || "").replace(/<[^>]*>/g, "").slice(0, 360)
);

onMounted(async () => {
  loading.value = true;
  try {
    const id = Number(route.params.id);
    product.value = await odooApi.getProductById(id);
    if (product.value) {
      await odooApi.markRecentlyViewed(product.value.id);
      try {
        combinationInfo.value = await odooApi.getCombinationInfo({
          productTemplateId: product.value.id,
          productId: null,
          combination: [],
          addQty: 1
        });
      } catch {
        combinationInfo.value = null;
      }
    }
  } finally {
    loading.value = false;
  }
});

function money(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD"
  }).format(Number(value || 0));
}

async function addToCart() {
  if (!product.value) {
    return;
  }
  await cartStore.addToCart(product.value.id, Math.max(1, Number(qty.value || 1)));
  message.value = "Added to cart.";
}

async function addToWishlist() {
  if (!product.value) {
    return;
  }
  await wishlistStore.add(product.value.id);
  message.value = "Added to wishlist.";
}

async function compare() {
  if (!product.value) {
    return;
  }
  await compareStore.toggle(product.value.id);
  message.value = "Compare list updated.";
}

async function notifyStock() {
  if (!product.value || !stockEmail.value) {
    return;
  }
  await odooApi.addStockNotification(stockEmail.value, product.value.id);
  message.value = "Stock notification saved.";
}
</script>

<style scoped>
.page {
  padding-top: 1rem;
}

.block {
  padding: 1rem;
}

.product-layout {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 1rem;
}

.gallery {
  min-height: 420px;
  overflow: hidden;
  display: grid;
  place-items: center;
  background: linear-gradient(160deg, #f3f8f5 0%, #fdf4e5 100%);
}

.gallery img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder {
  color: var(--muted);
}

.details {
  padding: 1rem;
  display: grid;
  gap: 0.7rem;
  align-content: start;
}

h1 {
  margin: 0;
  line-height: 1.15;
}

.price {
  margin: 0;
  font-size: 1.6rem;
  font-weight: 700;
}

.desc {
  margin: 0;
}

.combo {
  padding: 0.8rem;
}

.combo h3 {
  margin: 0;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  align-items: end;
  gap: 0.5rem;
}

.qty {
  width: 90px;
}

.notify {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.5rem;
}

.message {
  margin: 0;
  color: var(--accent);
  font-weight: 600;
}

@media (max-width: 960px) {
  .product-layout {
    grid-template-columns: 1fr;
  }
}
</style>
