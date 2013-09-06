openerp.resource = function(openerp)
{
	openerp.web.form.add('duration','openerp.resource.duration_widget');
	openerp.resource.duration_widget = openerp.web.form.FieldChar.extend(
	{
		template:'duration',
		init: function(view, code)
			{
				this._super(view,code);
			}
	});
}