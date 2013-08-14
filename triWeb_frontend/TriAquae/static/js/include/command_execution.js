$(function(){
	$.get('/AllCommands/',function(data){
		CommandExecutePage.tags = data.split('\n');
		$( "#appendedDropdownButton" ).autocomplete({
			source: function( request, response ) {
				  var matcher = new RegExp( "^" + $.ui.autocomplete.escapeRegex( request.term ), "i" );
				  response( $.grep(CommandExecutePage.tags, function( item ){
					  return matcher.test( item );
				  }) );
			  },
			minLength: 2,
			select: function( event, ui ) {
			//	log( ui.item ?
			//	"Selected: " + ui.item.label : "Nothing selected, input was " + this.value);
			},
			open: function() {
					$( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
			},
			close: function() {
					$( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
			}
		});
	});

	$.get('/AllUsers/',function(data){
		var usrCount =JSON.parse(data);
		for(var i=0;i<usrCount.length;i++)
		{
			var listEle = $("<li></li>");
			listEle.data("UserName",usrCount[i]);
			listEle.html("Run as "+usrCount[i]);
			$("#invokeOperation").append(listEle);
		}
	});

	$("#stopprocess").click(CommandExecutePage.stopExecution);
	$("#invokeOperation").delegate("li","click",function(){
		var usr = $(this).data("UserName");
		var computers = getDatas();
		CommandExecutePage.popDia($('#appendedDropdownButton').val(),usr,computers);
	});
	 $("#appendedDropdownButton").keyup(function(){
		var _val = $(this).val();
		if(CommandExecutePage.dangerousCmd.indexOf(_val) != -1)
			$(".alert").css("display","block").alert("close");
			
	});
});



