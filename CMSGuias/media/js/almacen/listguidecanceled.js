$(document).ready(function() {
	$("input[name=dates]").datepicker({ showAnim: "slide", dateFormat: "yy-mm-dd"});
	$(".btn-show-gv").click(function (event) {
		event.preventDefault();
		$(".btn-gv").val(this.value);
		$(".mview").modal("show");
	});
	$(".btn-gv").click(function (event) {
		event.preventDefault();
		url= "/reports/guidereferral/"+this.value+"/"+this.name+"/";
		window.open(url,"_blank");
	});
	$("input[name=search]").change(function () {
		$("input[name=search]").each(function () {
			if (this.checked) {
				$("input[name="+this.value+"]").attr('disabled', false);
			}else{
				$("input[name="+this.value+"]").attr('disabled', true);
			};
		});
	});
	$(".btn-search").click(function (event) {
		event.preventDefault();
		searchGuide();
	});
	// search guide referral
	var searchGuide = function () {
		// variables
		var input=null,data={};
		$("input[name=search]").each(function () {
			if (this.checked) {
				input= this.value;
			};
		});
		if (input!=null) {
			data['tra']= input;
			$("input[name="+input+"]").each(function () {
				data[this.id]= $.trim(this.value) == "" ? "" : this.value;
			});
			$.getJSON("",data,function (response) {
				if (response.status) {
					var $tb = $("tbody"),
							temp= "<tr class='success tr{{guia_id}}'><td class='text-center'>{{item}}</td><td class='text-center'>{{guia_id}}</td><td>{{nompro}}</td><td>{{traslado}}</td><td>{{connom}}</td><td class='text-center'><button class='btn btn-link btn-sm text-black btn-show-gv' onClick='view(this);' value='{{guia_id}}'><span class='glyphicon glyphicon-paperclip'></span></button></td><td class='text-center'><button class='btn btn-link btn-sm text-black'  onclick='show_annular(this);' value='{{guia_id}}'><span class='glyphicon glyphicon-fire'></span></button></td></tr>";
					$tb.empty();
					for (var i in response.list) {
						$tb.append( Mustache.render(temp, response.list[i]) );
					};
				};
			});
		}else{
			$().toastmessage("showWarningToast","Los campos se encuentrán vacios.");
		};
	};
});
var view= function (tag) {
	$(".btn-gv").val(tag.value);
	$(".mview").modal("show");
}