$(document).ready(function() {
	$("[name=fi-su],[name=ff-su]").datepicker({ showAnim : "slide", dateFormat : "yy-mm-dd" });
	$("[name=id-su],[name=fi-su],[name=ff-su]").attr('disabled', true);
	$("[name=rdo]").on("change", changeRadio);
	$(".btn-proccess").hover(
		function () {
			$(".btn-proccess").find('span').toggleClass("glyphicon-unchecked").addClass("glyphicon-check");
		}
	);
	$(".btn-proccess").on("click", showStatus);
	$(".btn-rpt").on("click", viewReport);
	$(".btn-status").on("click", changeStatus);
});

// functions
var viewReport = function (event) {
	event.preventDefault();
	url = "/reports/supply/".concat($(".nro-su").html()+"/");
	window.open(url, "_blank");
}
var showStatus	= function (event) {
	event.preventDefault();
	$(".nro-su").html(this.name);
	$(".msupply").modal("show");
}
var changeStatus = function (event) {
	event.preventDefault();
	var data = new Object(), $nro = $(".nro-su");
	if ($nro.html() != "" ) {
		data['id-su'] = $nro.html();
		data['csrfmiddlewaretoken'] = $("input[name=csrfmiddlewaretoken]").val();
		data['status'] = this.value;
		$.post('', data, function(response) {
			if (response.status) {
				if (response.type == 'approve') {
					$().toastmessage("showToast",
					{
						text : 'Muy bien Desea cotizar esta Orden de Suminsitro?',
						type : 'confirm',
						buttons : [{value:'Si'},{value:'No'}],
						sticky: true,
						success: function (result) {
							if (result == 'Si') {
								location.href='/logistics/supply/to/convert/#'.concat($nro.html());
							}else{
								location.reload();
							};
						}
					}
					);
				}else{
					location.reload();
				};
			};
		});
	}else{
		$().toastmessage("showWarningToast", "No se a encontrado id Suministro.");
	};
}

var changeRadio = function (event) {
	event.preventDefault();
	if (this.checked) {
		if (this.value == "code") {
			$("[name=id-su]").attr("disabled",false);
			$("[name=fi-su],[name=ff-su]").attr("disabled",true);
		}else if(this.value == "date"){
			$("[name=fi-su],[name=ff-su]").attr("disabled",false);
			$("[name=id-su]").attr('disabled',true);
		};
	};
}