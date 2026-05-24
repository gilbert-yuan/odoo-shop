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
    salePrice: Number(item.list_price || 0),
    imageUrl: item.image_url || "",
    canBeSold: item.sale_ok !== false,
    websitePublished: item.is_published !== false
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
    throw new Error(result?.message || "Mobile shop API call failed.");
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
      const data = await callApi(`/products/${Number(id)}`);
      if (!data.item) {
        return null;
      }
      return normalizeProduct(data.item);
    } catch {
      return null;
    }
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

  async getCartOrderFromPage() {
    return { orderId: null, lines: [] };
  },

  async getCartLines(orderId) {
    if (!orderId) {
      return [];
    }
    const data = await callApi("/cart");
    return (data.lines || []).map(normalizeCartLine);
  },

  async addToCart({
    productId,
    addQty = 1,
    setQty = null
  }) {
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
    addQty = 1,
    parentCombination = []
  }) {
    return rpc("/website_sale/get_combination_info", {
      product_template_id: Number(productTemplateId),
      product_id: productId ? Number(productId) : false,
      combination: combination.map(Number),
      add_qty: addQty,
      parent_combination: parentCombination.map(Number)
    });
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

  async getCheckoutOrder() {
    const data = await callApi("/cart");
    return {
      ...(data.order || {}),
      lines: (data.lines || []).map(normalizeCartLine)
    };
  },

  async submitAddress({
    partnerId = null,
    addressType = "billing",
    useDeliveryAsBilling = false,
    form = {}
  }) {
    const params = new URLSearchParams();
    if (partnerId) {
      params.set("partner_id", String(partnerId));
    }
    params.set("address_type", addressType);
    params.set("use_delivery_as_billing", useDeliveryAsBilling ? "true" : "false");
    Object.entries(form).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.set(key, String(value));
      }
    });

    const response = await fetch("/shop/address/submit", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      credentials: "include",
      body: params.toString()
    });

    if (!response.ok) {
      throw new Error(`Address submit failed: HTTP ${response.status}`);
    }
    const text = await response.text();
    try {
      return JSON.parse(text);
    } catch {
      return { redirectUrl: "/checkout" };
    }
  },

  async getCountryInfo(countryId, addressType = "billing") {
    return rpc(`/shop/country_info/${Number(countryId)}`, {
      address_type: addressType
    });
  },

  async getDeliveryMethods() {
    const data = await callApi("/delivery/methods");
    return {
      rawHtml: "",
      items: data.items || [],
      selectedCarrierId: data.selected_carrier_id || null
    };
  },

  async setDeliveryMethod(dmId) {
    return callApi("/delivery/set", {
      carrier_id: Number(dmId)
    });
  },

  async getDeliveryRate(dmId) {
    return rpc("/shop/get_delivery_rate", {
      dm_id: Number(dmId)
    });
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

  async applyCoupon(code) {
    return callApi("/coupon/apply", { code });
  },

  async claimReward({ rewardId, code = null, redirect = "/shop/cart", productId = null }) {
    const params = new URLSearchParams();
    params.set("reward_id", String(rewardId));
    params.set("r", redirect);
    if (code) {
      params.set("code", code);
    }
    if (productId) {
      params.set("product_id", String(productId));
    }
    const response = await fetch(`/shop/claimreward?${params.toString()}`, {
      method: "GET",
      credentials: "include"
    });
    return {
      ok: response.ok,
      redirected: response.redirected,
      url: response.url
    };
  },

  async preparePaymentTransaction({ orderId, accessToken, providerCode, flow = "redirect", amount = null }) {
    return rpc(`/shop/payment/transaction/${Number(orderId)}`, {
      access_token: accessToken,
      provider_code: providerCode,
      flow,
      amount
    });
  },

  async getOrders(limit = 20) {
    const data = await callApi("/orders", { limit });
    return (data.items || []).map(normalizeOrder);
  },

  async getOrderLines(orderId) {
    const data = await callApi(`/orders/${Number(orderId)}/lines`);
    return (data.lines || []).map(normalizeCartLine);
  },

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
