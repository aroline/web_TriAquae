//(function(){
if (typeof CommandExecutePage == "undefined")
	CommandExecutePage={};	
	
(function(cmdObj){
	var command = "",remote_path = "",fileLists="";
	var username = "";
	cmdObj.track_mark =0;
	cmdObj.total_tasks =0;
	cmdObj.dangerousCmd = [];
	cmdObj.transfer_action=["SendFile","GetFile"];
	cmdObj.tags = [ "shutdown", "restart", "df", "cat", "du", "top", "iostat" ];	
	cmdObj.executeCommand =function(_command,_username,_computers,remotepath,filelists){
		if(cmdObj.transfer_action.indexOf(_command) != -1){
			command = _command;
			username = _username;
			remote_path = remotepath;
			fileLists = filelists;
		        $.post('/transferFile/', {IPLists:_computers.toString(),UserName:_username,command:_command,FileLists:filelists.toString(),RemotePath:remotepath}, function(data) {
                        	var json_data = JSON.parse(data);
	                        var totalNum = json_data.TotalNum,trackmark=json_data.TrackMark;
        	                cmdObj.total_tasks = parseInt(totalNum);
                	        cmdObj.track_mark = trackmark;
                	});
		
		}
		else{
		        $.post('/runCmd/', {IPLists:_computers.toString(),UserName:_username,command:_command }, function(data) {
                      		var json_data = JSON.parse(data);
	                        var totalNum = json_data.TotalNum,trackmark=json_data.TrackMark;
        	                cmdObj.total_tasks = parseInt(totalNum);
                	        cmdObj.track_mark = trackmark;
                	});
		}
		var updateProgress = cmdObj.InitProgressbar();
		setTimeout(updateProgress,2000);
		$("#stopprocess").attr("disabled",false);	
	};	
		
	cmdObj.stopExecution = function(){
		//alert("stop");//todo
		$.get('/stopExecution/',{TrackMark:cmdObj.track_mark},function(data){
		
		
	});
	};
	cmdObj.popDia = function(command,username,computers,remotepath,filelists) {
	//	var computers = getDatas();
		var timertick =5,diagbody =  $("#dialog_body");
		if(computers.length == 0){
			diagbody.html("Please choose computers first.");
			$( "#dialog-confirm" ).dialog({
				resizable: false,
				height:240,
			//	width:500,
				modal: true,
				buttons: {
					"OK": function() {
							$( this ).dialog( "close" );
					}
				}	
			});
		return;			
		}
		if(command==""||typeof command =="undefined"){
			diagbody.html("You should type valid command first");
			$( "#dialog-confirm" ).dialog({
				resizable: false,
				height:240,
				modal: true,
				buttons: {
					"OK": function() {
							$( this ).dialog( "close" );
					}
				}
					
			});	

		}else{
			if((cmdObj.transfer_action)[0].indexOf(command) != -1 && filelists.length == 0){
        	                          diagbody.html("You should choose files first");
                	                $( "#dialog-confirm" ).dialog({
                        	                resizable: false,
                                	        height:240,
                                        	modal: true,
	                                        buttons: {
        	                                "OK": function() {
                	                                        $( this ).dialog( "close" );
                        	                	}
                               			 }

                               		 });
				return;

                        }
				
			diagbody.html("Execute the command '"+ command+"' in five seconds automatically! 5");
			var timer = setInterval(function(){
				var bodycontent = diagbody.html();
				bodycontent = bodycontent.substr(0,bodycontent.length -1);
				timertick -=1;
				bodycontent += timertick;
						diagbody.html(bodycontent);
				if(timertick==0){
					clearInterval(timer);
					$("#dialog-confirm").dialog("close");
					cmdObj.executeCommand(command,username,computers,remotepath,filelists);
				}
			},1000);
			
			$( "#dialog-confirm" ).dialog({
				resizable: false,
				height:240,
				modal: true,
				buttons: {
					"Execute immediately": function() {
						$( this ).dialog( "close" );
						clearInterval(timer);
						cmdObj.executeCommand(command,username,computers,remotepath,filelists);
					},
					Cancel: function() {
						$( this ).dialog( "close" );
						clearInterval(timer);
					}
				}
			});
		}
	};
	cmdObj.InitProgressbar = function(){
		var progressbar0 = $( "#progressbar" ),progressLabel = $( ".progress-label" );
		progressbar0.css("display","block");
		var mytimer;
//		var totalnum = cmdObj.total_tasks;
		progressbar0.progressbar({
			value: false,
			change: function() {
				progressLabel.text(progressbar0.progressbar("value") + "%" );
			},
			complete: function() {
				progressLabel.text( "Complete!" );
				$("#stopprocess").attr("disabled",true);  
				clearTimeout(mytimer); 
			}
		});
		return(function sendXHR(){
			 $.ajax({
				url: "/cmd_result/",
				data: {"TrackMark": cmdObj.track_mark,"TotalTasks":cmdObj.total_tasks},
				type:"GET",
				async:false,
				timeout:3000,
				success: function( data ) {
					var jsondata = JSON.parse(data);
					var val = progressbar0.progressbar( "value" ) || 0;
					var failnum=0,successnum = 0;
					var htmlstr = "";
					for (var key in jsondata)
					{
						if(key == "result_count")
						{
							successnum = (jsondata[key])[0];
							failnum = (jsondata[key])[1];						
						}else{
							htmlstr += jsondata[key].join();
							htmlstr +="<br />";
						}
					}

					$("#execution_process").html(htmlstr);
					$("#totalnum").html(cmdObj.total_tasks);//.parent().click(cmdObj.showProcessRet);
					$("#failednum").html(failnum);//.parent().click(cmdObj.showFailedLists);
					$("#successnum").html(successnum);				//todoif(failnum)
					mytimer = setTimeout( sendXHR,1000); 
					if(cmdObj.total_tasks != 0) 
						progressbar0.progressbar("value",parseInt((failnum + successnum)/cmdObj.total_tasks * 100));
				},
				error:function(XMLHttpRequest,textStatus,errorThrown){
					clearTimeout(mytimer);
				}                       
			});
		}); 
	};
	cmdObj.showFailedLists = function(){
		$.get("/getFailedLists/",{TrackMark:cmdObj.track_mark},function(data){
			var lists = JSON.parse(data);
				
			var len = lists.length;
			var ulele = $("<ul></ul>");
			for(var i=0;i<len;i++)
			{
				var li_checkbox=$("<li><input type='checkbox' name='failedip' value ='"+lists[i]+"'/> "+lists[i]+" </li>");
				ulele.append(li_checkbox);
			}
			var allchecked =$("<input type='button' id='selectall' value='select all'/>");
			var reAct = $("<input type='button' id='reActCmd' value='Re-Execute The Command'/>");
				
			$("#execution_failed").html("").append(ulele).append(allchecked).append(reAct).css("display","block");	
			$("#selectall").click(cmdObj.selectAll);
			$("#execution_process").css("display","none");
			$("#reActCmd").click(function(){
				var machine = [];
				$("input:checked").each(function(i,n){
					machine.push($(this).val());
				});	
				cmdObj.popDia(command,username,machine,remote_path,fileLists);
			});
		});

	};
	cmdObj.showProcessRet = function(){
		$("#execution_process").css("display","block");
		$("#execution_failed").css("display","none");
	
	
	};
	cmdObj.selectAll = function(){
		$("#execution_failed input[type='checkbox']").each(function(ele){
			$(this).attr("checked",true);
		});
	
	};
	//value lists should be an array containing keys
	cmdObj.makeOptions = function(valueLists){
		var optionHtml="";
		$.each(valueLists,function(i,n){
			var opt = "<option value='"
				+ valueLists[i] 
				+ "'>"
				+ valueLists[i]
				+"</option>";
			
			optionHtml += opt;			
		});
		return optionHtml;
	};
	cmdObj.fileLists = [];
	//return an array containing all the option value
	cmdObj.getOptions = function(selectId){
		var selectEle = $("#"+selectId);
		var optionValues=[];
		$("#"+selectId+" option").each(function(i,n){
			optionValues.push($(this).attr("value"));
		});
		return optionValues;
	};
	 $("#totalnum").parent().click(cmdObj.showProcessRet);
         $("#failednum").parent().click(cmdObj.showFailedLists);
	$.get("/getDangerousCmd/",function(data){
		cmdObj.dangerousCmd = JSON.parse(data);

	});	
})(CommandExecutePage);

