import { defineStore } from "pinia";

import { odooApi } from "../services/odooApi";

function submitRedirectForm(html) {
  const wrapper = document.createElement("div");
  wrapper.style.display = "none";
  wrapper.innerHTML = html;
  document.body.appendChild(wrapper);
  const form = wrapper.querySelector("form");
  if (form) {
    form.submit();
    return true;
  }
  document.body.removeChild(wrapper);
  return false;
}

export const useCheckoutStore = defineStore("checkout", {
  state: () => ({
    loading: false,
    error: "",
    order: null,
    currentStep: "address",

    countries: [],
    statesByCountry: {},

    addresses: [],
    currentBillingId: null,
    currentShippingId: null,

    deliveryMethods: [],
    deliveryRates: {},

    providers: [],
    paymentMethods: [],
    tokens: [],
    selectedProviderId: null,
    selectedPaymentMethodId: null,
    selectedTokenId: null,

    paymentResult: null
  }),

  getters: {
    hasBilling(state) {
      return Boolean(state.order?.billing_address?.id);
    },
    hasShipping(state) {
      return Boolean(state.order?.shipping_address?.id);
    },
    hasDelivery(state) {
      return Boolean(state.order?.carrier?.id);
    },
    canCheckout(state) {
      return Boolean(state.order?.lines?.length);
    },
    statesForBilling(state) {
      const cid = state.order?.billing_address?.country_id;
      return cid ? state.statesByCountry[cid] || [] : [];
    }
  },

  actions: {
    async refreshOrder() {
      this.loading = true;
      this.error = "";
      try {
        this.order = await odooApi.getCurrentOrder();
      } catch (error) {
        this.error = error.message || "Failed to load order.";
      } finally {
        this.loading = false;
      }
    },

    async loadCountries() {
      if (this.countries.length) {
        return;
      }
      try {
        this.countries = await odooApi.getCountries();
      } catch (error) {
        this.error = error.message || "Failed to load countries.";
      }
    },

    async loadStates(countryId) {
      const key = Number(countryId);
      if (!key) {
        return [];
      }
      if (this.statesByCountry[key]) {
        return this.statesByCountry[key];
      }
      try {
        const items = await odooApi.getStates(key);
        this.statesByCountry = { ...this.statesByCountry, [key]: items };
        return items;
      } catch (error) {
        this.error = error.message || "Failed to load states.";
        return [];
      }
    },

    async loadAddresses() {
      try {
        const result = await odooApi.getAddresses("all");
        this.addresses = result.items || [];
        this.currentBillingId = result.currentBillingId;
        this.currentShippingId = result.currentShippingId;
      } catch (error) {
        if (error.status === 403 || error.status === 401) {
          this.addresses = [];
          return;
        }
        this.error = error.message || "Failed to load addresses.";
      }
    },

    async saveAddress({ partnerId = null, addressType = "billing", form = {}, useOnOrder = true }) {
      this.loading = true;
      this.error = "";
      try {
        const result = await odooApi.saveAddress({ partnerId, addressType, form, useOnOrder });
        if (result.order) {
          this.order = result.order;
        }
        await this.loadAddresses();
        return result;
      } catch (error) {
        this.error = error.message || "Failed to save address.";
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async deleteAddress(partnerId) {
      this.loading = true;
      this.error = "";
      try {
        await odooApi.deleteAddress(partnerId);
        await this.loadAddresses();
      } catch (error) {
        this.error = error.message || "Failed to delete address.";
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async useAddress(partnerId, addressType = "billing") {
      this.loading = true;
      this.error = "";
      try {
        const result = await odooApi.useAddressOnOrder(partnerId, addressType);
        if (result.order) {
          this.order = result.order;
        }
        await this.loadAddresses();
      } catch (error) {
        this.error = error.message || "Failed to apply address.";
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async setDefaultAddress(partnerId, addressType = "billing") {
      try {
        await odooApi.setDefaultAddress(partnerId, addressType);
        await this.loadAddresses();
      } catch (error) {
        this.error = error.message || "Failed to set default.";
        throw error;
      }
    },

    async loadDeliveryMethods() {
      try {
        const result = await odooApi.getDeliveryMethods();
        this.deliveryMethods = result.items;
        if (result.selectedCarrierId && !this.order?.carrier?.id) {
          await this.refreshOrder();
        }
      } catch (error) {
        this.error = error.message || "Failed to load delivery methods.";
      }
    },

    async loadDeliveryRate(carrierId) {
      try {
        const result = await odooApi.getDeliveryRate(carrierId);
        this.deliveryRates = { ...this.deliveryRates, [carrierId]: result };
        return result;
      } catch (error) {
        const fallback = { success: false, error_message: error.message };
        this.deliveryRates = { ...this.deliveryRates, [carrierId]: fallback };
        return fallback;
      }
    },

    async setDeliveryMethod(carrierId) {
      this.loading = true;
      this.error = "";
      try {
        const order = await odooApi.setDeliveryMethod(carrierId);
        if (order) {
          this.order = order;
        } else {
          await this.refreshOrder();
        }
      } catch (error) {
        this.error = error.message || "Failed to set delivery method.";
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async applyCoupon(code) {
      this.loading = true;
      this.error = "";
      try {
        const result = await odooApi.applyCoupon(code);
        if (result.order) {
          this.order = result.order;
        }
        return result;
      } catch (error) {
        this.error = error.message || "Coupon application failed.";
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async confirm() {
      this.loading = true;
      this.error = "";
      try {
        return await odooApi.confirmOrder();
      } catch (error) {
        this.error = error.message || "Cannot confirm order.";
        if (error.payload?.step) {
          this.currentStep = error.payload.step;
        }
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async loadProviders() {
      try {
        const result = await odooApi.getPaymentProviders();
        this.providers = result.providers || [];
        this.paymentMethods = result.payment_methods || [];
        this.tokens = result.tokens || [];
        if (!this.selectedProviderId && this.providers.length) {
          this.selectedProviderId = this.providers[0].id;
        }
      } catch (error) {
        this.error = error.message || "Failed to load payment providers.";
      }
    },

    async payNow({ providerId = null, paymentMethodId = null, tokenId = null } = {}) {
      const provider = providerId || this.selectedProviderId;
      const method = paymentMethodId || this.selectedPaymentMethodId;
      const token = tokenId || this.selectedTokenId;
      if (!this.order?.id || !this.order?.access_token) {
        this.error = "Order not ready for payment.";
        return;
      }
      if (!provider) {
        this.error = "Pick a payment provider first.";
        return;
      }
      this.loading = true;
      this.error = "";
      try {
        const result = await odooApi.createPaymentTransaction({
          orderId: this.order.id,
          accessToken: this.order.access_token,
          providerId: provider,
          paymentMethodId: method,
          tokenId: token,
          flow: token ? "token" : "redirect",
          landingRoute: "/checkout/done"
        });
        this.paymentResult = result;

        if (result.redirect_url) {
          window.location.assign(result.redirect_url);
          return;
        }
        if (result.redirect_form_html) {
          if (submitRedirectForm(result.redirect_form_html)) {
            return;
          }
        }
        const done = `/checkout/done/${this.order.id}?access_token=${encodeURIComponent(this.order.access_token)}`;
        window.location.assign(done);
      } catch (error) {
        this.error = error.message || "Payment failed.";
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async pollStatus(orderId, accessToken) {
      return odooApi.getPaymentStatus(orderId, accessToken);
    },

    setStep(step) {
      this.currentStep = step;
    },

    syncStepFromOrder() {
      if (!this.hasBilling || !this.hasShipping) {
        this.currentStep = "address";
      } else if (!this.hasDelivery && this.deliveryMethods.length) {
        this.currentStep = "delivery";
      } else {
        this.currentStep = "payment";
      }
    }
  }
});
