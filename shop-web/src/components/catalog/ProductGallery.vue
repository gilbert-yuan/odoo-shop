<template>
  <section class="gallery">
    <div class="main">
      <img v-if="currentImage" :src="currentImage" :alt="alt" @error="onImageError" />
      <div v-else class="placeholder">No image</div>
    </div>
    <div v-if="images.length > 1" class="thumbs">
      <button
        v-for="(src, idx) in images"
        :key="src + idx"
        type="button"
        class="thumb"
        :class="{ active: activeIndex === idx }"
        @click="activeIndex = idx"
      >
        <img :src="src" :alt="`${alt} ${idx + 1}`" />
      </button>
    </div>
  </section>
</template>

<script setup>
import { computed, ref, watch } from "vue";

const props = defineProps({
  images: { type: Array, default: () => [] },
  alt: { type: String, default: "Product image" },
  override: { type: String, default: "" }
});

const activeIndex = ref(0);

watch(
  () => props.images,
  () => {
    activeIndex.value = 0;
  }
);

const currentImage = computed(() => props.override || props.images[activeIndex.value] || "");

function onImageError(event) {
  event.target.style.display = "none";
}
</script>

<style scoped>
.gallery {
  display: grid;
  gap: 0.7rem;
}

.main {
  background: linear-gradient(160deg, #f3f8f5 0%, #fdf4e5 100%);
  border-radius: var(--radius-lg);
  overflow: hidden;
  aspect-ratio: 1 / 1;
  display: grid;
  place-items: center;
}

.main img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.placeholder {
  color: var(--muted);
}

.thumbs {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.thumb {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  border: 1px solid var(--line);
  padding: 0;
  background: #fff;
  cursor: pointer;
  overflow: hidden;
  transition: border-color 0.15s, transform 0.15s;
}

.thumb:hover {
  border-color: var(--accent);
}

.thumb.active {
  border-color: var(--accent);
  outline: 2px solid var(--accent-soft);
}

.thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
