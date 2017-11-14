
odoo.define('bss_one2many_action.FieldOne2ManyAction', function (require) {
    "use strict";

    var core = require('web.core');
    var FieldOne2Many = core.form_widget_registry.get('one2many');

    /**
     * Create a FieldOne2ManyAction, based on FieldOne2Many.
     * extend() of Odoo Class will call extend() function of underscore
     * library but with create a new object before. Then FieldOne2Many
     * is not affected.
     */
    var FieldOne2ManyAction = FieldOne2Many.extend({
        _actions: {},
        init: function() {
            this._super.apply(this, arguments);
            var context = this.build_context().eval();
            this._actions[this.name] = context['on_click_action'];
            self = this;
            this.x2many_views.list.include({
                do_activate_record: function(index, id) {
                    // x2many_views is a reference shared by all x2m
                    // components, then we have to check if the
                    // event is from a one2many_action, otherwise
                    // calling super to not affect other component
                    // if there is many x2m components on the same view.
                    if (this.x2m.widget == 'one2many_action') {
                        if (self._actions[this.x2m.name]) {
                            this.do_button_action(
                                self._actions[this.x2m.name], id,
                                function () {});
                        }
                    } else {
                        this._super(index, id);
                    }
                }
            });
        }
    });

    core.form_widget_registry.add('one2many_action', FieldOne2ManyAction);

    return FieldOne2ManyAction;
});
