<template>
  <article class="card product rise-in">
    <RouterLink :to="`/product/${product.id}`" class="image-wrap">
      <img v-if="product.imageUrl" :src="product.imageUrl" :alt="product.name" loading="lazy" />
      <div v-else class="placeholder">No image</div>

      <span
        v-if="ribbonLabel"
        class="ribbon"
        :style="ribbonStyle"
      >{{ ribbonLabel }}</span>

      <span v-if="discountPercent" class="discount">−{{ discountPercent }}%</span>

      <button
        class="wishlist"
        type="button"
        :aria-label="inWishlist ? 'Remove from wishlist' : 'Add to wishlist'"
        :class="{ active: inWishlist }"
        @click.prevent="$emit('wishlist', product)"
      >
        {{ inWishlist ? "♥" : "♡" }}
      </button>
    </RouterLink>

    <div class="body">
      <p v-if="brand" class="brand">{{ brand }}</p>
      <RouterLink :to="`/product/${product.id}`" class="name">
        {{ product.displayName }}
      </RouterLink>

      <div v-if="product.ratingCount > 0" class="rating">
        <span class="stars" :style="{ '--pct': starPct + '%' }">★★★★★</span>
        <span class="count muted">({{ product.ratingCount }})</span>
      </div>

      <div class="price-row">
        <strong class="price">{{ formatMoney(product.salePrice || product.listPrice) }}</strong>
        <span
          v-if="strikedPrice"
          class="list"
        >{{ formatMoney(strikedPrice) }}</span>
        <span v-if="product.uomName" class="uom muted">/ {{ product.uomName }}</span>
      </div>

      <button
        class="button primary add"
        type="button"
        @click="$emit('add', product)"
      >
        {{ t("common.addToCart") }}
      </button>
    </div>
  </article>
</template>

<script setup>
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";

import { formatMoney } from "../../utils/format";

const { t } = useI18n();

const props = defineProps({
  product: { type: Object, required: true },
  inWishlist: { type: Boolean, default: false }
});

defineEmits(["add", "wishlist", "compare"]);

const ribbonLabel = computed(() => props.product.ribbon?.name || "");
const ribbonStyle = computed(() => {
  const r = props.product.ribbon;
  if (!r) return {};
  return {
    background: r.bg_color || "#0d8066",
    color: r.text_color || "#fff"
  };
});

const brand = computed(() => {
  const t = props.product.tags?.find?.((x) => /brand/i.test(x.name)) || null;
  return t?.name?.replace(/brand[:\s]*/i, "") || "";
});

const strikedPrice = computed(() => {
  if (props.product.compareListPrice && props.product.compareListPrice > props.product.salePrice) {
    return props.product.compareListPrice;
  }
  if (props.product.hasDiscountedPrice && props.product.listPrice > props.product.salePrice) {
    return props.product.listPrice;
  }
  return null;
});

const discountPercent = computed(() => {
  const original = strikedPrice.value;
  const now = props.product.salePrice || props.product.listPrice;
  if (!original || !now || original <= now) return null;
  return Math.round(((original - now) / original) * 100);
});

const starPct = computed(() => Math.max(0, Math.min(5, props.product.ratingAvg)) * 20);
</script>

<style scoped>
.product {
  overflow: hidden;
  display: grid;
  grid-template-rows: 200px 1fr;
  position: relative;
  transition: transform 0.18s, box-shadow 0.18s;
}

.product:hover {
  transform: translateY(-3px);
  box-shadow: 0 24px 38px rgba(16, 35, 28, 0.12);
}

.image-wrap {
  position: relative;
  background: #fff;
  display: grid;
  place-items: center;
  overflow: hidden;
}

:global(html.dark) .image-wrap {
  background: rgba(255, 255, 255, 0.04);
}

img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 0.6rem;
  transition: transform 0.3s;
}

.product:hover img {
  transform: scale(1.05);
}

.placeholder {
  color: var(--muted);
  font-size: 0.9rem;
}

.ribbon {
  position: absolute;
  top: 0.6rem;
  left: 0.6rem;
  background: var(--accent);
  color: #fff;
  padding: 0.22rem 0.55rem;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.discount {
  position: absolute;
  top: 0.6rem;
  right: 0.6rem;
  background: var(--danger);
  color: #fff;
  padding: 0.22rem 0.5rem;
  border-radius: 4px;
  font-size: 0.78rem;
  font-weight: 700;
}

.wishlist {
  position: absolute;
  bottom: 0.55rem;
  right: 0.55rem;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid var(--line);
  background: #fff;
  font-size: 1.1rem;
  cursor: pointer;
  color: var(--muted);
  display: grid;
  place-items: center;
  transition: color 0.15s, transform 0.15s;
}

.wishlist:hover {
  color: var(--danger);
  transform: scale(1.08);
}

.wishlist.active {
  color: var(--danger);
}

.body {
  padding: 0.85rem 0.9rem 0.95rem;
  display: grid;
  gap: 0.45rem;
}

.brand {
  margin: 0;
  font-size: 0.74rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 600;
}

.name {
  font-weight: 600;
  font-size: 0.93rem;
  line-height: 1.32;
  color: var(--ink);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 2.4em;
}

.name:hover {
  color: var(--accent);
}

.rating {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.82rem;
}

.stars {
  --pct: 0%;
  font-size: 0.95rem;
  letter-spacing: 0.05em;
  background: linear-gradient(90deg, #f5a623 var(--pct), #d8d3c8 var(--pct));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  line-height: 1;
}

.count {
  font-size: 0.78rem;
}

.price-row {
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.price {
  font-size: 1.05rem;
  color: var(--danger);
}

.list {
  font-size: 0.82rem;
  color: var(--muted);
  text-decoration: line-through;
}

.uom {
  font-size: 0.78rem;
}

.add {
  padding: 0.55rem;
  font-size: 0.86rem;
  margin-top: 0.2rem;
}
</style>
