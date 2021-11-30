
from odoo import http, fields
from odoo.http import request
from odoo.tools.safe_eval import json


class WebsiteSale(http.Controller):

    @http.route(['/shop/cart/update_json'], type='json', auth="public",
                methods=['POST'], website=True, csrf=False)
    def cart_update_json(self, product_id, line_id=None, add_qty=None,
                         set_qty=None, display=True):
        """This route is called when changing quantity from the cart or adding
        a product from the wishlist."""
        order = request.website.sale_get_order(force_create=1)
        if order.state != 'draft':
            request.website.sale_reset()
            return {}

        value = order._cart_update(product_id=product_id, line_id=line_id,
                                   add_qty=add_qty, set_qty=set_qty)

        # print(value)
        if not order.cart_quantity:
            request.website.sale_reset()
            return value

        order = request.website.sale_get_order()
        value['cart_quantity'] = order.cart_quantity

        if not display:
            return value

        value['website_sale.cart_lines'] = request.env[
            'ir.ui.view']._render_template("website_sale.cart_lines", {
            'website_sale_order': order,
            'date': fields.Date.today(),
            'suggested_products': order._cart_accessories()
        })
        value['website_sale.short_cart_summary'] = request.env[
            'ir.ui.view']._render_template("website_sale.short_cart_summary", {
            'website_sale_order': order,
        })
        return value

    @http.route(['/shop/cart/update'], type='http', auth="public",
                methods=['POST'], website=True)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        """This route is called when adding a product to cart (no options)."""
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.state != 'draft':
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)

        print(sale_order)
        settings_product_data = request.env['res.config.settings']
        product_bom_data = settings_product_data.search([])
        for rec in product_bom_data:
            # print(rec.product_ids)
            settings_product_ids = rec.product_ids
        # print(settings_product_ids)
        bom_product_data = request.env['mrp.bom']
        bom_records = bom_product_data.search([])
        bom_meterials = []
        for rec in bom_records:
            pass
            # print(rec.product_tmpl_id,int(product_id))
        #     for data in rec.bom_line_ids:
        #         # print(data.product_id.name)
        #         bom_meterials.append(data.product_id.name)
        # print(bom_meterials,product_id)




        product_custom_attribute_values = None
        if kw.get('product_custom_attribute_values'):
            product_custom_attribute_values = json.loads(
                kw.get('product_custom_attribute_values'))

        no_variant_attribute_values = None
        if kw.get('no_variant_attribute_values'):
            no_variant_attribute_values = json.loads(
                kw.get('no_variant_attribute_values'))

        sale_order._cart_update(
            product_id=int(product_id),
            add_qty=add_qty,
            set_qty=set_qty,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values
        )

        if kw.get('express'):
            return request.redirect("/shop/checkout?express=1")

        return request.redirect("/shop/cart")
