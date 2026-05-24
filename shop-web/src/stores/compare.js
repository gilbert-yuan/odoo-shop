import { defineStore } from "pinia";

import { odooApi } from "../services/odooApi";

const STORAGE_KEY = "odoo_storefront_compare_ids";

export const useCompareStore = defineStore("compare", {
  state: () => ({
    ids: [],
    dataMap: {},
    loading: false
  }),

  getters: {
    entries(state) {
      return state.ids
        .map((id) => state.dataMap[id])
        .filter(Boolean);
    }
  },

  actions: {
    async restoreFromStorage() {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        try {
          const parsed = JSON.parse(raw);
          if (Array.isArray(parsed)) {
            this.ids = parsed.map(Number).slice(0, 4);
          }
        } catch {
          this.ids = [];
        }
      }
      if (this.ids.length) {
        await this.refreshData();
      }
    },

    persist() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.ids));
    },

    async refreshData() {
      if (!this.ids.length) {
        this.dataMap = {};
        return;
      }
      this.loading = true;
      try {
        const payload = await odooApi.getCompareProductData(this.ids);
        const next = {};
        this.ids.forEach((id) => {
          if (payload[id]?.product) {
            next[id] = payload[id].product;
          }
        });
        this.dataMap = next;
      } finally {
        this.loading = false;
      }
    },

    async toggle(productId) {
      const id = Number(productId);
      if (this.ids.includes(id)) {
        this.ids = this.ids.filter((x) => x !== id);
      } else {
        this.ids = [...this.ids, id].slice(-4);
      }
      this.persist();
      await this.refreshData();
    },

    async clear() {
      this.ids = [];
      this.persist();
      this.dataMap = {};
    }
  }
});
