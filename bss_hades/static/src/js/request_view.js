openerp.bss_hades = function(instance) {

    instance.bss_hades.FieldRequestView = instance.web.form.FieldChar.extend({
        template : "FieldRequestView",
        
        initialize_content: function() {
            this._super();
            
        },
        
        render_value: function() {
        	var field = this
        	//$('.oe_view_manager_header').css('display', 'none')
        	$('.oe_view_manager_sidebar').css('display', 'none')
        	
        	var request_id = this.get('value');
        	var request_obj = new instance.web.Model('request.data');
        	request_obj.call('get_datas', [request_id]).then(function (result) {
        		var content = $('div#request_view_content');
        		content.empty();
            	
            	if(result.datas.length == 0) {
            		html = "<p class=\"no-data\">No data found matching the current query and parameters</p>";
            	} else {
	            	var headerline = "<tr>";
	            	for(var i in result.headers) {
	            		headerline += "<th>" + result.headers[i] + "</th>";
	            	}
	            	headerline += "</tr>";
	            	
	            	var bodylines = "";
	            	for(var i in result.datas) {
	            		bodylines += "<tr>";
	            		for(var j in result.headers) {
	            			bodylines += "<td>" + result.datas[i][result.headers[j]] + "</td>";
	            		}
	            		bodylines += "</tr>";
	            	}
            	
            		html = "<table>" + headerline + bodylines + "</table>";
            	}
            	
            	content.append(html);
            	
            	$('#request_view_content td').filter(function() {
					return this.innerHTML.match(/^[0-9\s\.,]+$/);
				}).addClass('numeric');
				
				$('#request_view_content td').filter(function() {
					return this.innerHTML.match(/^null$/);
				}).empty();
				
				$('#request_view_content td').filter(function() {
					return this.innerHTML.match(/^(true|false)$/);
				}).css('text-transform', 'capitalize');
            });
        }
    });
    
    instance.web.form.widgets.add('bss_hades_request_view', 'instance.bss_hades.FieldRequestView');
}
