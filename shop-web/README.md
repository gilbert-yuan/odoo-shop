# Odoo 18 Vue Storefront

Modern Vue 3 storefront for Odoo 18 ecommerce APIs, with a UI style aligned to global ecommerce design patterns.

## Features implemented

- Product catalog, search, filters, sorting
- Product detail page + variant combination request
- Cart add/update/remove/clear (`/shop/cart/update_json`)
- Checkout flow skeleton:
  - billing/delivery address submit (`/shop/address/submit`)
  - delivery method fetch/set (`/shop/delivery_methods`, `/shop/set_delivery_method`)
  - coupon apply (`/coupon/<code>`)
  - payment transaction creation (`/shop/payment/transaction/<order_id>`)
- Account login/logout (`/web/session/authenticate`, `/web/session/destroy`)
- Orders list and order lines
- Wishlist (`/shop/wishlist/*`)
- Compare (`/shop/get_product_data`)
- Stock notifications (`/shop/add/stock_notification`)
- Recently viewed (`/shop/products/recently_viewed_update`)

## Tech stack

- Vue 3 + Vite
- Vue Router
- Pinia

## Run

1. Install dependencies

```bash
npm install
```

If your system has no global `npm`, install Node.js LTS first, then run the command above in this folder.

2. Create env file

```bash
cp .env.example .env
```

3. Edit `.env`

```env
VITE_ODOO_BASE_URL=http://127.0.0.1:8069
VITE_ODOO_DB=odoo18
VITE_ODOO_USE_PROXY=true
```

4. Start dev server

```bash
npm run dev
```

By default, Vite runs on `http://localhost:4173`.

## Notes for production hardening

- CSRF handling for form-style routes (`/shop/address/submit`) should be aligned with your Odoo website auth setup.
- Payment flow currently builds transaction payload and returns processor values; full hosted-fields UX per provider should be completed per your payment modules.
- Some website routes return rendered HTML snippets; replace with API-centric endpoints if you prefer pure JSON frontend contracts.
