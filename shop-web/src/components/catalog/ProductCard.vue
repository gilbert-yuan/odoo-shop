<template>
  <article class="card product rise-in">
    <RouterLink :to="`/product/${product.id}`" class="image-wrap">
      <img v-if="product.imageUrl" :src="product.imageUrl" :alt="product.name" />
      <div v-else class="placeholder">No image</div>
    </RouterLink>
    <div class="body">
      <RouterLink :to="`/product/${product.id}`" class="name">
        {{ product.displayName }}
      </RouterLink>
      <p class="muted desc">{{ product.shortDescription || "Curated product for your store." }}</p>
      <div class="bottom">
        <strong>{{ currency(product.salePrice || product.listPrice) }}</strong>
        <div class="actions">
          <button class="button ghost mini" type="button" @click="$emit('compare', product)">
            Compare
          </button>
          <button class="button primary mini" type="button" @click="$emit('add', product)">
            Add
          </button>
        </div>
      </div>
    </div>
  </article>
</template>

<script setup>
import { RouterLink } from "vue-router";

defineProps({
  product: {
    type: Object,
    required: true
  }
});

defineEmits(["add", "compare"]);

function currency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD"
  }).format(Number(value || 0));
}
</script>

<style scoped>
.product {
  overflow: hidden;
  display: grid;
  grid-template-rows: 220px 1fr;
}

.image-wrap {
  background: linear-gradient(160deg, #f3f8f5 0%, #fdf4e5 100%);
  display: grid;
  place-items: center;
  overflow: hidden;
}

img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder {
  color: var(--muted);
  font-size: 0.9rem;
}

.body {
  display: grid;
  gap: 0.6rem;
  padding: 1rem;
}

.name {
  font-weight: 700;
  line-height: 1.3;
}

.desc {
  margin: 0;
  font-size: 0.92rem;
}

.bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
}

.actions {
  display: flex;
  gap: 0.4rem;
}

.mini {
  padding: 0.45rem 0.8rem;
  font-size: 0.84rem;
}
</style>
