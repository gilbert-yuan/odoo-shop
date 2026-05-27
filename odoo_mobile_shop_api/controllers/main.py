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

    ribbon = None
    if hasattr(product_tmpl, "website_ribbon_id") and product_tmpl.website_ribbon_id:
        r = product_tmpl.website_ribbon_id
        ribbon = {
            "id": r.id,
            "name": r.name or "",
            "bg_color": getattr(r, "bg_color", "") or "",
            "text_color": getattr(r, "text_color", "") or "",
            "html_class": getattr(r, "html_class", "") or "",
        }

    tags = []
    if hasattr(product_tmpl, "product_tag_ids"):
        for tag in product_tmpl.product_tag_ids:
            tags.append({
                "id": tag.id,
                "name": tag.name,
                "color": getattr(tag, "color", 0) or 0,
            })

    return {
        "id": product_tmpl.id,
        "name": product_tmpl.name,
        "display_name": product_tmpl.display_name,
        "website_description": product_tmpl.website_description or "",
        "description_sale": product_tmpl.description_sale or "",
        "list_price": product_tmpl.list_price,
        "compare_list_price": getattr(product_tmpl, "compare_list_price", 0) or 0,
        "currency": _currency_payload(product_tmpl.currency_id),
        "image_url": image_url,
        "is_published": bool(product_tmpl.is_published),
        "sale_ok": bool(product_tmpl.sale_ok),
        "public_category_ids": product_tmpl.public_categ_ids.ids,
        "default_code": product_tmpl.default_code or "",
        "rating_avg": getattr(product_tmpl, "rating_avg", 0) or 0,
        "rating_count": getattr(product_tmpl, "rating_count", 0) or 0,
        "ribbon": ribbon,
        "tags": tags,
        "uom_name": product_tmpl.uom_id.name if product_tmpl.uom_id else "",
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


def _address_payload(partner):
    if not partner:
        return None
    return {
        "id": partner.id,
        "name": partner.name or "",
        "email": partner.email or "",
        "phone": partner.phone or "",
        "street": partner.street or "",
        "street2": partner.street2 or "",
        "city": partner.city or "",
        "zip": partner.zip or "",
        "country_id": partner.country_id.id if partner.country_id else None,
        "country_name": partner.country_id.name if partner.country_id else "",
        "country_code": partner.country_id.code if partner.country_id else "",
        "state_id": partner.state_id.id if partner.state_id else None,
        "state_name": partner.state_id.name if partner.state_id else "",
        "vat": partner.vat or "",
        "type": partner.type or "contact",
        "is_company": bool(partner.is_company),
        "parent_id": partner.parent_id.id if partner.parent_id else None,
    }


def _carrier_payload(carrier):
    if not carrier:
        return None
    return {
        "id": carrier.id,
        "name": carrier.name,
        "delivery_type": carrier.delivery_type,
    }


def _payment_payload(transaction):
    if not transaction:
        return None
    provider = transaction.provider_id
    return {
        "tx_id": transaction.id,
        "state": transaction.state,
        "amount": transaction.amount,
        "reference": transaction.reference,
        "provider_id": provider.id if provider else None,
        "provider_code": provider.code if provider else "",
        "provider_name": provider.name if provider else "",
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


def _order_payload_full(order):
    base = _order_payload(order)
    base["lines"] = [_cart_line_payload(line) for line in order.website_order_line]
    base["billing_address"] = _address_payload(order.partner_invoice_id) if order.partner_invoice_id else None
    base["shipping_address"] = _address_payload(order.partner_shipping_id) if order.partner_shipping_id else None
    base["partner"] = _address_payload(order.partner_id) if order.partner_id else None
    base["carrier"] = _carrier_payload(order.carrier_id) if order.carrier_id else None
    base["date_order"] = str(order.date_order) if order.date_order else ""
    base["invoice_status"] = order.invoice_status

    txs = order.transaction_ids.sorted("create_date", reverse=True)
    base["payment"] = _payment_payload(txs[:1]) if txs else None
    return base


def _is_public_user():
    return request.env.user._is_public()


def _website_public_partner_id():
    website = request.website
    public_user = website.user_id
    return public_user.partner_id.id if public_user else None


def _can_access_order(order):
    if not order or not order.exists():
        return False
    user = request.env.user
    if user._is_public():
        return False
    partner = user.partner_id
    commercial = partner.commercial_partner_id
    if order.partner_id == partner or order.partner_id == commercial:
        return True
    if order.partner_id.commercial_partner_id == commercial:
        return True
    return False


def _can_access_partner(partner):
    """For mutating/listing personal address book operations (requires login)."""
    if not partner.exists():
        return False
    user = request.env.user
    if user._is_public():
        return False
    commercial = user.partner_id.commercial_partner_id
    return partner == commercial or partner.parent_id == commercial


def _product_full_payload(product_tmpl, website=None):
    """Full product payload: base info + images + variants + attribute lines + pricelist price."""
    payload = _product_payload(product_tmpl)

    image_urls = [f"/web/image/product.template/{product_tmpl.id}/image_1024"]
    for img in product_tmpl.product_template_image_ids:
        image_urls.append(f"/web/image/product.image/{img.id}/image_1024")
    payload["image_urls"] = image_urls

    payload["attribute_lines"] = []
    for line in product_tmpl.attribute_line_ids:
        if line.attribute_id.create_variant == "no_variant":
            continue
        payload["attribute_lines"].append({
            "id": line.id,
            "attribute_id": line.attribute_id.id,
            "attribute_name": line.attribute_id.name,
            "display_type": line.attribute_id.display_type,
            "values": [
                {
                    "id": v.id,
                    "ptav_id": ptav.id,
                    "name": v.name,
                    "html_color": v.html_color or "",
                    "price_extra": ptav.price_extra,
                }
                for v, ptav in [
                    (val, line.product_template_value_ids.filtered(lambda p: p.product_attribute_value_id == val)[:1])
                    for val in line.value_ids
                ]
                if ptav
            ],
        })

    variants = []
    for variant in product_tmpl.product_variant_ids:
        try:
            variant_price = variant._get_combination_info_variant().get("price", variant.lst_price)
        except Exception:
            variant_price = variant.lst_price
        variants.append({
            "id": variant.id,
            "default_code": variant.default_code or "",
            "list_price": variant.lst_price,
            "price": variant_price,
            "image_url": f"/web/image/product.product/{variant.id}/image_512",
            "ptav_ids": variant.product_template_attribute_value_ids.ids,
            "qty_available": variant.qty_available if hasattr(variant, "qty_available") else 0,
            "free_qty": variant.free_qty if hasattr(variant, "free_qty") else 0,
            "is_in_stock": (variant.free_qty > 0) if hasattr(variant, "free_qty") else True,
        })
    payload["variants"] = variants

    if website:
        try:
            combo = product_tmpl._get_combination_info(
                combination=False,
                product_id=False,
                add_qty=1,
                pricelist=website.pricelist_id,
            )
            payload["price"] = combo.get("price", product_tmpl.list_price)
            payload["price_extra"] = combo.get("price_extra", 0)
            payload["has_discounted_price"] = bool(combo.get("has_discounted_price"))
            payload["list_price"] = combo.get("list_price", product_tmpl.list_price)
            payload["combination_info"] = {
                k: v for k, v in combo.items()
                if isinstance(v, (str, int, float, bool, type(None), list, dict))
            }
        except Exception:
            payload["price"] = product_tmpl.list_price

    return payload


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
        line_id_int = _to_int(line_id) if line_id else 0
        set_qty_provided = set_qty is not None and set_qty != ""
        set_qty_float = _to_float(set_qty, -1.0) if set_qty_provided else -1.0
        add_qty_provided = add_qty is not None and add_qty != ""
        add_qty_float = _to_float(add_qty, 0.0) if add_qty_provided else 0.0

        # Path 1 — explicit removal: set_qty <= 0 on an existing line
        if line_id_int and set_qty_provided and set_qty_float <= 0:
            line = request.env["sale.order.line"].sudo().browse(line_id_int)
            if not line.exists() or line.order_id.id != order.id:
                return _err("line not found in current cart", 404)
            try:
                line.unlink()
            except Exception as exc:
                return _err(f"failed to remove line: {exc}", 400)
            request.session["website_sale_cart_quantity"] = order.cart_quantity
            return _ok({
                "removed": True,
                "cart_quantity": order.cart_quantity,
                "order": _order_payload(order),
                "line": None,
            })

        # Path 2 — set quantity on an existing line (set_qty > 0)
        if line_id_int and set_qty_provided and set_qty_float > 0:
            line = request.env["sale.order.line"].sudo().browse(line_id_int)
            if not line.exists() or line.order_id.id != order.id:
                return _err("line not found in current cart", 404)
            values = {}
            try:
                values = order._cart_update(
                    line_id=line.id,
                    product_id=line.product_id.id,
                    set_qty=set_qty_float,
                ) or {}
            except Exception:
                try:
                    line.write({"product_uom_qty": set_qty_float})
                    values = {"line_id": line.id, "quantity": set_qty_float}
                except Exception as exc:
                    return _err(f"failed to set quantity: {exc}", 400)
            request.session["website_sale_cart_quantity"] = order.cart_quantity
            return _ok({
                "update": values,
                "cart_quantity": order.cart_quantity,
                "order": _order_payload(order),
                "line": _cart_line_payload(line) if line.exists() else None,
            })

        # Path 3 — add to cart (add_qty with product_id, or pure add)
        if product_id and add_qty_provided:
            variant_id = self._resolve_variant_id(product_id)
            if not variant_id:
                return _err("product not found", 404)
            try:
                values = order._cart_update(
                    product_id=variant_id,
                    add_qty=add_qty_float,
                ) or {}
            except Exception as exc:
                return _err(f"failed to add to cart: {exc}", 400)
            request.session["website_sale_cart_quantity"] = order.cart_quantity
            line = request.env["sale.order.line"].sudo().browse(values.get("line_id") or 0)
            return _ok({
                "update": values,
                "cart_quantity": order.cart_quantity,
                "order": _order_payload(order),
                "line": _cart_line_payload(line) if line.exists() else None,
            })

        # Path 4 — generic fallback (kwargs passthrough)
        kwargs = {}
        if product_id:
            variant_id = self._resolve_variant_id(product_id)
            if variant_id:
                kwargs["product_id"] = variant_id
        if line_id_int:
            kwargs["line_id"] = line_id_int
        if add_qty_provided:
            kwargs["add_qty"] = add_qty_float
        if set_qty_provided:
            kwargs["set_qty"] = set_qty_float
        try:
            values = order._cart_update(**kwargs) or {}
        except Exception as exc:
            return _err(f"cart update failed: {exc}", 400)
        request.session["website_sale_cart_quantity"] = order.cart_quantity
        line = request.env["sale.order.line"].sudo().browse(values.get("line_id") or 0)
        return _ok({
            "update": values,
            "cart_quantity": order.cart_quantity,
            "order": _order_payload(order),
            "line": _cart_line_payload(line) if line.exists() else None,
        })

    @http.route(f"{_BASE}/cart/clear", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def cart_clear(self):
        order = request.website.sale_get_order(force_create=True).sudo()
        order.website_order_line.unlink()
        request.session["website_sale_cart_quantity"] = 0
        return _ok({"cleared": True})

    # -----------------------------
    # Geography (countries / states)
    # -----------------------------
    @http.route(f"{_BASE}/countries", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def countries(self):
        records = request.env["res.country"].sudo().search([], order="name asc")
        return _ok({
            "items": [
                {
                    "id": c.id,
                    "name": c.name,
                    "code": c.code or "",
                    "phone_code": c.phone_code,
                    "state_required": bool(c.state_required),
                    "zip_required": bool(c.zip_required),
                    "vat_label": c.vat_label or "VAT",
                }
                for c in records
            ]
        })

    @http.route(f"{_BASE}/countries/<int:country_id>/states", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def country_states(self, country_id):
        records = request.env["res.country.state"].sudo().search(
            [("country_id", "=", country_id)],
            order="name asc",
        )
        return _ok({
            "items": [
                {
                    "id": s.id,
                    "name": s.name,
                    "code": s.code or "",
                    "country_id": s.country_id.id,
                }
                for s in records
            ]
        })

    # -----------------------------
    # Address book
    # -----------------------------
    @http.route(f"{_BASE}/addresses", type="json", auth="user", methods=["POST"], csrf=False, website=True)
    def addresses_list(self, address_type="all"):
        commercial = request.env.user.partner_id.commercial_partner_id
        Partner = request.env["res.partner"].sudo()
        domain = ["|", ("id", "=", commercial.id), ("parent_id", "=", commercial.id)]
        if address_type == "billing":
            domain += [("type", "in", ("contact", "invoice", "other"))]
        elif address_type == "shipping":
            domain += [("type", "in", ("contact", "delivery", "other"))]
        partners = Partner.search(domain, order="id asc")
        order = request.website.sale_get_order(force_create=False)
        return _ok({
            "items": [_address_payload(p) for p in partners],
            "default_billing_id": commercial.id,
            "default_shipping_id": commercial.id,
            "current_billing_id": order.partner_invoice_id.id if order and order.partner_invoice_id else None,
            "current_shipping_id": order.partner_shipping_id.id if order and order.partner_shipping_id else None,
        })

    @http.route(f"{_BASE}/addresses/save", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def address_save(self, partner_id=None, address_type="billing", form=None, use_on_order=True):
        form = form or {}
        order = request.website.sale_get_order(force_create=True).sudo()
        Partner = request.env["res.partner"].sudo()

        vals = {}
        for key in ("name", "email", "phone", "street", "street2", "city", "zip", "vat"):
            value = form.get(key)
            if value is not None:
                vals[key] = str(value).strip()
        country_id = _to_int(form.get("country_id"))
        state_id = _to_int(form.get("state_id"))
        if country_id:
            vals["country_id"] = country_id
        if state_id:
            vals["state_id"] = state_id

        partner_id = _to_int(partner_id)
        is_public = _is_public_user()
        is_first_time_guest = False

        if partner_id:
            partner = Partner.browse(partner_id)
            if not partner.exists():
                return _err("partner not found", 404)
            if is_public:
                if partner != order.partner_id and partner.parent_id != order.partner_id:
                    return _err("access denied", 403)
            else:
                commercial = request.env.user.partner_id.commercial_partner_id
                if partner != commercial and partner.parent_id != commercial:
                    return _err("access denied", 403)
            partner.write(vals)
        else:
            if is_public:
                public_partner_id = _website_public_partner_id()
                is_first_time_guest = not order.partner_id or order.partner_id.id == public_partner_id
                if is_first_time_guest:
                    partner = Partner.create(vals)
                else:
                    target_type = "delivery" if address_type == "shipping" else "invoice"
                    create_vals = dict(vals)
                    create_vals["parent_id"] = order.partner_id.id
                    create_vals["type"] = target_type
                    partner = Partner.create(create_vals)
            else:
                commercial = request.env.user.partner_id.commercial_partner_id
                target_type = "delivery" if address_type == "shipping" else "invoice"
                create_vals = dict(vals)
                create_vals["parent_id"] = commercial.id
                create_vals["type"] = target_type
                partner = Partner.create(create_vals)

        if use_on_order:
            if address_type == "shipping":
                order.write({"partner_shipping_id": partner.id})
            else:
                update = {"partner_invoice_id": partner.id}
                if is_first_time_guest:
                    update["partner_id"] = partner.id
                    update["partner_shipping_id"] = partner.id
                order.write(update)

        return _ok({"partner": _address_payload(partner), "order": _order_payload_full(order)})

    @http.route(f"{_BASE}/addresses/<int:partner_id>/delete", type="json", auth="user", methods=["POST"], csrf=False, website=True)
    def address_delete(self, partner_id):
        commercial = request.env.user.partner_id.commercial_partner_id
        partner = request.env["res.partner"].sudo().browse(partner_id)
        if not partner.exists():
            return _err("partner not found", 404)
        if partner == commercial:
            return _err("cannot delete the account's primary partner", 400)
        if partner.parent_id != commercial:
            return _err("access denied", 403)
        partner.write({"active": False})
        return _ok({"deleted": True, "id": partner_id})

    @http.route(f"{_BASE}/addresses/<int:partner_id>/use", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def address_use(self, partner_id, address_type="billing"):
        order = request.website.sale_get_order(force_create=True).sudo()
        partner = request.env["res.partner"].sudo().browse(partner_id)
        if not partner.exists():
            return _err("partner not found", 404)
        is_public = _is_public_user()
        if is_public:
            if partner != order.partner_id and partner.parent_id != order.partner_id:
                return _err("access denied", 403)
        else:
            commercial = request.env.user.partner_id.commercial_partner_id
            if partner != commercial and partner.parent_id != commercial:
                return _err("access denied", 403)
        if address_type == "shipping":
            order.write({"partner_shipping_id": partner.id})
        else:
            order.write({"partner_invoice_id": partner.id})
        return _ok({"order": _order_payload_full(order)})

    @http.route(f"{_BASE}/addresses/<int:partner_id>/default", type="json", auth="user", methods=["POST"], csrf=False, website=True)
    def address_default(self, partner_id, address_type="billing"):
        commercial = request.env.user.partner_id.commercial_partner_id
        Partner = request.env["res.partner"].sudo()
        partner = Partner.browse(partner_id)
        if not partner.exists():
            return _err("partner not found", 404)
        if partner != commercial and partner.parent_id != commercial:
            return _err("access denied", 403)
        target_type = "delivery" if address_type == "shipping" else "invoice"
        siblings = Partner.search([
            ("parent_id", "=", commercial.id),
            ("type", "=", target_type),
            ("id", "!=", partner.id),
        ])
        if siblings:
            siblings.write({"type": "contact"})
        if partner != commercial:
            partner.write({"type": target_type})
        return _ok({"partner": _address_payload(partner)})

    # -----------------------------
    # Order detail / confirm
    # -----------------------------
    @http.route(f"{_BASE}/order", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def current_order(self):
        order = request.website.sale_get_order(force_create=True).sudo()
        return _ok({"order": _order_payload_full(order)})

    @http.route(f"{_BASE}/order/<int:order_id>", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def order_detail(self, order_id, access_token=None):
        order = request.env["sale.order"].sudo().browse(order_id)
        if not order.exists():
            return _err("order not found", 404)
        if not _can_access_order(order):
            if not access_token or access_token != order.access_token:
                return _err("access denied", 403)
        return _ok({"order": _order_payload_full(order)})

    @http.route(f"{_BASE}/order/confirm", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def order_confirm(self):
        order = request.website.sale_get_order(force_create=False)
        if not order:
            return _err("no active cart", 400)
        order = order.sudo()
        if not order.order_line:
            return _err("cart is empty", 400, {"step": "cart"})

        public_partner_id = _website_public_partner_id()
        if not order.partner_invoice_id or order.partner_invoice_id.id == public_partner_id:
            return _err("billing address required", 400, {"step": "address"})
        if not order.partner_shipping_id or order.partner_shipping_id.id == public_partner_id:
            return _err("shipping address required", 400, {"step": "address"})

        methods = order._get_delivery_methods()
        if methods and not order.carrier_id:
            return _err("delivery method required", 400, {"step": "delivery"})

        return _ok({
            "ready": True,
            "order_id": order.id,
            "access_token": order.access_token,
            "amount_total": order.amount_total,
        })

    # -----------------------------
    # Checkout helpers (delivery / coupon)
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
        return _ok({"order": _order_payload_full(order)})

    @http.route(f"{_BASE}/delivery/rate", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def delivery_rate(self, carrier_id=None):
        carrier_id = _to_int(carrier_id)
        if not carrier_id:
            return _err("carrier_id required", 400)
        order = request.website.sale_get_order(force_create=False)
        if not order:
            return _err("no active cart", 400)
        order = order.sudo()
        carrier = request.env["delivery.carrier"].sudo().browse(carrier_id)
        if not carrier.exists():
            return _err("invalid carrier", 404)
        try:
            rate = carrier.rate_shipment(order)
        except Exception as exc:
            return _err(str(exc), 400)
        return _ok({
            "success": bool(rate.get("success")),
            "price": rate.get("price"),
            "error_message": rate.get("error_message") or "",
            "warning_message": rate.get("warning_message") or "",
        })

    @http.route(f"{_BASE}/coupon/apply", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def coupon_apply(self, code=None):
        if not code:
            return _err("coupon code required", 400)
        order = request.website.sale_get_order(force_create=True).sudo()
        result = order._try_apply_code(code.strip())
        if isinstance(result, dict) and result.get("error"):
            return _err(result.get("error"), 400, {"result": result})
        return _ok({"result": result, "order": _order_payload_full(order)})

    # -----------------------------
    # Reward / Loyalty
    # -----------------------------
    @http.route(f"{_BASE}/reward/claim", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def reward_claim(self, reward_id=None, code=None, product_id=None):
        order = request.website.sale_get_order(force_create=False)
        if not order:
            return _err("no active cart", 400)
        order = order.sudo()

        if code:
            result = order._try_apply_code(str(code).strip())
            if isinstance(result, dict) and result.get("error"):
                return _err(result["error"], 400, {"result": result})

        reward_id = _to_int(reward_id)
        if reward_id:
            reward = request.env["loyalty.reward"].sudo().browse(reward_id)
            if not reward.exists():
                return _err("invalid reward", 404)
            try:
                claimable = order._get_claimable_rewards()
            except Exception as exc:
                return _err(f"reward lookup failed: {exc}", 400)
            target_coupon = None
            for coupon, rewards in claimable.items():
                if reward in rewards:
                    target_coupon = coupon
                    break
            if target_coupon is None:
                return _err("reward not claimable for this cart", 400)
            try:
                order._apply_program_reward(reward, target_coupon)
            except Exception as exc:
                return _err(str(exc), 400)

        return _ok({"order": _order_payload_full(order)})

    # -----------------------------
    # Payment
    # -----------------------------
    @http.route(f"{_BASE}/payment/providers", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def payment_providers(self, order_id=None, access_token=None):
        order_id = _to_int(order_id)
        if order_id:
            order = request.env["sale.order"].sudo().browse(order_id)
            if not order.exists():
                return _err("order not found", 404)
            if access_token != order.access_token and not _can_access_order(order):
                return _err("access denied", 403)
        else:
            order = request.website.sale_get_order(force_create=False)
            if not order:
                return _err("no active cart", 400)
            order = order.sudo()

        partner = order.partner_invoice_id or order.partner_id
        currency = order.currency_id
        company = order.company_id
        website = request.website

        Provider = request.env["payment.provider"].sudo()
        try:
            providers = Provider._get_compatible_providers(
                company.id,
                partner.id,
                order.amount_total,
                currency_id=currency.id,
                sale_order_id=order.id,
                website_id=website.id,
            )
        except Exception:
            providers = Provider.search([
                ("state", "in", ("enabled", "test")),
                ("company_id", "=", company.id),
            ])

        PaymentMethod = request.env["payment.method"].sudo()
        try:
            payment_methods = PaymentMethod._get_compatible_payment_methods(
                providers.ids,
                partner.id,
                currency_id=currency.id,
            )
        except Exception:
            payment_methods = PaymentMethod.search([("provider_ids", "in", providers.ids)]) if providers else PaymentMethod

        tokens = request.env["payment.token"].sudo()
        if not _is_public_user():
            try:
                tokens = tokens._get_available_tokens(
                    providers.ids,
                    partner.id,
                )
            except Exception:
                tokens = tokens.search([
                    ("partner_id", "=", partner.id),
                    ("provider_id", "in", providers.ids),
                ])

        return _ok({
            "providers": [
                {
                    "id": p.id,
                    "name": p.name,
                    "code": p.code,
                    "state": p.state,
                    "display_as": getattr(p, "display_as", None) or p.name,
                    "image_url": f"/web/image/payment.provider/{p.id}/image",
                    "payment_method_ids": p.payment_method_ids.ids if hasattr(p, "payment_method_ids") else [],
                    "pre_msg": getattr(p, "pre_msg", "") or "",
                }
                for p in providers
            ],
            "payment_methods": [
                {
                    "id": m.id,
                    "name": m.name,
                    "code": m.code,
                    "image_url": f"/web/image/payment.method/{m.id}/image",
                    "provider_ids": m.provider_ids.ids if hasattr(m, "provider_ids") else [],
                }
                for m in payment_methods
            ],
            "tokens": [
                {
                    "id": t.id,
                    "name": t.display_name,
                    "provider_id": t.provider_id.id,
                    "payment_method_id": t.payment_method_id.id
                    if hasattr(t, "payment_method_id") and t.payment_method_id
                    else None,
                }
                for t in tokens
            ],
        })

    @http.route(f"{_BASE}/payment/transaction", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def payment_transaction(
        self,
        order_id=None,
        access_token=None,
        provider_id=None,
        payment_method_id=None,
        token_id=None,
        flow="redirect",
        landing_route="/checkout/done",
    ):
        order_id = _to_int(order_id)
        order = request.env["sale.order"].sudo().browse(order_id)
        if not order.exists():
            return _err("order not found", 404)
        if access_token != order.access_token and not _can_access_order(order):
            return _err("invalid access token", 403)
        if not order.order_line:
            return _err("cart is empty", 400)

        provider_id = _to_int(provider_id)
        payment_method_id = _to_int(payment_method_id)
        token_id = _to_int(token_id) or None

        provider = request.env["payment.provider"].sudo().browse(provider_id)
        if not provider.exists():
            return _err("invalid provider", 400)

        partner = order.partner_invoice_id or order.partner_id
        operation = "online_token" if token_id else f"online_{flow}"
        landing = f"{landing_route}/{order.id}?access_token={order.access_token}"

        try:
            reference = request.env["payment.transaction"].sudo()._compute_reference(
                provider.code,
                prefix=order.name,
                sale_order_ids=[(6, 0, [order.id])],
            )
        except Exception:
            reference = f"{order.name}-{provider.code}"

        tx_vals = {
            "amount": order.amount_total,
            "currency_id": order.currency_id.id,
            "partner_id": partner.id,
            "provider_id": provider.id,
            "operation": operation,
            "sale_order_ids": [(6, 0, [order.id])],
            "landing_route": landing,
            "reference": reference,
        }
        if payment_method_id:
            tx_vals["payment_method_id"] = payment_method_id
        if token_id:
            tx_vals["token_id"] = token_id

        try:
            transaction = request.env["payment.transaction"].sudo().create(tx_vals)
        except Exception as exc:
            return _err(f"transaction create failed: {exc}", 400)

        processing_values = {}
        try:
            processing_values = transaction._get_processing_values() or {}
        except Exception as exc:
            return _err(f"processing values failed: {exc}", 400, {"tx_id": transaction.id})

        return _ok({
            "tx_id": transaction.id,
            "reference": transaction.reference,
            "state": transaction.state,
            "provider_code": provider.code,
            "redirect_url": processing_values.get("redirect_url"),
            "redirect_form_html": processing_values.get("redirect_form_html"),
            "landing_route": landing,
            "processing_values": {
                k: v for k, v in processing_values.items()
                if isinstance(v, (str, int, float, bool, type(None)))
            },
        })

    @http.route(f"{_BASE}/payment/status", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def payment_status(self, order_id=None, access_token=None):
        order_id = _to_int(order_id)
        order = request.env["sale.order"].sudo().browse(order_id)
        if not order.exists():
            return _err("order not found", 404)
        if access_token != order.access_token and not _can_access_order(order):
            return _err("access denied", 403)

        txs = order.transaction_ids.sorted("create_date", reverse=True)
        last_tx = txs[:1]
        return _ok({
            "order_id": order.id,
            "order_state": order.state,
            "amount_total": order.amount_total,
            "tx": _payment_payload(last_tx) if last_tx else None,
        })

    # -----------------------------
    # Wishlist / Compare / Stock
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
    # Orders (authenticated)
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

    # -----------------------------
    # Products: variants / images / pricelist
    # -----------------------------
    @http.route(f"{_BASE}/products/<int:product_tmpl_id>/full", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def product_full(self, product_tmpl_id):
        website = request.website
        Product = request.env["product.template"].sudo()
        domain = website.sale_product_domain() + [("id", "=", product_tmpl_id)]
        product = Product.search(domain, limit=1)
        if not product:
            return _err("product not found", 404)
        return _ok({"item": _product_full_payload(product, website=website)})

    @http.route(f"{_BASE}/products/<int:product_tmpl_id>/combination", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def product_combination(self, product_tmpl_id, ptav_ids=None, add_qty=1):
        website = request.website
        Product = request.env["product.template"].sudo()
        product = Product.browse(product_tmpl_id)
        if not product.exists():
            return _err("product not found", 404)
        ptav_ids = [int(x) for x in (ptav_ids or []) if str(x).isdigit()]
        try:
            combo = product._get_combination_info(
                combination=request.env["product.template.attribute.value"].sudo().browse(ptav_ids),
                add_qty=_to_float(add_qty, 1.0),
                pricelist=website.pricelist_id,
            )
        except Exception as exc:
            return _err(str(exc), 400)
        serializable = {
            k: v for k, v in combo.items()
            if isinstance(v, (str, int, float, bool, type(None), list, dict))
        }
        variant_id = combo.get("product_id") or 0
        if variant_id:
            variant = request.env["product.product"].sudo().browse(variant_id)
            serializable["image_url"] = f"/web/image/product.product/{variant.id}/image_1024"
            serializable["qty_available"] = variant.qty_available if hasattr(variant, "qty_available") else 0
            serializable["free_qty"] = variant.free_qty if hasattr(variant, "free_qty") else 0
            serializable["is_in_stock"] = (variant.free_qty > 0) if hasattr(variant, "free_qty") else True
        return _ok({"combination": serializable})

    # -----------------------------
    # Auth: register / password / profile
    # -----------------------------
    @http.route(f"{_BASE}/auth/register", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def register(self, name=None, login=None, password=None, phone=None):
        if not name or not login or not password:
            return _err("name, login and password required", 400)
        if len(password) < 6:
            return _err("password must be at least 6 characters", 400)

        existing = request.env["res.users"].sudo().search([("login", "=", login)], limit=1)
        if existing:
            return _err("account already exists", 400)

        website = request.website
        signup_group = website.auth_signup_uninvited == "b2c" if hasattr(website, "auth_signup_uninvited") else True
        if not signup_group:
            return _err("signup disabled on this website", 403)

        try:
            user_vals = {
                "name": name,
                "login": login,
                "email": login,
                "password": password,
            }
            if phone:
                user_vals["phone"] = phone
            portal_group = request.env.ref("base.group_portal", raise_if_not_found=False)
            if portal_group:
                user_vals["groups_id"] = [(6, 0, [portal_group.id])]
            user = request.env["res.users"].sudo().with_context(no_reset_password=True).create(user_vals)
        except Exception as exc:
            return _err(f"registration failed: {exc}", 400)

        try:
            db_name = request.session.db
            if db_name:
                request.session.authenticate(db_name, {"login": login, "password": password, "type": "password"})
        except Exception:
            pass

        return _ok({
            "uid": user.id,
            "name": user.name,
            "login": user.login,
            "partner_id": user.partner_id.id,
        })

    @http.route(f"{_BASE}/auth/password/forgot", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def password_forgot(self, login=None):
        if not login:
            return _err("login required", 400)
        user = request.env["res.users"].sudo().search([("login", "=", login)], limit=1)
        if not user:
            return _ok({"sent": True})
        try:
            user.action_reset_password()
        except Exception as exc:
            return _err(str(exc), 400)
        return _ok({"sent": True})

    @http.route(f"{_BASE}/auth/password/reset", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def password_reset(self, token=None, login=None, new_password=None):
        if not token or not login or not new_password:
            return _err("token, login and new_password required", 400)
        if len(new_password) < 6:
            return _err("password must be at least 6 characters", 400)
        try:
            db_name = request.session.db
            request.env["res.users"].sudo().signup({
                "login": login,
                "password": new_password,
                "token": token,
            }, token=token)
            if db_name:
                request.session.authenticate(db_name, {"login": login, "password": new_password, "type": "password"})
        except Exception as exc:
            return _err(str(exc), 400)
        return _ok({"reset": True})

    @http.route(f"{_BASE}/auth/password/change", type="json", auth="user", methods=["POST"], csrf=False, website=True)
    def password_change(self, current_password=None, new_password=None):
        if not current_password or not new_password:
            return _err("current_password and new_password required", 400)
        if len(new_password) < 6:
            return _err("password must be at least 6 characters", 400)
        user = request.env.user
        try:
            request.env["res.users"].sudo().change_password(current_password, new_password)
        except Exception as exc:
            return _err(str(exc), 400)
        try:
            db_name = request.session.db
            if db_name:
                request.session.authenticate(db_name, {"login": user.login, "password": new_password, "type": "password"})
        except Exception:
            pass
        return _ok({"changed": True})

    @http.route(f"{_BASE}/profile", type="json", auth="user", methods=["POST"], csrf=False, website=True)
    def profile_get(self):
        user = request.env.user
        partner = user.partner_id
        return _ok({
            "uid": user.id,
            "name": partner.name or "",
            "email": partner.email or user.login,
            "phone": partner.phone or "",
            "login": user.login,
            "lang": user.lang or "",
            "tz": user.tz or "",
            "partner_id": partner.id,
        })

    @http.route(f"{_BASE}/profile/update", type="json", auth="user", methods=["POST"], csrf=False, website=True)
    def profile_update(self, name=None, email=None, phone=None, lang=None):
        user = request.env.user
        partner = user.partner_id
        partner_vals = {}
        user_vals = {}
        if name is not None:
            partner_vals["name"] = name
            user_vals["name"] = name
        if email is not None:
            partner_vals["email"] = email
        if phone is not None:
            partner_vals["phone"] = phone
        if lang is not None and lang:
            partner_vals["lang"] = lang
            user_vals["lang"] = lang
        if partner_vals:
            partner.sudo().write(partner_vals)
        if user_vals:
            user.sudo().write(user_vals)
        return _ok({
            "name": partner.name,
            "email": partner.email,
            "phone": partner.phone,
            "lang": user.lang,
        })

    # -----------------------------
    # Languages / Sitemap
    # -----------------------------
    @http.route(f"{_BASE}/languages", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def languages(self):
        website = request.website
        try:
            langs = website.language_ids
        except Exception:
            langs = request.env["res.lang"].sudo().search([("active", "=", True)])
        return _ok({
            "default": website.default_lang_id.code if getattr(website, "default_lang_id", False) else "en_US",
            "items": [
                {
                    "code": lang.code,
                    "name": lang.name,
                    "iso_code": lang.iso_code or "",
                    "url_code": lang.url_code or lang.code,
                }
                for lang in langs
            ],
        })

    @http.route(f"{_BASE}/sitemap", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def sitemap_data(self):
        website = request.website
        Product = request.env["product.template"].sudo()
        products = Product.search(website.sale_product_domain(), limit=1000)
        Category = request.env["product.public.category"].sudo()
        categories = Category.search(website.website_domain())
        return _ok({
            "products": [
                {
                    "id": p.id,
                    "url": f"/product/{p.id}",
                    "name": p.name,
                    "write_date": str(p.write_date) if p.write_date else "",
                }
                for p in products
            ],
            "categories": [
                {
                    "id": c.id,
                    "url": f"/shop?category={c.id}",
                    "name": c.name,
                }
                for c in categories
            ],
            "static_pages": [
                {"url": "/", "name": "Home"},
                {"url": "/shop", "name": "Shop"},
            ],
        })

    # -----------------------------
    # Contact / Wholesale lead capture
    # -----------------------------
    @http.route(f"{_BASE}/contact", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def contact_submit(self, name=None, email=None, phone=None, subject=None, message=None):
        if not email or not message:
            return _err("email and message required", 400)
        if "crm.lead" not in request.env:
            return _err("CRM module not installed on this Odoo instance", 501)
        Lead = request.env["crm.lead"].sudo()
        try:
            lead = Lead.create({
                "name": (subject or "").strip() or f"Contact from {name or email}",
                "contact_name": (name or "").strip(),
                "email_from": email.strip(),
                "phone": (phone or "").strip(),
                "description": (message or "").strip(),
                "type": "lead",
            })
        except Exception as exc:
            return _err(f"failed to submit: {exc}", 400)
        return _ok({"submitted": True, "id": lead.id})

    @http.route(f"{_BASE}/wholesale", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def wholesale_submit(
        self,
        company=None,
        name=None,
        email=None,
        phone=None,
        country=None,
        products=None,
        volume=None,
        message=None,
    ):
        if not email or not company:
            return _err("company and email required", 400)
        if "crm.lead" not in request.env:
            return _err("CRM module not installed on this Odoo instance", 501)
        Lead = request.env["crm.lead"].sudo()
        Tag = request.env["crm.tag"].sudo()
        tag = Tag.search([("name", "=", "Wholesale")], limit=1)
        if not tag:
            try:
                tag = Tag.create({"name": "Wholesale"})
            except Exception:
                tag = False

        description_lines = []
        if country:
            description_lines.append(f"Country: {country}")
        if products:
            description_lines.append(f"Products of interest: {products}")
        if volume:
            description_lines.append(f"Estimated volume: {volume}")
        if message:
            description_lines.append("")
            description_lines.append(str(message))

        vals = {
            "name": f"Wholesale inquiry: {company}",
            "partner_name": company,
            "contact_name": (name or "").strip(),
            "email_from": email.strip(),
            "phone": (phone or "").strip(),
            "description": "\n".join(description_lines),
            "type": "lead",
        }
        if tag:
            vals["tag_ids"] = [(6, 0, [tag.id])]

        try:
            lead = Lead.create(vals)
        except Exception as exc:
            return _err(f"failed to submit: {exc}", 400)
        return _ok({"submitted": True, "id": lead.id})

    @http.route(f"{_BASE}/coa/lookup", type="json", auth="public", methods=["POST"], csrf=False, website=True)
    def coa_lookup(self, code=None):
        if not code:
            return _err("code required", 400)
        code = str(code).strip()

        items = []
        # Prefer product.document (Odoo 17+); fall back to ir.attachment
        try:
            Document = request.env["product.document"].sudo()
            docs = Document.search([("name", "ilike", code)], limit=20)
            for d in docs:
                attachment_id = d.id
                if hasattr(d, "ir_attachment_id") and d.ir_attachment_id:
                    attachment_id = d.ir_attachment_id.id
                items.append({
                    "id": d.id,
                    "name": d.name,
                    "url": f"/web/content/{attachment_id}?download=true",
                    "mimetype": getattr(d, "mimetype", "") or "",
                    "product_id": d.res_id if hasattr(d, "res_id") and d.res_model in ("product.template", "product.product") else None,
                })
        except Exception:
            pass

        if not items:
            Attachment = request.env["ir.attachment"].sudo()
            atts = Attachment.search([
                ("name", "ilike", code),
                ("res_model", "in", ("product.template", "product.product", "product.document")),
            ], limit=20)
            for a in atts:
                items.append({
                    "id": a.id,
                    "name": a.name,
                    "url": f"/web/content/{a.id}?download=true",
                    "mimetype": a.mimetype or "",
                    "product_id": a.res_id if a.res_model in ("product.template", "product.product") else None,
                })

        return _ok({"items": items, "code": code})
