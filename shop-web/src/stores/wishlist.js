import { defineStore } from "pinia";

import { odooApi } from "../services/odooApi";

export const useWishlistStore = defineStore("wishlist", {
  state: () => ({
    loading: false,
    ids: [],
    items: []
  }),

  getters: {
    has: (state) => (productId) => state.ids.includes(Number(productId))
  },

  actions: {
    async refresh() {
      this.loading = true;
      try {
        this.ids = await odooApi.getWishlistIds();
        if (!this.ids.length) {
          this.items = [];
          return;
        }
        const products = await Promise.all(this.ids.map((id) => odooApi.getProductById(id)));
        this.items = products.filter(Boolean);
      } finally {
        this.loading = false;
      }
    },

    async add(productId) {
      await odooApi.addToWishlist(productId);
      await this.refresh();
    },

    async toggle(productId) {
      const id = Number(productId);
      if (this.ids.includes(id)) {
        await odooApi.removeWishlist(id);
      } else {
        await odooApi.addToWishlist(id);
      }
      await this.refresh();
    },

    async removeWish(wishId) {
      await odooApi.removeWishlist(wishId);
      await this.refresh();
    }
  }
});
