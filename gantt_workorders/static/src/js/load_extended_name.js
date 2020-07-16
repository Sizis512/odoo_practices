odoo.define('gantt_workorders.GanttModel', function (require) {
    "use strict";

    let AbstractModel = require('web.AbstractModel');

    let GanttModel = AbstractModel.extend({

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
                    'long_name',
                    'progress',
                    'parent_id',
                    'color',
                    'user_id',
                ],
            })
                .then(this._processData.bind(this));
        } //else call super
    },
    });
    return GanttModel: GanttModel;
});