import { defineStore } from "pinia";

import { odooApi } from "../services/odooApi";

export const useCartStore = defineStore("cart", {
  state: () => ({
    loading: false,
    order: null,
    lines: [],
    quantity: 0,
    error: ""
  }),

  getters: {
    subtotal(state) {
      return state.lines.reduce((sum, line) => sum + line.subtotal, 0);
    },
    total(state) {
      if (state.order?.amount_total !== undefined) {
        return Number(state.order.amount_total || 0);
      }
      return state.lines.reduce((sum, line) => sum + line.total, 0);
    }
  },

  actions: {
    async refresh() {
      this.loading = true;
      this.error = "";
      try {
        this.quantity = await odooApi.getCartQuantity();
        this.order = await odooApi.getCartOrder();
        if (this.order) {
          this.lines = await odooApi.getCartLines(this.order.id);
        } else {
          const fallback = await odooApi.getCartOrderFromPage();
          this.order = fallback.orderId
            ? { id: fallback.orderId, amount_total: 0, amount_tax: 0, amount_untaxed: 0 }
            : null;
          this.lines = fallback.lines;
        }
      } catch (error) {
        this.error = error.message || "Unable to load cart.";
      } finally {
        this.loading = false;
      }
    },

    async addToCart(productId, qty = 1) {
      this.loading = true;
      this.error = "";
      try {
        await odooApi.addToCart({
          productId,
          addQty: qty
        });
        await this.refresh();
      } catch (error) {
        this.error = error.message || "Unable to add item to cart.";
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async setLineQty(line, qty) {
      this.loading = true;
      this.error = "";
      try {
        await odooApi.updateCartLine({
          productId: line.productId,
          lineId: line.id,
          setQty: qty
        });
        await this.refresh();
      } catch (error) {
        this.error = error.message || "Unable to update quantity.";
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async clear() {
      this.loading = true;
      this.error = "";
      try {
        await odooApi.clearCart();
        await this.refresh();
      } catch (error) {
        this.error = error.message || "Unable to clear cart.";
        throw error;
      } finally {
        this.loading = false;
      }
    }
  }
});
