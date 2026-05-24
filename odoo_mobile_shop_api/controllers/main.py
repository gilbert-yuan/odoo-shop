from __future__ import annotations

from odoo import http
from odoo.http import request


def _ok(data=None, message="ok", status=200):
    return {
        "ok": True,
        "status": status,
        "message": message,
        "data": data or {},
    }


def _err(message="error", status=400, data=None):
    return {
        "ok": False,
        "status": status,
        "message": message,
        "data": data or {},
    }


def _to_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return default


def _to_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def _currency_payload(currency):
    if not currency:
        return None
    return {
        "id": currency.id,
        "name": currency.name,
        "symbol": currency.symbol,
        "position": currency.position,
    }


def _product_payload(product_tmpl):
    image_url = f"/web/image/product.template/{product_tmpl.id}/image_512"
    return {
        "id": product_tmpl.id,
        "name": product_tmpl.name,
        "display_name": product_tmpl.display_name,
        "website_description": product_tmpl.website_description or "",
        "description_sale": product_tmpl.description_sale or "",
        "list_price": product_tmpl.list_price,
        "currency": _currency_payload(product_tmpl.currency_id),
        "image_url": image_url,
        "is_published": bool(product_tmpl.is_published),
        "sale_ok": bool(product_tmpl.sale_ok),
        "public_category_ids": product_tmpl.public_categ_ids.ids,
    }


def _category_payload(category):
    return {
        "id": category.id,
        "name": category.name,
        "parent_id": category.parent_id.id if category.parent_id else None,
        "website_id": category.website_id.id if category.website_id else None,
    }


def _cart_line_payload(line):
    return {
        "id": line.id,
        "product_id": line.product_id.id,
        "product_tmpl_id": line.product_id.product_tmpl_id.id,
        "name": line.name_short or line.name,
        "quantity": line.product_uom_qty,
        "price_unit": line.price_unit,
        "price_subtotal": line.price_subtotal,
        "price_total": line.price_total,
        "is_delivery": bool(line.is_delivery),
    }


def _order_payload(order):
    return {
        "id": order.id,
        "name": order.name,
        "state": order.state,
        "amount_total": order.amount_total,
        "amount_untaxed": order.amount_untaxed,
        "amount_tax": order.amount_tax,
        "amount_delivery": order.amount_delivery,
        "cart_quantity": order.cart_quantity,
        "currency": _currency_payload(order.currency_id),
        "partner_id": order.partner_id.id,
        "partner_invoice_id": order.partner_invoice_id.id if order.partner_invoice_id else None,
        "partner_shipping_id": order.partner_shipping_id.id if order.partner_shipping_id else None,
        "carrier_id": order.carrier_id.id if order.carrier_id else None,
        "access_token": order.access_token,
    }


