odoo.define('website_bom_in_cart.cart', function (require) {
'use strict';

    var publicWidget = require('web.public.widget');
    var cart = require('website_sale.cart');


    publicWidget.registry.websiteSaleCartLink = publicWidget.Widget.extend({
//        selector: '#top_menu a[href$="/shop/cart"]',
        selector: '.oe_website_sale',
        events: {
    //        'mouseenter': '_onMouseEnter',
    //        'mouseleave': '_onMouseLeave',
            'click .add_to_cart': '_onClickAlert',
        },
        _onClickAlert: function (ev) {
            alert("hiiiiiiiiiiiiiii")
        }
    });
});