$(document).ready(function() {
	$("#guide,#note").hide();
	$("input[name=traslado]").datepicker({minDate: "0" , maxDate: '+1M', showAnim: 'slide', dateFormat: 'yy-mm-dd'});
	$(".btn-guide-show").click(function  (event) {
		event.preventDefault();
		$("#note").hide('blind', 600);
		$("#guide").show('blind', 600);
	});
	$(".btn-note-show").click(function  (event) {
		event.preventDefault();
		$("#guide").hide('blind', 600);
		$("#note").show('blind', 600);
	});
	$("select[name=traruc]").click(function(event) {
		event.preventDefault();
		loadTransport(this.value);
		loadConductor(this.value);
	});
	$(".btn-change").click(function (event) {
		$("[name="+this.name+"]").removeAttr("readonly");
	});
	$(".btn-save-guide").click(function (event) {
		//event.preventDefault();
		var pass = false, btn = this;
		$("select").each(function () {
			pass = this.value == "" ? false : true
			return pass;
		});
		if (pass) {
			$().toastmessage("showToast",{
				type: 'confirm',
				sticky: true,
				text: "Desea Generar Guia de Remisión?",
				buttons: [{value:'No'},{value:'Si'}],
				success: function (result) {
					if (result === 'Si') {
						$(btn).button('loading');
						var data= new FormData($("[name=formguide]").get(0));
						$.ajax({
							url: '',
							type: 'POST',
							dataType: 'json',
							data: data,
							cache: false,
							contentType: false,
							processData: false,
							success: function (response) {
								if (response.status) {
									$(btn).button('complete');
									console.log(response);
									$(".nro-guide").html(response.guide);
									$(".btn-gv").val(response.guide);
									$(".mguide").modal("show");
								};
							}
						});
					};
				}
			});
		}else{
			$().toastmessage("showWarningToast","Existe un campo vacio.");
			return pass;
		};
	});
	// btn view report guide referral
	$(".btn-gv").click(function(event) {
		event.preventDefault();
		location.href="/report/"
	});
	////
	var loadTransport = function (ruc) {
		$.getJSON('/json/get/list/transport/'+ruc+'/',function (response) {
			if (response.status) {
				var tmp= "<option value='{{nropla_id}}'>{{nropla_id}} - {{marca}}</option>";
				var $transport= $("select[name=nropla]");
				$transport.empty();
				for (var i in response.list) {
					$transport.append( Mustache.render(tmp, response.list[i] ) );
				};
			};
		});
	};
	var loadConductor = function (ruc) {
		$.getJSON('/json/get/list/conductor/'+ruc+'/',function (response) {
			if (response.status) {
				var tmp= "<option value='{{condni_id}}'>{{conlic}} - {{connom}}</option>";
				var $transport= $("select[name=condni]");
				$transport.empty();
				for (var i in response.list) {
					$transport.append( Mustache.render(tmp, response.list[i] ) );
				};
			};
		});
	};
});