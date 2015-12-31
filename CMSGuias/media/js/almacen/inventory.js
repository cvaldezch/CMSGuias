$(document).ready(function() {
	$(".opad").hide();
	$(document).on('keyup',"input[name=cod],input[name=desc]" , keyUpInput);
	$(document).on("click",".btn-add-supply", addsupply);
	$(".btn-register-all-list").on('click',register_all_list);
	$(document).on("change", "input[name=nper]", changeperiod);
	$(".btn-list-period").on("click", register_period_pased);
	$(".stkmin").on("change", chkmin);
	$("button[name=btn-opad]").click(function(event) {
		$(".opad").toggle("blind", 600);
	});
	$(".btn-stmp-supply").on("click", save_tmp_supply);
	$("#bdelAllInv").on("click", bdelallitem);
	$("#bupall").on("click", function (){
		$("#ufile").modal("show");
	});
	$(".upfile").on("click", uploadFile);
});

var bdelallitem = function (event){
	swal({
		title: "Eliminar todo el inventario?",
		text: "realmente desea eliminar todo el inventario?",
		type: "warning",
		showCancelButton: true,
		confirmButtonText: "Si!",
		confirmButtonColor: "#DD6B55",
		cancelButtonText: "No"
	}, function (isConfirm) {
		console.log(event);
		if (isConfirm) {
			event.currentTarget.disabled = true;
			event.currentTarget.innerHTML = "<i class=\"fa fa-spinner fa-pulse\"></i> Procesando";
			data = {"delInventory": true, "csrfmiddlewaretoken": $("[name=csrfmiddlewaretoken]").val()}
			$.post("", data, function (response){
				if (response.status) {
					location.reload();
				}else{
					event.currentTarget.disabled = false;
					event.currentTarget.innerHTML = "<i class=\"fa fa-fire\"></i> Eliminar Todo";
				};
			}, "json");
		};
	});
}

var uploadFile = function (event){
	event.currentTarget.disabled = true;
	event.currentTarget.innerHTML = "<i class=\"fa fa-spinner fa-pulse\"></i> Procesando";
	data = new FormData();
	data.append("csrfmiddlewaretoken", $("[name=csrfmiddlewaretoken]").val())
	data.append("uploadInventory", true);
	data.append("inventory", $("#afile")[0].files[0]);
	$.ajax({
		url: "",
		data: data,
		dataType: "json",
		type: "post",
		processData: false,
		contentType: false,
		cache: false,
		success: function (response){
			if (response.status) {
				location.reload();
			}else{
				event.currentTarget.disabled = false;
				event.currentTarget.innerHTML = "<i class=\"fa fa-upload\"></i> Cargar";
			};
		}
	});
}

