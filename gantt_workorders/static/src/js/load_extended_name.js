odoo.define('gantt_workorders.custom_feature', function (require) {
    "use strict";

    let GanttModel = require('ba_web_gantt.GanttModel');

    GanttModel.include({

        //same as super but if in workorder takes 'display_name' too
        _loadTasks: function () {
            if (this.modelName == 'mrp.workorder'){
                return this._rpc({
                    model: this.modelName,
                    method: 'search_read',
                    context: this.chart.context,
                    domain: this.chart.domain,
                    fields: [
                        this.chart.start_date,
                        this.chart.stop_date,
                        'name',
                        'display_name',
                        'progress',
                        'parent_id',
                        'color',
                        'user_id'
                    ],
                })
                    .then(this._processData.bind(this));
            } else {
                return this._super();
            }
        },

        //same as super but if in workorder uses 'display_name' instead of 'name'
        _processData: function (raw_data) {
            var self = this;
            self._super(raw_data);
            if (self.modelName == 'mrp.workorder') {
                self.chart.data.forEach(function (data, i) {
                    var id = Number(data.id);
                    var raw = raw_data.find(function(element) {return element.id === id;});
                    data.name = raw.display_name;
                });
            }
        },
    });
});