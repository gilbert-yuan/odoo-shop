import { defineStore } from "pinia";

import { odooApi } from "../services/odooApi";

export const useCheckoutStore = defineStore("checkout", {
  state: () => ({
    loading: false,
    order: null,
    deliveryHtml: "",
    deliverySummary: null,
    lastPaymentValues: null,
    error: "",
    couponCode: ""
  }),

  actions: {
    async refresh() {
      this.loading = true;
      this.error = "";
      try {
        this.order = await odooApi.getCheckoutOrder();
      } catch (error) {
        this.error = error.message || "Failed to load checkout order.";
      } finally {
        this.loading = false;
      }
    },

    async submitAddress(payload) {
      this.loading = true;
      this.error = "";
      try {
        const result = await odooApi.submitAddress(payload);
        await this.refresh();
        return result;
      } catch (error) {
        this.error = error.message || "Failed to submit address.";
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async loadDeliveryMethods() {
      this.loading = true;
      this.error = "";
      try {
        const result = await odooApi.getDeliveryMethods();
        this.deliveryHtml = result.rawHtml || "";
        this.deliverySummary = result;
      } catch (error) {
        this.error = error.message || "Failed to load delivery methods.";
      } finally {
        this.loading = false;
      }
    },

    async setDeliveryMethod(dmId) {
      this.loading = true;
      this.error = "";
      try {
        this.deliverySummary = await odooApi.setDeliveryMethod(dmId);
        await this.refresh();
      } catch (error) {
        this.error = error.message || "Failed to set delivery method.";
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async getDeliveryRate(dmId) {
      return odooApi.getDeliveryRate(dmId);
    },

    async applyCoupon(code) {
      this.loading = true;
      this.error = "";
      try {
        this.couponCode = code;
        const result = await odooApi.applyCoupon(code);
        await this.refresh();
        return result;
      } catch (error) {
        this.error = error.message || "Coupon application failed.";
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async createPaymentTransaction({ providerCode, flow = "redirect", amount = null }) {
      if (!this.order?.id || !this.order?.access_token) {
        throw new Error("Missing order access token. Please login and continue checkout on Odoo session first.");
      }
      this.loading = true;
      this.error = "";
      try {
        this.lastPaymentValues = await odooApi.preparePaymentTransaction({
          orderId: this.order.id,
          accessToken: this.order.access_token,
          providerCode,
          flow,
          amount
        });
        return this.lastPaymentValues;
      } catch (error) {
        this.error = error.message || "Failed to create payment transaction.";
        throw error;
      } finally {
        this.loading = false;
      }
    }
  }
});
