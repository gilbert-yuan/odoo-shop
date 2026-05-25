import { defineStore } from "pinia";

import { odooApi } from "../services/odooApi";

export const useCartStore = defineStore("cart", {
  state: () => ({
    loading: false,
    mutating: false,
    initialized: false,
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
    async refresh({ silent = false } = {}) {
      if (!silent && !this.initialized) {
        this.loading = true;
      }
      this.error = "";
      try {
        const [quantity, order] = await Promise.all([
          odooApi.getCartQuantity(),
          odooApi.getCartOrder()
        ]);
        this.quantity = quantity;
        this.order = order;
        this.lines = order ? await odooApi.getCartLines(order.id) : [];
      } catch (error) {
        this.error = error.message || "Unable to load cart.";
      } finally {
        this.loading = false;
        this.initialized = true;
      }
    },

    async addToCart(productId, qty = 1) {
      this.mutating = true;
      this.error = "";
      try {
        await odooApi.addToCart({ productId, addQty: qty });
        await this.refresh({ silent: true });
      } catch (error) {
        this.error = error.message || "Unable to add item to cart.";
        throw error;
      } finally {
        this.mutating = false;
      }
    },

    async setLineQty(line, qty) {
      this.error = "";
      const previousLines = this.lines.map((l) => ({ ...l }));
      const previousQuantity = this.quantity;
      const previousOrder = this.order ? { ...this.order } : null;

      // optimistic update
      if (qty <= 0) {
        this.lines = this.lines.filter((l) => l.id !== line.id);
      } else {
        this.lines = this.lines.map((l) =>
          l.id === line.id
            ? {
                ...l,
                quantity: qty,
                subtotal: l.unitPrice * qty,
                total: l.unitPrice * qty
              }
            : l
        );
      }
      this.quantity = this.lines.reduce((sum, l) => sum + l.quantity, 0);

      this.mutating = true;
      try {
        await odooApi.updateCartLine({
          productId: line.productId,
          lineId: line.id,
          setQty: qty
        });
        await this.refresh({ silent: true });
      } catch (error) {
        // roll back on failure
        this.lines = previousLines;
        this.quantity = previousQuantity;
        this.order = previousOrder;
        this.error = error.message || "Unable to update quantity.";
        throw error;
      } finally {
        this.mutating = false;
      }
    },

    async clear() {
      this.error = "";
      const previousLines = this.lines;
      const previousQuantity = this.quantity;
      this.lines = [];
      this.quantity = 0;

      this.mutating = true;
      try {
        await odooApi.clearCart();
        await this.refresh({ silent: true });
      } catch (error) {
        this.lines = previousLines;
        this.quantity = previousQuantity;
        this.error = error.message || "Unable to clear cart.";
        throw error;
      } finally {
        this.mutating = false;
      }
    }
  }
});
