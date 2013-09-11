openerp.duration = function(instance)
{	
	instance.duration.FieldDuration = instance.web.form.FieldChar.extend(
    {
    	template : "FieldDuration",
    	initialize_content: function()
    	{
    		this._super();
    	},
    	
    	render_value: function()
    	{
    		var parser_obj = new instance.web.Model('bss_duration_widget.bss_parser');
    		parser_obj.call('display_value', this.get('value')).then(function(result)
    			{
    				var content = $("div#duration_widget_content");
    				content.empty();
    				content.append("<input type='text' value='" + result + "' />");
    			});
    	}
    });
	    
	instance.web.form.widgets.add('duration', 'instance.duration.FieldDuration');
}