class MobileShopApiController(http.Controller):
    _BASE = "/api/mobile/shop"

    @staticmethod
    def _resolve_variant_id(product_or_template_id):
        ProductProduct = request.env["product.product"].sudo()
        product = ProductProduct.browse(_to_int(product_or_template_id))
        if product.exists():
            return product.id
        template = request.env["product.template"].sudo().browse(_to_int(product_or_template_id))
        if template.exists() and template.product_variant_id:
            return template.product_variant_id.id
        return 0

    # -----------------------------
    # Session / Auth
    # -----------------------------
    @http.route(f"{_BASE}/session", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def session_info(self):
        user = request.env.user
        is_public = user._is_public()
        return _ok(
            {
                "uid": None if is_public else user.id,
                "is_public": is_public,
                "name": None if is_public else user.name,
                "login": None if is_public else user.login,
                "partner_id": None if is_public else user.partner_id.id,
            }
        )

    @http.route(f"{_BASE}/auth/login", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def login(self, login=None, password=None, db=None):
        if not login or not password:
            return _err("login and password required", 400)
        try:
            db_name = db or request.session.db
            if not db_name:
                return _err("database name is required", 400)
            auth_info = request.session.authenticate(db_name, {"login": login, "password": password, "type": "password"})
            if not auth_info.get("uid"):
                return _err("authentication failed", 401)
            user = request.env.user
            return _ok(
                {
                    "uid": user.id,
                    "name": user.name,
                    "login": user.login,
                    "partner_id": user.partner_id.id,
                }
            )
        except Exception as exc:
            return _err(str(exc), 401)

    @http.route(f"{_BASE}/auth/logout", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def logout(self):
        request.session.logout(keep_db=True)
        return _ok({})

    # -----------------------------
    # Catalog
    # -----------------------------
    @http.route(f"{_BASE}/categories", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def categories(self):
        website = request.website
        Category = request.env["product.public.category"].sudo()
        domain = website.website_domain()
        categories = Category.search(domain, order="name asc")
        return _ok({"items": [_category_payload(c) for c in categories]})

    @http.route(f"{_BASE}/products", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def products(
        self,
        search="",
        category_id=None,
        min_price=None,
        max_price=None,
        order="id desc",
        limit=40,
        offset=0,
    ):
        website = request.website
        Product = request.env["product.template"].with_context(bin_size=True).sudo()
        domain = website.sale_product_domain()

        if search:
            search = str(search).strip()
            domain += ["|", ("name", "ilike", search), ("default_code", "ilike", search)]
        if category_id:
            domain += [("public_categ_ids", "child_of", _to_int(category_id))]
        if min_price not in (None, ""):
            domain += [("list_price", ">=", _to_float(min_price))]
        if max_price not in (None, ""):
            domain += [("list_price", "<=", _to_float(max_price))]

        products = Product.search(domain, order=order, limit=_to_int(limit, 40), offset=_to_int(offset, 0))
        total = Product.search_count(domain)
        return _ok(
            {
                "total": total,
                "items": [_product_payload(p) for p in products],
            }
        )

    @http.route(f"{_BASE}/products/<int:product_tmpl_id>", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def product_detail(self, product_tmpl_id):
        website = request.website
        Product = request.env["product.template"].sudo()
        domain = website.sale_product_domain() + [("id", "=", product_tmpl_id)]
        product = Product.search(domain, limit=1)
        if not product:
            return _err("product not found", 404)
        return _ok({"item": _product_payload(product)})

    # -----------------------------
    # Cart
    # -----------------------------
    @http.route(f"{_BASE}/cart", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def cart(self):
        order = request.website.sale_get_order(force_create=True)
        order = order.sudo()
        lines = order.website_order_line
        return _ok(
            {
                "order": _order_payload(order),
                "lines": [_cart_line_payload(line) for line in lines],
            }
        )

    @http.route(f"{_BASE}/cart/quantity", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def cart_quantity(self):
        order = request.website.sale_get_order(force_create=True).sudo()
        return _ok({"cart_quantity": order.cart_quantity})

    @http.route(f"{_BASE}/cart/update", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def cart_update(self, product_id=None, line_id=None, add_qty=None, set_qty=None):
        if not product_id and not line_id:
            return _err("product_id or line_id required", 400)
        order = request.website.sale_get_order(force_create=True).sudo()
        kwargs = {}
        if product_id:
            variant_id = self._resolve_variant_id(product_id)
            if not variant_id:
                return _err("product not found", 404)
            kwargs["product_id"] = variant_id
        if line_id:
            kwargs["line_id"] = _to_int(line_id)
        if add_qty is not None:
            kwargs["add_qty"] = _to_float(add_qty, 0.0)
        if set_qty is not None:
            kwargs["set_qty"] = _to_float(set_qty, 0.0)
        values = order._cart_update(**kwargs)
        request.session["website_sale_cart_quantity"] = order.cart_quantity

        line = request.env["sale.order.line"].sudo().browse(values.get("line_id"))
        return _ok(
            {
                "update": values,
                "cart_quantity": order.cart_quantity,
                "order": _order_payload(order),
                "line": _cart_line_payload(line) if line.exists() else None,
            }
        )

    @http.route(f"{_BASE}/cart/clear", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def cart_clear(self):
        order = request.website.sale_get_order(force_create=True).sudo()
        order.website_order_line.unlink()
        request.session["website_sale_cart_quantity"] = 0
        return _ok({"cleared": True})

    # -----------------------------
    # Checkout helpers
    # -----------------------------
    @http.route(f"{_BASE}/delivery/methods", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def delivery_methods(self):
        order = request.website.sale_get_order(force_create=True).sudo()
        methods = order._get_delivery_methods()
        items = [
            {
                "id": m.id,
                "name": m.name,
                "delivery_type": m.delivery_type,
                "invoice_policy": m.invoice_policy,
            }
            for m in methods
        ]
        return _ok({"items": items, "selected_carrier_id": order.carrier_id.id if order.carrier_id else None})

    @http.route(f"{_BASE}/delivery/set", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def delivery_set(self, carrier_id=None):
        carrier_id = _to_int(carrier_id)
        if not carrier_id:
            return _err("carrier_id required", 400)
        order = request.website.sale_get_order(force_create=True).sudo()
        methods = order._get_delivery_methods()
        carrier = methods.filtered(lambda m: m.id == carrier_id)[:1]
        if not carrier:
            return _err("invalid carrier_id", 400)
        order._set_delivery_method(carrier)
        return _ok({"order": _order_payload(order)})

    @http.route(f"{_BASE}/coupon/apply", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def coupon_apply(self, code=None):
        if not code:
            return _err("coupon code required", 400)
        order = request.website.sale_get_order(force_create=True).sudo()
        result = order._try_apply_code(code.strip())
        if isinstance(result, dict) and result.get("error"):
            return _err(result.get("error"), 400, {"result": result})
        return _ok({"result": result, "order": _order_payload(order)})

    # -----------------------------
    # Wishlist / Compare
    # -----------------------------
    @http.route(f"{_BASE}/wishlist/add", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def wishlist_add(self, product_id=None):
        product_id = self._resolve_variant_id(product_id)
        if not product_id:
            return _err("product_id required", 400)
        product = request.env["product.product"].sudo().browse(product_id)
        if not product.exists():
            return _err("product not found", 404)

        website = request.website
        pricelist = website.pricelist_id
        price = product._get_combination_info_variant()["price"]
        Wishlist = request.env["product.wishlist"]
        if website.is_public_user():
            Wishlist = Wishlist.sudo()
            partner_id = False
        else:
            partner_id = request.env.user.partner_id.id

        wish = Wishlist._add_to_wishlist(
            pricelist.id,
            pricelist.currency_id.id,
            website.id,
            price,
            product_id,
            partner_id,
        )

        if not partner_id:
            request.session["wishlist_ids"] = request.session.get("wishlist_ids", []) + [wish.id]

        return _ok({"wish_id": wish.id, "product_id": product_id})

    @http.route(f"{_BASE}/compare/data", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def compare_data(self, product_ids=None):
        raw_ids = [int(x) for x in (product_ids or []) if str(x).isdigit()]
        if not raw_ids:
            return _ok({"items": []})
        items = []
        for raw_id in raw_ids:
            variant_id = self._resolve_variant_id(raw_id)
            if not variant_id:
                continue
            product = request.env["product.product"].sudo().browse(variant_id)
            items.append(
                {
                    "id": raw_id,
                    "variant_id": product.id,
                    "name": product.name,
                    "display_name": product.display_name,
                }
            )
        return _ok({"items": items})

    @http.route(f"{_BASE}/wishlist/ids", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def wishlist_ids(self):
        wishes = request.env["product.wishlist"].sudo().current()
        ids = wishes.mapped("product_id.product_tmpl_id.id")
        return _ok({"product_template_ids": ids})

    @http.route(f"{_BASE}/wishlist/remove", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def wishlist_remove(self, product_template_id=None):
        product_template_id = _to_int(product_template_id)
        wishes = request.env["product.wishlist"].sudo().current()
        wishes = wishes.filtered(lambda w: w.product_id.product_tmpl_id.id == product_template_id)
        wishes.unlink()
        return _ok({"removed": True})

    @http.route(f"{_BASE}/stock/notify", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def stock_notify(self, email=None, product_id=None):
        if not email:
            return _err("email required", 400)
        variant_id = self._resolve_variant_id(product_id)
        if not variant_id:
            return _err("product not found", 404)
        product = request.env["product.product"].sudo().browse(variant_id)
        partners = request.env["res.partner"].sudo()._mail_find_partner_from_emails([email], force_create=True)
        partner = partners[0]
        if not product._has_stock_notification(partner):
            product.sudo().stock_notification_partner_ids += partner
        return _ok({"subscribed": True})

    # -----------------------------
    # Orders
    # -----------------------------
    @http.route(f"{_BASE}/orders", type="json", auth="user", methods=["POST"], csrf=False, website=True)
    def orders(self, limit=20):
        partner = request.env.user.partner_id.commercial_partner_id
        orders = request.env["sale.order"].sudo().search(
            [("partner_id", "child_of", partner.id), ("state", "!=", "cancel")],
            order="date_order desc",
            limit=_to_int(limit, 20),
        )
        items = [
            {
                "id": o.id,
                "name": o.name,
                "date_order": str(o.date_order) if o.date_order else "",
                "state": o.state,
                "amount_total": o.amount_total,
                "invoice_status": o.invoice_status,
                "currency": _currency_payload(o.currency_id),
            }
            for o in orders
        ]
        return _ok({"items": items})

    @http.route(f"{_BASE}/orders/<int:order_id>/lines", type="json", auth="user", methods=["POST"], csrf=False, website=True)
    def order_lines(self, order_id):
        partner = request.env.user.partner_id.commercial_partner_id
        order = request.env["sale.order"].sudo().search(
            [("id", "=", order_id), ("partner_id", "child_of", partner.id)],
            limit=1,
        )
        if not order:
            return _err("order not found", 404)
        lines = [
            _cart_line_payload(line)
            for line in order.order_line.filtered(lambda l: not l.display_type)
        ]
        return _ok({"order_id": order.id, "lines": lines})
