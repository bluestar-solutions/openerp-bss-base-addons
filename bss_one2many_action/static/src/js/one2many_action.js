
odoo.define('bss_one2many_action.FieldOne2ManyAction', function (require) {
    "use strict";

    var core = require('web.core');
    var FieldOne2Many = core.form_widget_registry.get('one2many');

    var FieldOne2ManyAction = FieldOne2Many.extend({
        _actions: {},
        init: function() {
            this._super.apply(this, arguments);
            var context = this.build_context().eval();
            this._actions[this.name] = context['on_click_action'];
            self = this;
            this.x2many_views.list.include({
                do_activate_record: function(index, id) {
                    if (self._actions[this.x2m.name]) {
                        this.do_button_action(
                            self._actions[this.x2m.name], id, function () {});
                    }
                }
            });
        }
    });

    core.form_widget_registry.add('one2many_action', FieldOne2ManyAction);

    return FieldOne2ManyAction;
});
