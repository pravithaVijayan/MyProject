odoo.define('pos_discount_limit.receipt', function(require){
    "use strict";
    var models = require('point_of_sale.models');
    var field_utils = require('web.field_utils');
    var config = require('web.config');
//    var models = require('point_of_sale.screens');
    models.load_fields('pos.config', 'discount_limit');

    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({

        set_discount: function(discount) {
        var parsed_discount = isNaN(parseFloat(discount)) ? 0 : field_utils.parse.float('' + discount);
        var disc = Math.min(Math.max(parsed_discount || 0, 0),100);
        this.discount = disc;
        var old_discountStr = this.discountStr
        this.discountStr = '' + disc;
        if (this.discountStr < this.pos.config.discount_limit){
           this.trigger('change',this);
           console.log(this.discountStr)
           console.log(this.pos.config.discount_limit)
        }
        else{
        this.discountStr = old_discountStr
        alert("Discount Limit Exceeded")
        }
        },
        });

});
