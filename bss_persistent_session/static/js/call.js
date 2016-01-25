openerp.bss_persistent_session = function(instance) {
    $(document).ready(function(){
        // For following lines, consider time unit as ms. 
        var P = new instance.web.Model('ir.config_parameter');
        var parentDelay = 0;
        var sessionCallback = function(){
            P.call('get_param', ['bss_persistent_session.delay']).then(function(delay){
                if(parentDelay != delay) {
                    clearInterval(sessionback);
                    parentDelay = delay;
                    sessionback = setInterval(sessionCallback, delay);
                    }
                }, function(){ clearInterval(sessionback); parentDelay = 90000; });
            };
            sessionback = setInterval(sessionCallback,parentDelay);
    });
};
