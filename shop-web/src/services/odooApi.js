import { rpc } from "./odooHttp";

const MOBILE_API_BASE = "/api/mobile/shop";

function normalizeProduct(item) {
  return {
    id: Number(item.id),
    name: item.name || "Unnamed product",
    displayName: item.display_name || item.name || "Unnamed product",
    description: item.website_description || item.description_sale || "",
    shortDescription: item.description_sale || "",
    listPrice: Number(item.list_price || 0),
    salePrice: Number(item.price ?? item.list_price ?? 0),
    hasDiscountedPrice: Boolean(item.has_discounted_price),
    imageUrl: item.image_url || "",
    imageUrls: item.image_urls || (item.image_url ? [item.image_url] : []),
    canBeSold: item.sale_ok !== false,
    websitePublished: item.is_published !== false,
    variants: item.variants || [],
    attributeLines: item.attribute_lines || []
  };
}

function normalizeCategory(item) {
  return {
    id: Number(item.id),
    name: item.name || "Category",
    parentId: item.parent_id || null
  };
}

function normalizeCartLine(line) {
  return {
    id: Number(line.id),
    productId: Number(line.product_tmpl_id || line.product_id || 0),
    name: line.name || "Product",
    quantity: Number(line.quantity || 0),
    unitPrice: Number(line.price_unit || 0),
    subtotal: Number(line.price_subtotal || 0),
    total: Number(line.price_total || 0)
  };
}

function normalizeOrder(order) {
  return {
    id: Number(order.id),
    name: order.name || `SO${order.id}`,
    dateOrder: order.date_order || "",
    state: order.state || "",
    amountTotal: Number(order.amount_total || 0),
    invoiceStatus: order.invoice_status || ""
  };
}

async function callApi(path, payload = {}) {
  const result = await rpc(`${MOBILE_API_BASE}${path}`, payload);
  if (!result?.ok) {
    const err = new Error(result?.message || "Mobile shop API call failed.");
    err.status = result?.status;
    err.payload = result?.data || {};
    throw err;
  }
  return result.data || {};
}

