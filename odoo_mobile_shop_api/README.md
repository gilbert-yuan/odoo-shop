# Odoo Mobile Shop API Module

This module provides JSON endpoints for the Vue storefront (`mysql/shop-web`) so frontend clients can fetch ecommerce data without relying on brittle HTML parsing.

## Module path

`mysql/odoo_mobile_shop_api`

## Main API prefix

`/api/mobile/shop`

## Key endpoints

- `POST /api/mobile/shop/session`
- `POST /api/mobile/shop/auth/login`
- `POST /api/mobile/shop/auth/logout`
- `POST /api/mobile/shop/categories`
- `POST /api/mobile/shop/products`
- `POST /api/mobile/shop/products/<id>`
- `POST /api/mobile/shop/cart`
- `POST /api/mobile/shop/cart/quantity`
- `POST /api/mobile/shop/cart/update`
- `POST /api/mobile/shop/cart/clear`
- `POST /api/mobile/shop/delivery/methods`
- `POST /api/mobile/shop/delivery/set`
- `POST /api/mobile/shop/coupon/apply`
- `POST /api/mobile/shop/wishlist/add`
- `POST /api/mobile/shop/wishlist/ids`
- `POST /api/mobile/shop/wishlist/remove`
- `POST /api/mobile/shop/compare/data`
- `POST /api/mobile/shop/stock/notify`
- `POST /api/mobile/shop/orders` (auth user)
- `POST /api/mobile/shop/orders/<order_id>/lines` (auth user)

## Install in Odoo 18

1. Add this repo path to Odoo addons path, e.g. include:
   - `D:\myerp\odoo_graph\mysql`
2. Restart Odoo service.
3. Apps -> Update Apps List.
4. Install module: **Mobile Shop API for Odoo Storefront**.

## Frontend integration

`mysql/shop-web/src/services/odooApi.js` already uses these mobile APIs by default.
