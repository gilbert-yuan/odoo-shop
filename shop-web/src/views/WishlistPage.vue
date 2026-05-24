<template>
  <div class="container wishlist">
    <header class="head">
      <h1 class="section-title">Wishlist</h1>
      <p class="muted">Save favorites and move them to cart anytime.</p>
    </header>

    <div v-if="wishlistStore.loading" class="card block">Loading wishlist...</div>
    <EmptyState
      v-else-if="!wishlistStore.items.length"
      title="Wishlist is empty"
      description="Tap the wishlist button on any product."
      cta-to="/shop"
      cta-label="Explore products"
    />
    <section v-else class="grid cards">
      <article v-for="item in wishlistStore.items" :key="item.id" class="card entry">
        <img v-if="item.imageUrl" :src="item.imageUrl" :alt="item.name" />
        <div class="info">
          <h3>{{ item.displayName }}</h3>
          <p class="muted">{{ money(item.salePrice || item.listPrice) }}</p>
          <div class="actions">
            <button class="button primary" type="button" @click="addToCart(item)">Add to cart</button>
            <RouterLink class="button ghost" :to="`/product/${item.id}`">Details</RouterLink>
          </div>
        </div>
      </article>
    </section>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { RouterLink } from "vue-router";

import EmptyState from "../components/shared/EmptyState.vue";
import { useWishlistStore } from "../stores/wishlist";
import { useCartStore } from "../stores/cart";

const wishlistStore = useWishlistStore();
const cartStore = useCartStore();

onMounted(async () => {
  await wishlistStore.refresh();
});

function money(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD"
  }).format(Number(value || 0));
}

async function addToCart(product) {
  await cartStore.addToCart(product.id, 1);
}
</script>

<style scoped>
.wishlist {
  display: grid;
  gap: 1rem;
  padding-top: 1rem;
}

.head {
  display: grid;
  gap: 0.3rem;
}

.block {
  padding: 1rem;
}

.cards {
  grid-template-columns: repeat(2, 1fr);
}

.entry {
  overflow: hidden;
  display: grid;
  grid-template-columns: 180px 1fr;
}

.entry img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.info {
  padding: 0.9rem;
  display: grid;
  gap: 0.6rem;
}

h3 {
  margin: 0;
}

p {
  margin: 0;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

@media (max-width: 920px) {
  .cards {
    grid-template-columns: 1fr;
  }

  .entry {
    grid-template-columns: 1fr;
  }
}
</style>
