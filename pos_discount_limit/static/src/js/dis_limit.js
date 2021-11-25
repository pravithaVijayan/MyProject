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
                var category = this.get_product().pos_categ_id[0]
                var non_discount_category = this.pos.config.non_discount_categ_ids
                var flag = false
//                console.log(category)
                for (var categ in non_discount_category){
//                console.log(category,non_discount_category[categ])
                    if (category == non_discount_category[categ]){
                        flag = true
                    }
                }
//                console.log(flag)
                if(flag == false){
                    var parsed_discount = isNaN(parseFloat(discount)) ? 0 : field_utils.parse.float('' + discount);
                    var disc = Math.min(Math.max(parsed_discount || 0, 0),100);
                    this.discount = disc;
                    var old_discountStr = this.discountStr
                    this.discountStr = '' + disc;
                    if (this.discountStr < this.pos.config.discount_limit){
                       this.trigger('change',this);
            //           console.log(this.discountStr)
                       console.log("pos",this.get_product().pos_categ_id[0])
                       console.log("category",this.pos.config.non_discount_categ_ids)
                    }
                    else{
                        this.discountStr = old_discountStr
                        this.discount = old_discountStr
                        alert("Discount Limit Exceeded")
                    }
                }
                else{
                    alert("Discount Not Allowed for this Product Category")
                    flag = false
                }
            }


        });

});
