
odoo.define('bss_one2many_action.FieldOne2ManyAction', function (require) {
    "use strict";

    var core = require('web.core');
    var FieldOne2Many = core.form_widget_registry.get('one2many');

    var FieldOne2ManyAction = FieldOne2Many.extend({
        init: function() {
            this._super.apply(this, arguments);
            self = this;
            this.x2many_views.list.include({
                do_activate_record: function(index, id) {
                    var context = self.build_context().eval();
                    if (context['on_click_action']) {
                        this.do_button_action(
                            context['on_click_action'], id, function () {});
                    }
                }
            });
        }
    });

    core.form_widget_registry.add('one2many_action', FieldOne2ManyAction);

    return FieldOne2ManyAction;
});
