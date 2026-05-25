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
      <ProductGallery
        :images="galleryImages"
        :override="variantImage"
        :alt="product.displayName"
      />
      <section class="card details">
        <p class="muted">Product #{{ product.id }}</p>
        <h1>{{ product.displayName }}</h1>
        <p class="price">
          <strong>{{ money(displayPrice) }}</strong>
          <span v-if="product.listPrice && product.listPrice !== displayPrice" class="list">
            {{ money(product.listPrice) }}
          </span>
        </p>
        <p :class="['stock', stockClass]">{{ stockLabel }}</p>

        <p v-if="plainDescription" class="muted desc">{{ plainDescription }}</p>

        <VariantSelector
          v-if="product.attributeLines?.length"
          :attribute-lines="product.attributeLines"
          v-model="selectedPtavIds"
          :currency="currencyCode"
        />

        <div class="actions">
          <label>
            Qty
            <input v-model.number="qty" class="input qty" type="number" min="1" />
          </label>
          <button
            class="button primary"
            type="button"
            :disabled="!canBuy"
            @click="addToCart"
          >
            Add to cart
          </button>
          <button class="button ghost" type="button" @click="addToWishlist">Wishlist</button>
          <button class="button ghost" type="button" @click="compare">Compare</button>
        </div>

        <div v-if="!canBuy" class="notify">
          <input
            v-model="stockEmail"
            class="input"
            type="email"
            placeholder="Email for back in stock alerts"
          />
          <button class="button ghost" type="button" @click="notifyStock">Notify me</button>
        </div>

        <p v-if="message" class="message">{{ message }}</p>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useHead } from "@unhead/vue";
import { useRoute } from "vue-router";

import EmptyState from "../components/shared/EmptyState.vue";
import ProductGallery from "../components/catalog/ProductGallery.vue";
import VariantSelector from "../components/catalog/VariantSelector.vue";
import { odooApi } from "../services/odooApi";
import { useCartStore } from "../stores/cart";
import { useWishlistStore } from "../stores/wishlist";
import { useCompareStore } from "../stores/compare";
import { formatMoney } from "../utils/format";

const route = useRoute();
const cartStore = useCartStore();
const wishlistStore = useWishlistStore();
const compareStore = useCompareStore();

const loading = ref(false);
const product = ref(null);
const qty = ref(1);
const message = ref("");
const stockEmail = ref("");
const selectedPtavIds = ref([]);
const combination = ref(null);

const plainDescription = computed(() =>
  String(product.value?.description || "").replace(/<[^>]*>/g, "").slice(0, 360)
);

const currencyCode = computed(() => "USD");

const galleryImages = computed(() => product.value?.imageUrls || []);

const variantImage = computed(() => combination.value?.image_url || "");

const matchedVariant = computed(() => {
  if (!product.value?.variants?.length) return null;
  const want = new Set(selectedPtavIds.value.map(Number));
  return product.value.variants.find((v) => {
    const ids = (v.ptav_ids || []).map(Number);
    if (ids.length !== want.size) return false;
    return ids.every((id) => want.has(id));
  });
});

const displayPrice = computed(() => {
  if (combination.value?.price !== undefined) {
    return Number(combination.value.price);
  }
  if (matchedVariant.value?.price !== undefined) {
    return Number(matchedVariant.value.price);
  }
  return Number(product.value?.salePrice || product.value?.listPrice || 0);
});

const isInStock = computed(() => {
  if (combination.value && "is_in_stock" in combination.value) {
    return Boolean(combination.value.is_in_stock);
  }
  if (matchedVariant.value) {
    return Boolean(matchedVariant.value.is_in_stock);
  }
  return true;
});

const stockLabel = computed(() => (isInStock.value ? "In stock" : "Out of stock"));
const stockClass = computed(() => (isInStock.value ? "ok" : "bad"));
const canBuy = computed(() => isInStock.value && product.value?.canBeSold);

useHead({
  title: () => (product.value ? `${product.value.displayName} | Northstar Commerce` : "Product"),
  meta: [
    { name: "description", content: () => plainDescription.value || "Product details" },
    { property: "og:title", content: () => product.value?.displayName || "" },
    { property: "og:description", content: () => plainDescription.value || "" },
    { property: "og:image", content: () => product.value?.imageUrl || "" },
    { property: "og:type", content: "product" }
  ]
});

watch(selectedPtavIds, async (ids) => {
  if (!product.value || !ids.length) return;
  try {
    combination.value = await odooApi.getProductCombination(product.value.id, {
      ptavIds: ids,
      addQty: qty.value
    });
  } catch {
    combination.value = null;
  }
});

onMounted(async () => {
  loading.value = true;
  try {
    const id = Number(route.params.id);
    product.value = await odooApi.getProductById(id);
  } finally {
    loading.value = false;
  }
});

function money(value) {
  return formatMoney(value, currencyCode.value);
}

async function addToCart() {
  if (!product.value) return;
  const variantId = combination.value?.product_id || matchedVariant.value?.id || product.value.id;
  await cartStore.addToCart(variantId, Math.max(1, Number(qty.value || 1)));
  message.value = "Added to cart.";
}

async function addToWishlist() {
  if (!product.value) return;
  const variantId = matchedVariant.value?.id || product.value.id;
  await wishlistStore.add(variantId);
  message.value = "Added to wishlist.";
}

async function compare() {
  if (!product.value) return;
  await compareStore.toggle(product.value.id);
  message.value = "Compare list updated.";
}

async function notifyStock() {
  if (!product.value || !stockEmail.value) return;
  const variantId = matchedVariant.value?.id || product.value.id;
  await odooApi.addStockNotification(stockEmail.value, variantId);
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
  display: flex;
  align-items: baseline;
  gap: 0.6rem;
}

.price .list {
  font-size: 1rem;
  font-weight: 400;
  color: var(--muted);
  text-decoration: line-through;
}

.stock {
  margin: 0;
  font-weight: 600;
  font-size: 0.88rem;
}

.stock.ok {
  color: var(--accent);
}

.stock.bad {
  color: var(--danger);
}

.desc {
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
