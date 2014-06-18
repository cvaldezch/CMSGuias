$(document).ready(function() {
	$(".panel-quote,.panel-buy,.table-details").hide();
	$(".btn-proccess").on("click", showConvert);
	$("[name=transfer_buy],[name=traslado_quote]").datepicker({ dateFormat: "yy-mm-dd", showAnim: "slide" });
	$("[name=obser_quote]").focusin(function () {
		this.setAttribute("rows",3);
	}).focusout(function () {
		this.setAttribute("rows",1);
	});
	$(".conquote,.conbuy").on("click", selectConvert);
	$("[name=select]").on("change", changeRadio);
	$(".btn-new").on("click", newDocument);
	$(".btn-clean").on("click", cleanControls);
	$(document).on("change", "input[name=chk]",changeCheck);
	$(".btn-save").on("click", savedDocument);
	$(".btn-finish").on("click", terminateSupply);
});

// functions
var terminateSupply = function (event) {
	event.preventDefault();
	$().toastmessage("showToast",{
		type: 'confirm',
		sticky: true,
		text: 'Parece que has terminada de cotizar o compar, Deseas terminar con la order de suministro?',
		buttons: [{value:'No'},{value:'Si'}],
		success: function(res) {
			if (res == 'Si') {
				var data = new Object();
				data['csrfmiddlewaretoken'] = $("[name=csrfmiddlewaretoken]").val();
				data['supply'] = $("[name=supply]").val();
				data['type'] = "finish";
				$.post('', data, function(response) {
					console.log(response);
					if (response.status) {
						$().toastmessage("showNoticeToast","Bien, se a completado el suministro <b>Nro "+data.supply+".</b>");
						setTimeout(function() {
							location.href="/logistics/"
						}, 3000);
					};
				}, "json");
			};
		}
	});
}
var savedDocument = function (event) {
	event.preventDefault();
	// validate data
	var pass = false, counter = 0, btn = this, data = new Object(), arr = new Array();
	// first check whether the selected materials, at least one
	$("input[name=chk]").each(function () {
		if (this.checked) {
			counter += 1;
			arr.push({ mid: this.id, cant: this.value });
		};
	});
	if (counter > 0) {
		// validate header data
		$(".panel-"+btn.value).find("select,input,textarea").each(function () {
			if ($(this).is("textarea")) {
				data[this.name.replace("_".concat(btn.value),"")] = this.value;
				return true;
			};
			if ($.trim(this.value) != "") {
				var name = this.name.replace("_".concat(btn.value),"");
				if ( name == "traslado" ) {
					if (!validateFormatDate(this.value)) {
						$().toastmessage("showWarningToast","Campo \"Fecha\" no valido.");
						pass = false;
						return pass;
					};
				};
				data[name] = this.value;
				pass = true;
			}else{
				$().toastmessage("showWarningToast", "Existe un campo vacio o no se a seleccionado, revise los campos.");
				pass = false;
				return false;
			};
		});
		if (pass) {
			$().toastmessage("showToast", {
				type: "confirm",
				sticky: true,
				text: "Desea Generar la cotización para ".concat($("[name=supplier_"+btn.value+"]").html()),
				buttons: [{value:'Si'},{value:'No'}],
				success: function (result) {
					if (result == "Si") {
						data['newid'] = $.trim($("[name=nro-"+btn.value+"]").val()) != "" ? "0" : "1"
						if (data.newid == "0") {
							data['id'] = $("[name=nro-"+btn.value+"]").val();
						};
						data['mats'] = JSON.stringify(arr);
						data['type'] = btn.value;
						data['supply'] = $("[name=supply]").val();
						data['csrfmiddlewaretoken'] = $("[name=csrfmiddlewaretoken]").val();
						console.log(data);
						$.post("", data, function(response) {
							console.info(response);
							if (response.status) {
								$("[name=nro-"+btn.value+"]").val(response.id);
								$().toastmessage("showNoticeToast","Se ha guardado Correctamente. <br > <strong> Nro "+ response.id+".</strong><br> para el proveedor <strong>"+$("[name=supplier_"+btn.value+"]").val()+"</strong>");
								$(".btn-new").click();
							}else{
								$().toastmessage("showErrorToast","Error: Not proccess <q>Transaction</q>.");
							};
						}, "json");
					};
				}
			});
		};
	}else{
		$().toastmessage("showWarningToast","Debe seleccionar por lo menos un material.");
	};
}

