
#!/usr/bin/env python


LogLevel = {
        'info': {
                'action': ['console_pop_up'], 
        	},
        
        'warning': {
		'action': ['console_pop_up','email'],
		},
		
	}


Format = {

	'simple' : {
		'text' : "%s: %s  error happend!" ,#%(event_level,event_content),
	    'apply_to' : ['console_pop_up','sms'] ,
		
		   },

	'detail' : {	
		'text' : '''
			 <html>
			  <head></head>
			  <body>
    				<p>Hi!<br>
       					How are you?<br>
       					Here is the <a href="http://www.python.org">link</a> you wanted.
   				 </p>
  			</body>
			</html> ''' ,

    	    'apply_to' : ['email'],

		}	
}