// functions
var save_tmp_supply = function (event) {
	event.preventDefault();
	var data = new Object(), pass = false;
	$(".add-id, .add-cant").each(function () {
		if (this.value != "") {
			data[this.name] = this.value;
			pass = true;
		}else{
			$().toastmessage("showWarningToast","Se a encontrado un campo vacio.");
			this.focus();
			return false;
			pass = false;
		};
	});
	if (pass) {
		data.tipo = 'save-tmp';
		data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
		data['add-ori'] = "AL";
		data['add-oid'] = $("select[name=almacen]").val();
		//data['add-al'] = $("select[name=almacen]").val();
		console.info(data);
		$.post("", data, function (response) {
			if (response.status) {
				$("button[name=btn-"+data['add-id']+"]").attr('disabled', true);
				$().toastmessage("showNoticeToast","Se agrego a Temp Suministro, correctamente.");
				$(".add-id").val("");
				$(".maddsupply").modal("hide");
			}else{
				$().toastmessage("showErrorToast","He fallado! en mi misión.")
			};
		}, "json");
	};
}
var addsupply = function (event) {
	event.preventDefault();
	$(".add-id").val(this.value);
	$(".maddsupply").modal("show");
}
var changeperiod = function (event) {
	event.preventDefault();
	$("select[name=periodo]").attr("disabled", this.value == "now" ? true : false);
}
var chkmin = function (event) {
	event.preventDefault();
	$("[name=smin]").attr("disabled", !this.checked);
}
var keyUpInput = function (event) {
	event.preventDefault();
	var key = (event.keyCode ? event.keyCode : event.which);
	if (key == 13) {
		search(this,1);
	};
}
var search = function (ctrl,page) {
	var data = new Object();
	// recover data for search data
	data['periodo'] = $("select[name=periodo]").val(); // get value periodo
	data['almacen'] = $("select[name=almacen]").val(); // get value almacen
	data['omat'] = ctrl.value;
	data['tipo'] = ctrl.name;
	data['stkzero'] = $(".stkzero").is(":checked") ? 1 : 0;
	data['stkmin'] = $(".stkmin").is(":checked") ? $("[name=smin]").val() : 'None';
	data['page'] = page;
	$.get('',data,function (response) {
		var $tbody = $("tbody");
		var template = "<tr class='{{status}}'><td>{{ item }}</td>"+
									"<td>{{ materiales_id }}</td>"+
									"<td>{{ matnom }}</td>"+
									"<td>{{ matmed }}</td>"+
									"<td>{{ unid }}</td>"+
									"<td>{{ stkmin }}</td>"+
									"<td>{{ stock }}</td>"+
									"<td>{{ ingreso }}</td>"+
									"<td>{{ compra_id }}</td>"+
									"<td><button value='{{ materiales_id }}'' class='btn btn-xs btn-warning btn-add-supply text-black' {{ dis }}><span class='glyphicon glyphicon-plus'></span><span class='glyphicon glyphicon-shopping-cart'></span></button></td></tr>";
		$tbody.empty();
		for (var x in response.list) {
			response.list[x].status = response.list[x].stock <= 0 ? 'danger' : response.list[x].stock >= response.list[x].stkmin ? 'success' : 'warning'
			response.list[x].item = (parseInt(x) + 1);
			response.list[x].dis = response.list[x].spptag ? 'disabled' : '';
			$tbody.append(Mustache.render(template, response.list[x]));
		};
		var tmpnav = "";
		if (response['has_previous']) {
			tmpnav += "<li><a href=javascript:search_page('"+ctrl.name+"',1);>&laquo;</a><li>"+
								"<li><a href=javascript:search_page('"+ctrl.name+"',"+response['previous_page_number']+");>Anterior</a></li>";
		};
		tmpnav += " <li> Page "+response['number']+" of "+response['num_pages']+" <li> ";
		if (response['has_next']) {
			tmpnav += "<li><a href=javascript:search_page('"+ctrl.name+"',"+response['next_page_number']+");>Siguiente</a></li>"+
								"<li><a href=javascript:search_page('"+ctrl.name+"',"+response['num_pages']+");>&raquo;</a><li>";
		};
		var $nav = $(".pager");
		$nav.empty();
		$nav.append(tmpnav);
	});
}
var search_page = function (name,page) {
	console.log(name);
	console.info($("[name="+name+"]").get(0));
	var $ctrl = $("[name="+name+"]").get(0);
	console.warn($ctrl);
	search($ctrl,page);
}
var register_all_list = function () {
	var data = new Object();
	data['alid'] = $("select[name=almacen]").val();
	data['quantity'] = parseInt($("input[name=ias]").val());
	data['csrfmiddlewaretoken'] = $("input[name=csrfmiddlewaretoken]").val();
	data['tipo'] = 'all';
	$.post('',data, function (response) {
		console.info(response);
		if (response.status) {
			location.reload();
		};
	},'json');
}
var register_period_pased = function () {
	var data = new Object();
	data['alcp'] = $("select[name=alcp]").val();
	data['pewh'] = $("select[name=pewh]").val();
	data['alwh'] = $("select[name=alwh]").val();
	data['csrfmiddlewaretoken'] = $("input[name=csrfmiddlewaretoken]").val();
	data['tipo'] = 'per';
	console.log(data);
	$.post("", data, function (response) {
		console.log(response);
			location.reload();
	},"json");
}