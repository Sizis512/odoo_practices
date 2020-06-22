odoo.define('product_import_images.import_button', function (require) {
"use strict";

var core = require('web.core');
var ListController = require('web.ListController');
var KanbanController = require('web.KanbanController');
var rpc = require('web.rpc');
var session = require('web.session');
var _t = core._t;

var includeDict = {
    renderButtons: function($node) {
    this._super.apply(this, arguments);
        if (this.$buttons) {
            this.$buttons.find('.oe_import_image_button')
                         .click(this.proxy('action_def'));
        }
    },

    action_def: function () {
        var user = session.uid;
        rpc.query({
                model: 'product.import.images',
                method: 'get_view',
                });

/*
        var model_obj = new instance.web.Model('ir.model.data');
        var view_id = false;
        model_obj.call('get_object_reference',
                       ['product.import.image',
                       'Import Product Images'])
                       .then( function(result){
                               view_id = result[1];
                       });

        this.do_action({
            views: [[view_id, 'form']],
        });
*/
    },
};

ListController.include(includeDict);
KanbanController.include(includeDict);

});