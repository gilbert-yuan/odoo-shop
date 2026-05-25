<template>
  <article class="card product rise-in">
    <RouterLink :to="`/product/${product.id}`" class="image-wrap">
      <img v-if="product.imageUrl" :src="product.imageUrl" :alt="product.name" />
      <div v-else class="placeholder">No image</div>
      <span v-if="product.hasDiscountedPrice" class="badge">Sale</span>
    </RouterLink>
    <div class="body">
      <RouterLink :to="`/product/${product.id}`" class="name">
        {{ product.displayName }}
      </RouterLink>
      <p class="muted desc">{{ product.shortDescription || "Curated product for your store." }}</p>
      <div class="bottom">
        <span class="price">
          <strong>{{ formatMoney(product.salePrice || product.listPrice) }}</strong>
          <small v-if="product.hasDiscountedPrice" class="list">
            {{ formatMoney(product.listPrice) }}
          </small>
        </span>
        <div class="actions">
          <button class="button ghost mini" type="button" @click="$emit('compare', product)">
            {{ t("nav.compare") }}
          </button>
          <button class="button primary mini" type="button" @click="$emit('add', product)">
            {{ t("common.addToCart") }}
          </button>
        </div>
      </div>
    </div>
  </article>
</template>

<script setup>
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";

import { formatMoney } from "../../utils/format";

const { t } = useI18n();

defineProps({
  product: {
    type: Object,
    required: true
  }
});

defineEmits(["add", "compare"]);
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
  position: relative;
}

:global(html.dark) .image-wrap {
  background: linear-gradient(160deg, #1f2a25 0%, #283531 100%);
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

.badge {
  position: absolute;
  top: 0.7rem;
  left: 0.7rem;
  background: var(--danger);
  color: #fff;
  padding: 0.18rem 0.55rem;
  border-radius: 999px;
  font-size: 0.74rem;
  font-weight: 600;
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

.price {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  line-height: 1.2;
}

.price .list {
  color: var(--muted);
  text-decoration: line-through;
  font-size: 0.78rem;
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
