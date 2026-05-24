function pickNumber(input, fallback = 0) {
  const num = Number(input);
  return Number.isFinite(num) ? num : fallback;
}

export function normalizeProduct(item) {
  return {
    id: pickNumber(item.id),
    name: item.name || item.display_name || "Unnamed product",
    displayName: item.display_name || item.name || "Unnamed product",
    description: item.website_description || item.description_sale || "",
    shortDescription: item.description_sale || "",
    listPrice: pickNumber(item.list_price),
    salePrice:
      pickNumber(item.website_price, NaN) || pickNumber(item.price, NaN) || pickNumber(item.list_price),
    imageUrl: item.image_512
      ? `data:image/png;base64,${item.image_512}`
      : item.image_256
        ? `data:image/png;base64,${item.image_256}`
        : item.image_128
          ? `data:image/png;base64,${item.image_128}`
          : "",
    canBeSold: item.sale_ok !== false,
    websitePublished: item.is_published !== false
  };
}

export function normalizeCategory(item) {
  return {
    id: pickNumber(item.id),
    name: item.name || "Category",
    parentId: item.parent_id?.[0] || null
  };
}

export function normalizeCartLine(line) {
  return {
    id: pickNumber(line.id),
    productId: pickNumber(line.product_id?.[0] || line.product_id),
    name: line.name || line.product_id?.[1] || "Product",
    quantity: pickNumber(line.product_uom_qty, 1),
    unitPrice: pickNumber(line.price_unit),
    subtotal: pickNumber(line.price_subtotal),
    total: pickNumber(line.price_total)
  };
}

export function normalizeOrder(order) {
  return {
    id: pickNumber(order.id),
    name: order.name || `SO${order.id}`,
    dateOrder: order.date_order || "",
    state: order.state || "",
    amountTotal: pickNumber(order.amount_total),
    currencyId: order.currency_id?.[0] || null,
    invoiceStatus: order.invoice_status || ""
  };
}
