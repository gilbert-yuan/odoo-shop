<template>
  <section class="carousel">
    <header class="row">
      <h2 class="title">
        <span v-if="emoji" class="emoji">{{ emoji }}</span>
        {{ title }}
      </h2>
      <div class="ctrls">
        <RouterLink v-if="seeAllTo" :to="seeAllTo" class="see-all">See all →</RouterLink>
        <button class="nav" type="button" :disabled="!canPrev" aria-label="Previous" @click="scroll(-1)">‹</button>
        <button class="nav" type="button" :disabled="!canNext" aria-label="Next" @click="scroll(1)">›</button>
      </div>
    </header>

    <div ref="trackRef" class="track" @scroll.passive="onScroll">
      <template v-if="loading">
        <SkeletonCard v-for="n in 4" :key="`s${n}`" class="item" />
      </template>
      <template v-else>
        <ProductCard
          v-for="product in products"
          :key="product.id"
          :product="product"
          :in-wishlist="wishlistIds.includes(product.id)"
          class="item"
          @add="$emit('add', product)"
          @wishlist="$emit('wishlist', product)"
        />
      </template>
    </div>
  </section>
</template>

<script setup>
import { computed, nextTick, onMounted, ref, watch } from "vue";
import { RouterLink } from "vue-router";

import ProductCard from "./ProductCard.vue";
import SkeletonCard from "./SkeletonCard.vue";

const props = defineProps({
  title: { type: String, required: true },
  emoji: { type: String, default: "" },
  products: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  seeAllTo: { type: String, default: "" },
  wishlistIds: { type: Array, default: () => [] }
});

defineEmits(["add", "wishlist"]);

const trackRef = ref(null);
const canPrev = ref(false);
const canNext = ref(true);

function update() {
  const el = trackRef.value;
  if (!el) return;
  canPrev.value = el.scrollLeft > 4;
  canNext.value = el.scrollLeft + el.clientWidth < el.scrollWidth - 4;
}

function onScroll() {
  update();
}

function scroll(dir) {
  const el = trackRef.value;
  if (!el) return;
  el.scrollBy({ left: dir * el.clientWidth * 0.85, behavior: "smooth" });
}

onMounted(async () => {
  await nextTick();
  update();
});

watch(() => props.products.length, async () => {
  await nextTick();
  update();
});
</script>

<style scoped>
.carousel {
  display: grid;
  gap: 0.7rem;
}

.row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.title {
  margin: 0;
  font-size: clamp(1.05rem, 1.6vw, 1.35rem);
  letter-spacing: -0.01em;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.emoji {
  font-size: 1.2em;
}

.ctrls {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.see-all {
  font-size: 0.88rem;
  color: var(--accent);
  font-weight: 600;
  margin-right: 0.4rem;
}

.see-all:hover {
  text-decoration: underline;
}

.nav {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: 1px solid var(--line);
  background: var(--panel);
  cursor: pointer;
  font-size: 1.2rem;
  display: grid;
  place-items: center;
  color: var(--ink);
  transition: border-color 0.15s, background 0.15s;
}

.nav:hover:not(:disabled) {
  border-color: var(--accent);
  color: var(--accent);
}

.nav:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.track {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: minmax(220px, 1fr);
  gap: 0.85rem;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scrollbar-width: thin;
  padding-bottom: 0.4rem;
}

.track::-webkit-scrollbar {
  height: 6px;
}

.track::-webkit-scrollbar-thumb {
  background: var(--line);
  border-radius: 999px;
}

.item {
  scroll-snap-align: start;
  min-width: 0;
}

@media (min-width: 720px) {
  .track {
    grid-auto-columns: minmax(230px, calc((100% - 2.55rem) / 4));
  }
}

@media (max-width: 720px) {
  .track {
    grid-auto-columns: minmax(180px, 70vw);
  }
  .nav {
    display: none;
  }
}
</style>
