function extractNumber(text, fallback = 0) {
  const num = Number(text);
  return Number.isFinite(num) ? num : fallback;
}

function stripHtml(text) {
  return String(text || "").replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
}

export function parseCartPageHtml(html) {
  try {
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, "text/html");

    const orderEl = doc.querySelector(".my_cart_quantity");
    const orderId = orderEl?.getAttribute("data-order-id")
      ? Number(orderEl.getAttribute("data-order-id"))
      : null;

    const rows = Array.from(doc.querySelectorAll("#cart_products .o_cart_product"));
    const lines = rows
      .map((row) => {
        const productId = Number(row.getAttribute("data-product-id") || 0);
        const qtyInput = row.querySelector(".js_quantity[data-line-id]");
        if (!qtyInput) {
          return null;
        }
        const lineId = Number(qtyInput.getAttribute("data-line-id") || 0);
        const qty = extractNumber(qtyInput.getAttribute("value"), 1);
        const name = row.querySelector("h6")?.textContent || "Product";
        const priceText = row.querySelector("[name='website_sale_cart_line_price']")?.textContent || "";
        return {
          id: lineId,
          productId,
          name: stripHtml(name),
          quantity: qty,
          unitPrice: 0,
          subtotal: 0,
          total: 0,
          displayPrice: stripHtml(priceText)
        };
      })
      .filter(Boolean);

    return { orderId, lines };
  } catch {
    return { orderId: null, lines: [] };
  }
}
