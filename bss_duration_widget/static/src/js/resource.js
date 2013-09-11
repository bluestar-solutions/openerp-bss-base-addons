openerp.resource = function(instance)
{
	console.log("Module loaded");
	
	openerp.web.form.widgets.add('duration', 'openerp.resource.duration_widget');
	openerp.resource.duration_widget = openerp.web.form.FieldChar.extend(
	    {
	    	template : "duration",
	    	init: function (view, code)
	    	{
	    		this._super(view, code);
	        	console.log('loading...');
	    	},
	    	render_value: function()
	    	{
	    		var parser_obj = new instance.web.Model('bss_duration_widget.bss_parser');
	    		parser_obj.call('display_value', this.get('value')).then(function(result)
	    			{
	    				var content = $("div#duration_widget_content");
	    				content.empty();
	    				content.html("<input type='text' value='" + result + "' />");
	    			});
	    	}
	    });
}