var changeCheck = function (event) {
	event.preventDefault();
	var counter = 0, recount = 0;
	$("[name=chk]").each(function () {
		if (!this.checked){
			$("input[name=select]").attr("checked", false);
			recount += 1;
			//return false;
		}else{
			counter += 1;
		}
	});
	//console.log("re "+recount+" co "+counter);
	if (recount == $("input[name=chk]").length) {
		$("input[name=select]").each(function () {
			if (this.value == 0) {
				this.checked = true;
			};
		});
	} else if (counter == $("input[name=chk]").length) {
		$("input[name=select]").each(function () {
			if (this.value == 1) {
				this.checked = true;
			};
		});
	};
}
var cleanControls = function (event) {
	event.preventDefault();
	$(".panel-"+this.value).find('input,select,textarea').each(function () {
		if ($(this).is("select")) {
			this.selectedIndex = 0;
		}else{
			this.value = "";
		};
	});
}
var newDocument = function (event) {
	var sts = Boolean($(this).attr("status"));
	if (!sts) {
		$(this).text(" Cancelar").attr("status", "new");
		$("<span></span>").prependTo(this);
		$(".btn-new > span").removeClass("glyphicon-file").addClass("glyphicon-remove");
	}else{
		$(this).text(" Nuevo").removeAttr("status");
		$("<span></span>").prependTo(this);
		$(".btn-new > span").addClass("glyphicon-file").removeClass("glyphicon-remove");
	};
	$(".btn-new > span").addClass("glyphicon");
	$(".panel-"+this.value).find( !sts ? ':disabled' : 'input,select,textarea,.btn-clean,.btn-save').each(function () {
		$(this).attr('disabled', sts);
	});
}
var changeRadio = function (event) {
	event.preventDefault();
	if (this.checked) {
		var value = parseInt(this.value);
		$("input[name=chk]").each(function () {
			this.checked = Boolean(value);
		});
	};
}
var getlistMateriales = function (id_su) {
	if (id_su != "") {
		url = "/json/get/details/supply/".concat(id_su).concat("/");
		$.getJSON(url, function(response) {
			console.info(response);
				if (response.status) {
					var $tb = $(".table-details > tbody");
					$tb.empty();
					var template = "<tr><td>{{ counter }}</td><td><input type='checkbox' name='chk' id='{{ materiales_id }}' value='{{ cantidad }}'></td><td>{{ materiales_id }}</td><td>{{ materiales__matnom }}</td><td>{{ materiales__matmed }}</td><td>{{ materiales__unidades_id }}</td><td>{{ cantidad }}</td></tr>";
					for(var x in response.list){
						response.list[x].counter = (parseInt(x) + 1);
						$tb.append(Mustache.render(template, response.list[x]));
					}
				};
		});
	}else{
		$().toastmessage("showWaringToast","Hay un error al traer la lista de materiales. Código incorrecto");
	};
}
var showConvert = function(event) {
	event.preventDefault();
	$(".conquote,.conbuy").val(this.name).attr({
		placeholder: $(this).attr("placeholder"),
		data: $(this).attr("data")
	});
	$(".consu").html(this.name);
	$(".mquestion").modal("show");
	$("input[name=supply]").val(this.name);
};
var selectConvert = function (event) {
	event.preventDefault();
	// recover list of materials
	$(".table-principal").hide("blind", 600);
	getlistMateriales(this.value);
	if (this.title == "quote") {
		$(".panel-quote").show("slide", 600);
		$("[name=traslado_quote]").val($(this).attr("placeholder"));
		$("[name=storage_quote]").val($(this).attr("data"));
	}else{
		$(".panel-buy").show("slide",600);
		$("[name=transfer_buy]").val($(this).attr("placeholder"));
		$("[name=storage_buy]").val($(this).attr("data"));
	};
	$(".table-details").show("slide",600);
	$(".mquestion").modal("hide");
};