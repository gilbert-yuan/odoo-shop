<template>
  <aside class="card panel">
    <h3>Refine</h3>

    <label>
      Search
      <input v-model="local.search" class="input" type="search" placeholder="Product name or SKU" />
    </label>

    <label>
      Category
      <select v-model="local.categoryId" class="select">
        <option value="">All categories</option>
        <option v-for="category in categories" :key="category.id" :value="String(category.id)">
          {{ category.name }}
        </option>
      </select>
    </label>

    <div class="price-grid">
      <label>
        Min
        <input v-model="local.minPrice" class="input" type="number" min="0" placeholder="0" />
      </label>
      <label>
        Max
        <input v-model="local.maxPrice" class="input" type="number" min="0" placeholder="9999" />
      </label>
    </div>

    <label>
      Sort
      <select v-model="local.order" class="select">
        <option value="id desc">Newest</option>
        <option value="name asc">Name A-Z</option>
        <option value="name desc">Name Z-A</option>
        <option value="list_price asc">Price Low to High</option>
        <option value="list_price desc">Price High to Low</option>
      </select>
    </label>

    <button class="button primary" type="button" @click="apply">Apply filters</button>
  </aside>
</template>

<script setup>
import { reactive, watch } from "vue";

const props = defineProps({
  categories: {
    type: Array,
    default: () => []
  },
  filters: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(["apply"]);

const local = reactive({
  search: "",
  categoryId: "",
  minPrice: "",
  maxPrice: "",
  order: "id desc"
});

watch(
  () => props.filters,
  (next) => {
    local.search = next.search || "";
    local.categoryId = next.categoryId || "";
    local.minPrice = next.minPrice || "";
    local.maxPrice = next.maxPrice || "";
    local.order = next.order || "id desc";
  },
  { immediate: true, deep: true }
);

function apply() {
  emit("apply", {
    search: local.search.trim(),
    categoryId: local.categoryId,
    minPrice: local.minPrice,
    maxPrice: local.maxPrice,
    order: local.order
  });
}
</script>

<style scoped>
.panel {
  padding: 1rem;
  display: grid;
  gap: 0.8rem;
  position: sticky;
  top: 90px;
}

h3 {
  margin: 0;
}

label {
  display: grid;
  gap: 0.3rem;
  font-size: 0.92rem;
}

.price-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.6rem;
}
</style>
