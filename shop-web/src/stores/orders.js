import { defineStore } from "pinia";

import { odooApi } from "../services/odooApi";

export const useOrdersStore = defineStore("orders", {
  state: () => ({
    loading: false,
    orders: [],
    selectedOrderLines: [],
    selectedOrderId: null,
    error: ""
  }),

  actions: {
    async refresh() {
      this.loading = true;
      this.error = "";
      try {
        this.orders = await odooApi.getOrders();
      } catch (error) {
        this.error = error.message || "Failed to load orders.";
      } finally {
        this.loading = false;
      }
    },

    async selectOrder(orderId) {
      this.loading = true;
      this.error = "";
      this.selectedOrderId = Number(orderId);
      try {
        this.selectedOrderLines = await odooApi.getOrderLines(orderId);
      } catch (error) {
        this.error = error.message || "Failed to load order lines.";
      } finally {
        this.loading = false;
      }
    }
  }
});
