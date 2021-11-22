odoo.define('pos_product_details.product_description', function (require) {
  "use strict";
  var models = require('point_of_sale.models');
  var _super_orderline = models.Orderline.prototype;
  models.load_fields('product.product', 'product_description');
  models.Orderline = models.Orderline.extend({
        initialize: function(attr, options) {
            var line = _super_orderline.initialize.apply(this,arguments);
            this.product_description= this.product.product_description;
//            console.log("orderline :",this.product_description)
        }
  })

});