export const odooApi = {
  async authenticate(login, password) {
    return callApi("/auth/login", { login, password });
  },

  async logout() {
    return callApi("/auth/logout");
  },

  async getSessionInfo() {
    try {
      const data = await callApi("/session");
      return {
        uid: data.uid || null,
        name: data.name || null,
        username: data.login || null
      };
    } catch {
      return null;
    }
  },

  async searchProducts({
    search = "",
    categoryId = null,
    minPrice = null,
    maxPrice = null,
    limit = 24,
    offset = 0,
    order = "id desc"
  } = {}) {
    const data = await callApi("/products", {
      search,
      category_id: categoryId || null,
      min_price: minPrice,
      max_price: maxPrice,
      order,
      limit,
      offset
    });
    return (data.items || []).map(normalizeProduct);
  },

  async getProductById(id) {
    try {
      const data = await callApi(`/products/${Number(id)}/full`);
      if (!data.item) {
        return null;
      }
      return normalizeProduct(data.item);
    } catch {
      try {
        const data = await callApi(`/products/${Number(id)}`);
        return data.item ? normalizeProduct(data.item) : null;
      } catch {
        return null;
      }
    }
  },

  async getProductCombination(productTemplateId, { ptavIds = [], addQty = 1 } = {}) {
    const data = await callApi(`/products/${Number(productTemplateId)}/combination`, {
      ptav_ids: ptavIds.map(Number),
      add_qty: addQty
    });
    return data.combination || null;
  },

  async getCategories() {
    const data = await callApi("/categories");
    return (data.items || []).map(normalizeCategory);
  },

  async getCartQuantity() {
    const data = await callApi("/cart/quantity");
    return Number(data.cart_quantity || 0);
  },

  async getCartOrder() {
    try {
      const data = await callApi("/cart");
      return data.order || null;
    } catch {
      return null;
    }
  },

  async getCartLines(orderId) {
    if (!orderId) {
      return [];
    }
    const data = await callApi("/cart");
    return (data.lines || []).map(normalizeCartLine);
  },

  async addToCart({ productId, addQty = 1, setQty = null }) {
    return callApi("/cart/update", {
      product_id: Number(productId),
      add_qty: addQty,
      set_qty: setQty
    });
  },

  async updateCartLine({ productId, lineId, setQty }) {
    return callApi("/cart/update", {
      product_id: Number(productId),
      line_id: Number(lineId),
      set_qty: Number(setQty)
    });
  },

  async clearCart() {
    return callApi("/cart/clear");
  },

  async getCombinationInfo({
    productTemplateId,
    productId = null,
    combination = [],
    addQty = 1
  }) {
    return this.getProductCombination(productTemplateId, {
      ptavIds: combination,
      addQty
    });
  },

  // ---------- account ----------
  async register({ name, login, password, phone = null }) {
    return callApi("/auth/register", { name, login, password, phone });
  },

  async passwordForgot(login) {
    return callApi("/auth/password/forgot", { login });
  },

  async passwordReset({ token, login, newPassword }) {
    return callApi("/auth/password/reset", {
      token,
      login,
      new_password: newPassword
    });
  },

  async changePassword({ currentPassword, newPassword }) {
    return callApi("/auth/password/change", {
      current_password: currentPassword,
      new_password: newPassword
    });
  },

  async getProfile() {
    return callApi("/profile");
  },

  async updateProfile({ name = null, email = null, phone = null, lang = null }) {
    return callApi("/profile/update", { name, email, phone, lang });
  },

  // ---------- meta ----------
  async getLanguages() {
    return callApi("/languages");
  },

  async getSitemapData() {
    return callApi("/sitemap");
  },

  // ---------- contact / wholesale / COA ----------
  async submitContact({ name, email, phone, subject, message }) {
    return callApi("/contact", { name, email, phone, subject, message });
  },

  async submitWholesale({ company, name, email, phone, country, products, volume, message }) {
    return callApi("/wholesale", { company, name, email, phone, country, products, volume, message });
  },

  async lookupCoa(code) {
    const data = await callApi("/coa/lookup", { code });
    return data.items || [];
  },

  async getAutocomplete(term, limit = 8) {
    const data = await callApi("/products", {
      search: term,
      limit,
      offset: 0
    });
    return (data.items || []).map((item) => ({
      _fa: "fa-tag",
      name: item.name,
      detail: item.description_sale || "",
      extra_link: `/product/${item.id}`
    }));
  },

  async addToWishlist(productId) {
    return callApi("/wishlist/add", {
      product_id: Number(productId)
    });
  },

  async getWishlistIds() {
    const data = await callApi("/wishlist/ids");
    return (data.product_template_ids || []).map(Number);
  },

  async removeWishlist(wishId) {
    return callApi("/wishlist/remove", {
      product_template_id: Number(wishId)
    });
  },

  async getCompareProductData(productIds = []) {
    if (!productIds.length) {
      return {};
    }
    const data = await callApi("/compare/data", {
      product_ids: productIds.map(Number)
    });
    const mapped = {};
    for (const item of data.items || []) {
      mapped[item.id] = { product: item };
    }
    return mapped;
  },

  async addStockNotification(email, productId) {
    return callApi("/stock/notify", {
      email,
      product_id: Number(productId)
    });
  },

  // ---------- geography ----------
  async getCountries() {
    const data = await callApi("/countries");
    return data.items || [];
  },

  async getStates(countryId) {
    if (!countryId) {
      return [];
    }
    const data = await callApi(`/countries/${Number(countryId)}/states`);
    return data.items || [];
  },

  // ---------- addresses ----------
  async getAddresses(addressType = "all") {
    const data = await callApi("/addresses", { address_type: addressType });
    return {
      items: data.items || [],
      currentBillingId: data.current_billing_id || null,
      currentShippingId: data.current_shipping_id || null
    };
  },

  async saveAddress({ partnerId = null, addressType = "billing", form = {}, useOnOrder = true }) {
    return callApi("/addresses/save", {
      partner_id: partnerId ? Number(partnerId) : null,
      address_type: addressType,
      form,
      use_on_order: useOnOrder
    });
  },

  async deleteAddress(partnerId) {
    return callApi(`/addresses/${Number(partnerId)}/delete`);
  },

  async useAddressOnOrder(partnerId, addressType = "billing") {
    return callApi(`/addresses/${Number(partnerId)}/use`, {
      address_type: addressType
    });
  },

  async setDefaultAddress(partnerId, addressType = "billing") {
    return callApi(`/addresses/${Number(partnerId)}/default`, {
      address_type: addressType
    });
  },

  // ---------- order ----------
  async getCurrentOrder() {
    const data = await callApi("/order");
    return data.order || null;
  },

  async getOrderDetail(orderId, accessToken = null) {
    const payload = {};
    if (accessToken) {
      payload.access_token = accessToken;
    }
    const data = await callApi(`/order/${Number(orderId)}`, payload);
    return data.order || null;
  },

  async confirmOrder() {
    return callApi("/order/confirm");
  },

  // ---------- delivery ----------
  async getDeliveryMethods() {
    const data = await callApi("/delivery/methods");
    return {
      items: data.items || [],
      selectedCarrierId: data.selected_carrier_id || null
    };
  },

  async setDeliveryMethod(dmId) {
    const data = await callApi("/delivery/set", { carrier_id: Number(dmId) });
    return data.order || null;
  },

  async getDeliveryRate(carrierId) {
    return callApi("/delivery/rate", { carrier_id: Number(carrierId) });
  },

  // ---------- coupon / reward ----------
  async applyCoupon(code) {
    return callApi("/coupon/apply", { code });
  },

  async claimReward({ rewardId = null, code = null, productId = null } = {}) {
    return callApi("/reward/claim", {
      reward_id: rewardId ? Number(rewardId) : null,
      code: code || null,
      product_id: productId ? Number(productId) : null
    });
  },

  // ---------- payment ----------
  async getPaymentProviders(orderId = null, accessToken = null) {
    const payload = {};
    if (orderId) {
      payload.order_id = Number(orderId);
    }
    if (accessToken) {
      payload.access_token = accessToken;
    }
    return callApi("/payment/providers", payload);
  },

  async createPaymentTransaction({
    orderId,
    accessToken,
    providerId,
    paymentMethodId = null,
    tokenId = null,
    flow = "redirect",
    landingRoute = "/checkout/done"
  }) {
    return callApi("/payment/transaction", {
      order_id: Number(orderId),
      access_token: accessToken,
      provider_id: Number(providerId),
      payment_method_id: paymentMethodId ? Number(paymentMethodId) : null,
      token_id: tokenId ? Number(tokenId) : null,
      flow,
      landing_route: landingRoute
    });
  },

  async getPaymentStatus(orderId, accessToken = null) {
    const payload = { order_id: Number(orderId) };
    if (accessToken) {
      payload.access_token = accessToken;
    }
    return callApi("/payment/status", payload);
  },

  // ---------- orders (history) ----------
  async getOrders(limit = 20) {
    const data = await callApi("/orders", { limit });
    return (data.items || []).map(normalizeOrder);
  },

  async getOrderLines(orderId) {
    const data = await callApi(`/orders/${Number(orderId)}/lines`);
    return (data.lines || []).map(normalizeCartLine);
  },

  // ---------- configurator (deferred; still legacy) ----------
  async createProductVariant(productTemplateId, ptavIds) {
    return rpc("/sale/create_product_variant", {
      product_template_id: Number(productTemplateId),
      product_template_attribute_value_ids: JSON.stringify(ptavIds.map(Number))
    });
  },

  async shouldShowConfigurator({ productTemplateId, ptavIds = [], isProductConfigured = false }) {
    return rpc("/website_sale/should_show_product_configurator", {
      product_template_id: Number(productTemplateId),
      ptav_ids: ptavIds.map(Number),
      is_product_configured: Boolean(isProductConfigured)
    });
  },

  async getConfiguratorValues(payload) {
    return rpc("/website_sale/product_configurator/get_values", payload);
  },

  async updateConfiguratorCombination(payload) {
    return rpc("/website_sale/product_configurator/update_combination", payload);
  },

  async getOptionalProducts(payload) {
    return rpc("/website_sale/product_configurator/get_optional_products", payload);
  },

  async updateCartWithConfigurator(mainProduct, optionalProducts = []) {
    return rpc("/website_sale/product_configurator/update_cart", {
      main_product: mainProduct,
      optional_products: optionalProducts
    });
  },

  async getComboData(payload) {
    return rpc("/website_sale/combo_configurator/get_data", payload);
  },

  async getComboPrice(payload) {
    return rpc("/website_sale/combo_configurator/get_price", payload);
  },

  async updateCartWithCombo(payload) {
    return rpc("/website_sale/combo_configurator/update_cart", payload);
  },

  async setClickAndCollectLocation(pickupLocationData) {
    return rpc("/shop/set_click_and_collect_location", {
      pickup_location_data: pickupLocationData
    });
  },

  async setPickupLocation(pickupLocationData) {
    return rpc("/website_sale/set_pickup_location", {
      pickup_location_data: pickupLocationData
    });
  },

  async getPickupLocations({ zipCode = "", productId = null } = {}) {
    return rpc("/website_sale/get_pickup_locations", {
      zip_code: zipCode,
      product_id: productId
    });
  },

  async markRecentlyViewed(productId) {
    return rpc("/shop/products/recently_viewed_update", {
      product_id: Number(productId)
    });
  },

  async removeRecentlyViewed({ productId = null, productTemplateId = null } = {}) {
    return rpc("/shop/products/recently_viewed_delete", {
      product_id: productId ? Number(productId) : undefined,
      product_template_id: productTemplateId ? Number(productTemplateId) : undefined
    });
  }
};
