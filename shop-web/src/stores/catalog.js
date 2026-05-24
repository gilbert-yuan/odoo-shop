import { defineStore } from "pinia";

import { odooApi } from "../services/odooApi";

export const useCatalogStore = defineStore("catalog", {
  state: () => ({
    loading: false,
    products: [],
    categories: [],
    filters: {
      search: "",
      categoryId: "",
      minPrice: "",
      maxPrice: "",
      order: "id desc"
    }
  }),

  actions: {
    setSearch(value) {
      this.filters.search = value;
    },

    setCategory(categoryId) {
      this.filters.categoryId = categoryId;
    },

    setPriceRange({ min, max }) {
      this.filters.minPrice = min;
      this.filters.maxPrice = max;
    },

    setOrder(order) {
      this.filters.order = order;
    },

    async loadCategories() {
      this.categories = await odooApi.getCategories();
    },

    async loadProducts(overrides = {}) {
      this.loading = true;
      try {
        const query = {
          ...this.filters,
          ...overrides
        };
        this.products = await odooApi.searchProducts({
          search: query.search,
          categoryId: query.categoryId || null,
          minPrice: query.minPrice || null,
          maxPrice: query.maxPrice || null,
          order: query.order,
          limit: query.limit || 40,
          offset: query.offset || 0
        });
      } finally {
        this.loading = false;
      }
    }
  }
});
