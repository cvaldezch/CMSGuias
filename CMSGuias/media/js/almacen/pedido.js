// load funtions of page
$(function () {
	$('.description, .block-add-mat').hide();
	$('.in-date').datepicker({ "minDate": "0", maxDate: "+2M", changeMonth: true, changeYear: true, showAnim:"slide", dateFormat: "yy-mm-dd"});
	$('.matnom').keypress(function (event) {
		var key = ( event.keyCode ? event.keyCode : event.which );
		if ( key != 13 ) {
			//event.preventDefault();
			getdescription(this.value.trim().toLowerCase());
		};
	});
	// get back list of materials
	var getdescription = function (name) {
		$.getJSON('/json/get/materials/name/', {'nom': name }, function (response) {
			var template = "<li id='li{{id}}' onClick=getidli(this);><a class='text-primary' onClick='selectMaterial(this);'>{{matnom}}</a></li>";
			$opt = $('.description');
			$opt.empty();
			//console.log(response);
			var i = 0;
			for (var x in response.name) {
				$opt.append(Mustache.render(template, response.name[x] ));
				//console.log(response.name[x]);
			};
			$('.description').show();
			$(".matnom").focus().after($('.description'));
		});
	}
	$(".matnom").keyup(function (event) {
		var key = ( event.keyCode || event.which );
		if (key == 40 || key == 38 || key == 39 || key == 37) {
			moveTopBottom(key);
		};
		if (key === 13) {
			$('.matnom').val( $('.item-selected > a').text() );
			$('.description').hide();
			count = 0;
			getMeters();
		};
	});
	$(".matmed").click(function () {
		var $nom = $(".matnom"), $med = $(".matmed");
		if ($nom.val().trim() != "" && $med.val() != "" ) {
			var template = "<tr><th>Codigo :</th><td class='id-mat'>{{materialesid}}</td></tr>"+
											"<tr><th>Descripción :</th><td>{{matnom}}</td></tr>"+
											"<tr><th>Medida :</th><td>{{matmed}}</td></tr>"+
											"<tr><th>Unidad :</th><td>{{unidad}}</td></tr>";
			var $tb = $(".details-table > tbody");
			$tb.empty();
			var data = { "matnom": $nom.val(), "matmed": $med.val() }
			$.getJSON("/json/get/resumen/details/materiales/", data, function (response) {
				for (var x in response.list) {
					$tb.append( Mustache.render(template, response.list[x] ) );
				};
			});
		};
	});
	$(".btnadd").click(function () {
		aggregate_materials();
	});
	$(".btn-edit-cantidad").click(function () {
		edit_quantity_tmp();
	});
	$(".btn-delete-mat").click(function () {
		var $mid = $(".del-mid"), $dni = $(".empdni"), $btn = $(this), $token = $("[name=csrfmiddlewaretoken]");
		if ($mid.html() != "") {
			$btn.button('loading');
			var data = { "dni": $dni.val(), "mid": $mid.html(),"csrfmiddlewaretoken":$token.val() }
			$.post("/json/post/delete/tmp/materials/", data, function (response) {
				if (response.status) {
					$btn.button('reset');
					list_temp_materials();
					$(".modal-delete-mid").modal("hide");
				};
			},"json");
		};
	});
	list_temp_materials();
	$(".btn-add-mat").click(function () {
		var $block = $(".block-add-mat"), $btn = $(".btn-add-mat > span");
		if (blockAdd) {
			$block.show("blind", 600);
			$btn.removeClass("glyphicon-plus").addClass("glyphicon-minus");
			blockAdd=Boolean(false).valueOf();
		}else{
			$block.hide("blind", 600);
			$btn.addClass("glyphicon-plus").removeClass("glyphicon-minus");
			blockAdd=Boolean(true).valueOf();
		};
	});
	$(".btn-list").click(function () {
		list_temp_materials();
	});
	$(".btn-niples").click(function () {
		get_niples();
	});
	$(".btn-del-all-temp-show").click(function () {
		$(".modal-delete-all-temp").modal("show");
	});
	$(".btn-up-file-show").click(function () {
		$(".modal-up-file").modal("show");
	});
	$(".btn-del-all-temp").click(function () {
		data = { "dni": $(".empdni").val(), "csrfmiddlewaretoken": $("[name=csrfmiddlewaretoken]").val() }
		$.post("/json/post/delete/all/temp/order/", data, function (response) {
			if (response.status) {
				location.reload();
			};
		},"json");
	});
	$(".btn-order-show").click(function (event) {
		event.preventDefault();
		$(".modal-order").modal("show");
	});
	// bedside order
	// loading projects
	$.getJSON("/json/get/projects/list/", function (response) {
		if (response.status) {
			var $pro = $(".pro");
			$pro.empty();
			var template = "<option value='{{proyecto_id}}'>{{nompro}}</option>";
			for(var x in response.list){
				$pro.append( Mustache.render(template, response.list[x]) );
			}
		};
	});
	$.getJSON("/json/get/stores/list/",function (response) {
		if (response.status) {
			var $al = $(".al");
			$al.empty();
			var template = "<option value='{{almacen_id}}'>{{nombre}}</option>";
			for(var x in response.list){
				$al.append( Mustache.render(template, response.list[x]) );
			}
		};
	});
	$(".pro").click(function (event) {
		event.preventDefault();
		var $sub = $(".sub"), $sec = $(".sec");
		// get list subprojects
		$.getJSON("/json/get/subprojects/list/", {"pro":this.value}, function (response) {
			if (response.status) {
				var template = "<option value='{{subproyecto_id}}'>{{nomsub}}</option>";
				$sub.empty();
				$sub.append("<option value=''>-- Nothing --</option>");
				for(var x in response.list){
					$sub.append( Mustache.render(template, response.list[x]) );
				}
			};
		});
		var data = {"pro": this.value}
		$.getJSON("/json/get/sectors/list/",data, function (response) {
			if (response.status) {
				var template = "<option value='{{sector_id}}'>{{nomsec}} {{planoid}}</option>";
				$sec.empty();
				for(var x in response.list){
					$sec.append( Mustache.render(template, response.list[x]) );
				};
			};
		});
	});
	$('.tofile').click(function (event) {
		event.preventDefault();
		$("#file").click();
	});
	$("#file").change(function () {
		console.log('in change');
		if (this.value != "") {
			$('.file-container,.tofile').removeClass('alert-warning text-warning').addClass('alert-success text-success');
		};
	});
	$(".btn-saved-order").click(function (event) {
		$(".modal-order").modal('hide');
		$().toastmessage('showToast',{
			text: 'Seguro(a) que termino de ingresar los materiales al pedido?',
			buttons: [{value:'No'},{value:'Si'}],
			type: 'confirm',
			sticky: true,
			success: function (result) {
				if (result == 'Si') {
					setTimeout(function() {
						$().toastmessage('showToast',{
						text: 'Seguro(a) que termino de ingresar los Niples al pedido, recuerde que una vez que se guarde el pedido no podra modificarse.?',
						buttons: [{value:'No'},{value:'Si'}],
						type: 'confirm',
						sticky: true,
						success: function (resp2) {
							if (resp2 == 'Si') {
								//
								setTimeout(function() {
									$().toastmessage('showToast',{
									sticky: true,
									text: "Desea Generar Pedido almacén?",
									type: "confirm",
									buttons: [{value:'No'},{value:'Si'}],
									success: function (resp3) {
										if(resp3 == 'Si'){
											var data = new FormData($("form").get(0));
											$.ajax({
												data : data,
												url: "",
												type: 'POST',
												dataType: 'json',
												cache: false,
												processData: false,
												contentType: false,
												success: function (response) {
													console.log(response);
													if (response.status) {
														location.reload();
													};
												}
											});
										}else{
											$(".modal-order").modal('show');
										}
									}
								});
								}, 600);
								//
							}else{
								$(".modal-order").modal('show');
							};
						}
					});
					}, 600);
				}else{
					$(".modal-order").modal('show');
				};
			}
		});
		
	});
	$('.obs').focus(function () {
		$(this).animate({height:"102px"},600);
	});
	$('.obs').blur(function () {
		$(this).animate({height:"34px"},600);
	});
	// download template
	$(".btn-down-temp").click(function(event) {
		var url= '/media/storage/templates/Orderstmp.xls';
		window.open(url, "_blank");
	});
	$(".show-input-file-temp").click(function (event) {
		event.preventDefault();
		$(".input-file-temp").click();
	});
});

/// functions 
var blockAdd = Boolean(true).valueOf();
// recover details of materials code, name, measure
var getMeters = function () {
	var $nom = $(".matnom");
	if ($nom.val() != "" ) {
		var template = "<option value='{{matmed}}'>{{matmed}}</option>";
		//$("[data-template-name=user-row]").html().trim();
		var data = { "matnom": $nom.val().trim() }
		$med = $(".matmed");
		$med.empty();
		$.getJSON("/json/get/meter/materials/", data, function (response) {
			for (var x in response.list) {
				$med.append(Mustache.render(template, response.list[x] ));
			};
		});
	};
}
// select materials with click a "a"
var getidli = function (item) {
	$('.matnom').val($('#'+item.id+' > a').text());
	$('.description').hide();
	count = 0;
}
// selected material with click or enter
var selectMaterial = function (all) {
	$('.matnom').val(all.innerHTML);
	$('.description').hide();
	count=0;
}
var count = 0;
// move in a autocomplete
var moveTopBottom = function (key) {
	var code = key;
	var ul = document.getElementById('description');
	if(code === 40){ //down
		if($('#description li.item-selected').length == 0){ //Si no esta seleccionado nada
			$('#description li:first').addClass('item-selected');
		}else{
			$('#description li:first').addClass('item-selected');
		}
	}else if(code === 38){ //arriba
		$('#description li.item-selected').removeClass('item-selected');
	}else if(code === 39){ //abajo
		var liSelected = $('#description li.item-selected');
		if(liSelected.length === 1 && liSelected.next().length === 1){
			liSelected.removeClass('item-selected').next().addClass('item-selected');
			if (count > 9) {
				ul.scrollTop+=30;
			};
			count++;
		}
	}else if(code === 37){ //izquierda
		var liSelected = $('#description li.item-selected');
		if(liSelected.length === 1 && liSelected.prev().length === 1){
			liSelected.removeClass('item-selected').prev().addClass ('item-selected');
			if (count > 9) {
				ul.scrollTop-=30;
			};
			count--;
		}
	}
}
// add material a temp
var aggregate_materials = function () {
	var $mid = $(".id-mat"), $cant = $(".cantidad"), $dni = $(".empdni"), $token = $("[name=csrfmiddlewaretoken]");
	if ($mid.html() != "" && $cant.val() != "") {
		var data = { "mid": $mid.html(),"cant": $cant.val(), "dni": $dni.val(), "csrfmiddlewaretoken": $token.val() }
		$.post("/json/post/aggregate/tmp/materials/", data, function (response) {
			console.log(response);
			if (response.status) {
				list_temp_materials();
			}else{
				console.error("Error en la transación add");
			};
		},"json");
	}else{
		console.warn("No se a ingresado codigo y cantidad.");
	};
}
// list of materials temp
var list_temp_materials = function () {
	var $mid = $(".id-mat");
	if ($(".edit-mid").html() != "") {
		$mid = $('.edit-mid');
	};
	$.getJSON("/json/get/list/temp/order/", { "dni": $(".empdni").val() }, function (response) {
		if (response.status) {
			var $tbody = $("[template-data-user=tmporder]");
			$tbody.empty();
			if (response.list.length > 0) {
				for (var x in response.list){
					if (response.list[x].materiales_id == $mid.html()) {
						var template = "<tr class='success'><td class='text-center'>{{item}}</td><td>{{materiales_id}}</td><td>{{matnom}}</td><td>{{matmed}}</td><td class='text-center'>{{unidad}}</td><td class='text-center'>{{cantidad}}</td><td class='text-center'><button class='btn btn-xs btn-info text-black' onClick='btn_edit_show({{materiales_id}},{{cantidad}});'><span class='glyphicon glyphicon-edit'></span></button></td><td class='text-center'><button class='btn btn-xs btn-danger text-black' onClick='btn_delete_show({{materiales_id}},{{cantidad}})'><span class='glyphicon glyphicon-remove'></span></button></td></tr>";	
					}else{
						var template = "<tr><td class='text-center'>{{item}}</td><td>{{materiales_id}}</td><td>{{matnom}}</td><td>{{matmed}}</td><td class='text-center'>{{unidad}}</td><td class='text-center'>{{cantidad}}</td><td class='text-center'><button class='btn btn-xs btn-info text-black' onClick='btn_edit_show({{materiales_id}},{{cantidad}});'><span class='glyphicon glyphicon-edit'></span></button></td><td class='text-center'><button class='btn btn-xs btn-danger text-black' onClick='btn_delete_show({{materiales_id}},{{cantidad}})'><span class='glyphicon glyphicon-remove'></span></button></td></tr>";
					}
					$tbody.append( Mustache.render(template,response.list[x]) );
				}
				$(".success").ScrollTo({
					duration: 1000,
					callback: function () {
						setTimeout(function() {
							$(".well").ScrollTo({
								duration: 1000
							});
							$(".description").focus();
						}, 1000);
					}
				});
			}else{
				$().toastmessage("showNoticeToast","No se han encontrado materiales para mostar.");
			};
		};
	});
}
var btn_edit_show = function (id,cant) {
	id = String(id).valueOf()
	if (id != "") {
		var data = { "mid": id }
		$.getJSON("/json/get/details/materials/", data, function (response) {
			if (response.status) {
				$(".edit-mid").html(id);
				$(".edit-des").html(response.matnom);
				$(".edit-med").html(response.matmed);
				$(".edit-unid").html(response.unidad_id);
				$(".edit-cant").val(cant);
				$(".modal-edit-cant").modal("show");
			};
		});
	};
}
var btn_delete_show = function (id,cant) {
	$.getJSON('/json/get/details/materials/',{"mid": id}, function (response) {
		if (response.status) {
			$(".del-mid").html(id);
			$(".del-des").html(response.matnom);
			$(".del-med").html(response.matmed);
			$(".del-unid").html(response.unidad_id);
			$(".del-cant").html(cant);
			$(".modal-delete-mid").modal("show");
		};
	});
}
var edit_quantity_tmp = function () {
	var $mid = $(".edit-mid"), $cant = $(".edit-cant"), $dni = $(".empdni"), $btn = $(".btn-edit-cantidad"), $token = $("[name=csrfmiddlewaretoken]");
	if ($mid.html() != "" && $cant.val() != 0) {
		$btn.button('loading');
		var data = { "dni": $dni.val(), "mid": $mid.html(), "cantidad": $cant.val(),"csrfmiddlewaretoken":$token.val() }
		$.post("/json/post/update/tmp/materials/", data, function (response) {
			if (response.status) {
				$btn.button('reset');
				$(".modal-edit-cant").modal("hide");
				list_temp_materials();
				setTimeout(function() { $(".edit-mid").html(""); }, 3000);
			};
		},"json");
	};
}
var get_niples = function () {
	var template = "<div class='panel panel-default panel-warning'>"+
										"<div class='panel-heading'>"+
											"<h4 class='panel-title'>"+
											"<a data-toggle='collapse' class='collapsed' data-parent='#niples' onClick='list_temp_nipples({{materiales_id}});' href='#des{{materiales_id}}'>{{matnom}} - {{matmed}}</a>"+
											"<span class='pull-right badge badge-warning'>Quedan <span class='res{{materiales_id}}'></span> cm</span>"+
											"<span class='pull-right badge badge-warning'>Ingresado <span class='in{{materiales_id}}'></span> cm</span>"+
											"<span class='pull-right badge badge-warning'>Total {{cantidad}} {{unidad}}</span>"+
											"<input type='hidden' class='totr{{materiales_id}}' value='{{cantidad}}'>"+
											"</h4>"+
										"</div>"+
										"<div id='des{{materiales_id}}' class='panel-collapse collapse'>"+
											"<div class='panel-body c{{materiales_id}}'>"+
											"<div class='table-responsive'>"+
												"<table class='table table-condensed table-hover'>"+
													"<caption class='text-left'><div class='row'><div class='col-md-4'><div class='btn-group'>"+
														"<button class='btn btn-default btn-xs btn-add-nipple-{{materiales_id}}' onClick='aggregate_nipples({{materiales_id}});' type='Button' data-loading-text='Proccess...'><span class='glyphicon glyphicon-plus-sign'></span> Agregar</button>"+
														"<button class='btn btn-default btn-xs' onClick='list_temp_nipples({{materiales_id}});' type='Button' data-loading-text='Proccess...'><span class='glyphicon glyphicon-refresh'></span> Recargar</button>"+
														"<button class='btn btn-danger btn-xs' onClick='delete_all_temp_nipples({{materiales_id}});' type='Button' data-loading-text='Proccess...'><span class='glyphicon glyphicon-trash'></span> Eliminar Todo</button>"+
													"</div></div>"+
													"<div class='col-md-8'><div class='form-inline pull-right'>"+
														"<div class='form-group '>"+
															"<select name='controlnipples' class='form-control input-sm tn{{materiales_id}}' title='Tipo Niple' placeholder='Tipo Niple' DISABLED>"+
																"<option value='A'>A - Roscado</option><option value='B'>B - Ranurado</option><option value='C'>C - Roscado - Ranurado</option>"+
															"</select>"+
														"</div>"+
														"<div class='form-group col-md-4'>"+
															"<div class='input-group input-group-sm'><input type='number' name='controlnipples' placeholder='Medida' min='0' class='form-control input-sm mt{{materiales_id}}' DISABLED><span class='input-group-addon'><strong>cm</strong><span></div>"+
														"</div>"+
														"<div class='form-group'>"+
															"<input type='number' name='controlnipples' placeholder='Cantidad' min='1' class='form-control input-sm nv{{materiales_id}}' DISABLED>"+
														"</div>"+
														"<input type='hidden' class='update-id-{{materiales_id}}' value=''>"+
														"<input type='hidden' class='update-quantity-{{materiales_id}}' value=''>"+
														"<button class='btn btn-success text-black btn-sm' name='controlnipples' type='Button' onClick='saved_or_update_nipples({{materiales_id}})' DISABLED><span class='glyphicon glyphicon-floppy-save'></span> Guardar</button>"+
													"</div></div>"+
													"</caption>"+
													"<thead><th>Cantidad</th><th>Descripción</th><th>Diametro</th><th><th><th>Medida</th><th>Unidad</th><th>Editar</th><th>Eliminar</th></thead>"+
													"<tbody class='tb{{materiales_id}}'></tbody>"+
												"</table>"+
											"</div>"+	
											"</div>"+
										"</div>"+
									"</div>";
	// bring all the tub for contruction "Nipples"
	$.getJSON("/json/get/nipples/temp/oreder/", function (response) {
		if (response.status) {
			var $collapse = $("#niples");
			$collapse.empty();
			for (var x in response.nipples) {
				$collapse.append( Mustache.render( template, response.nipples[x] ) );
			};
		}else{
			$().toastmessage("showNoticeToast","No se han encontrado Tuberia para generar niples.");
		};
	});
}
// enable function that controls
var aggregate_nipples = function (mid) {
	mid = String(mid).valueOf();
	$("[name=controlnipples]").attr("DISABLED",false);
	$(".update-id-"+mid).val("");
}
var list_temp_nipples = function (mid) {
	mid = String(mid).valueOf();
	if (mid != "") {
		var data = { "mid": mid, "dni": $(".empdni").val() }
		$.getJSON("/json/get/list/temp/nipples/", data, function (response) {
			if (response.status) {
				var $tb = $(".tb"+mid),
						template = "<tr><td class='text-center'>{{cantidad}}</td><td>{{matnom}}</td><td>{{matmed}}</td><td>x<td><td class='text-center'>{{metrado}}</td><td class='text-center'>cm</td><td class='text-center'><button type='Button' class='btn btn-xs btn-info text-black' onClick=edit_temp_nipple({{id}},{{materiales_id}},{{cantidad}},{{metrado}},'{{tipo}}');><span class='glyphicon glyphicon-edit'></span></button></td><td class='text-center'><button type='Button' class='text-black btn btn-xs btn-danger' onClick='delete_temp_nipple({{id}},{{materiales_id}})'><span class='glyphicon glyphicon-remove'></span></button></td>";
				$tb.empty();
				var totcm = 0, incm = 0, res = 0;
				totcm = ( (parseInt($(".totr"+mid).val())) * 100 );
				for(var x in response.list){
					$tb.append( Mustache.render(template, response.list[x]) );
					incm += ( response.list[x].cantidad * response.list[x].metrado);
				}
				res = totcm - incm;
				$(".in"+mid).html(incm);
				$(".res"+mid).html(res);
				if (res == 0 || res < 0) {
					$(".btn-add-nipple-"+mid).attr("disabled", true);
				}else{
					$(".btn-add-nipple-"+mid).attr("disabled", false);
				};
			};
		});
	};
}
var saved_or_update_nipples = function (mid) {
	mid = String(mid).valueOf();
	var $update = $(".update-id-"+mid), $quantity = $(".mt"+mid), $type = $(".tn"+mid), $nv = $(".nv"+mid), nv = 0, pass = Boolean(false).valueOf();
	if ($quantity.val().trim() == "") { $().toastmessage('showWarningToast', "No se a ingresado una cantidad."); return pass;}else{ pass = Boolean(true).valueOf(); console.info(pass);};
	if ($nv.val().trim() == "" || $nv.val().trim() == 0) { nv = 1 }else{ nv = $nv.val(); };
	var valcant = parseInt($quantity.val().trim()) * parseInt(nv), res = parseInt( $(".res"+mid).html().trim());
	if ($update.val().trim() != "") {
		var uco = $(".update-quantity-"+mid).val();
		pass = valcant <= (parseInt(uco)+res) ? Boolean(true).valueOf() : Boolean(false).valueOf();
	}else if (valcant > res) {
		pass = Boolean(false).valueOf();
		$().toastmessage("showWarningToast","La cantidad ingresada es superior a la establecida.");
		return false;
	};
	if (pass && nv >= 1) {
		var data = {}
		if ($update.val().trim() == "") {
			data = {"tra":"new","cant": $quantity.val().trim(), "mid": mid, "type": $type.val(), "veces": nv, "dni": $(".empdni").val(),"csrfmiddlewaretoken":$("[name=csrfmiddlewaretoken]").val()}
		}else{
			data = {"tra":"update","id": $update.val(),"cant": $quantity.val().trim(), "mid": mid, "type": $type.val(), "veces": nv, "dni": $(".empdni").val(),"csrfmiddlewaretoken":$("[name=csrfmiddlewaretoken]").val() }
		};
		$.post("/json/post/saved/temp/nipples/", data, function (response) {
			if (response.status) {
				list_temp_nipples(mid);
				$("[name=controlnipples]").attr("DISABLED",true);
				$(".update-id-"+mid).val("");
				$(".update-quantity-"+mid).val("");
			};
		});
	}else{
		$().toastmessage("showWarningToast","La cantidad o la medida no se han ingresado o no son correctas.")
	};
}
var edit_temp_nipple = function(id,mid,cant,med,tipo){
	$("[name=controlnipples]").attr("DISABLED",false);
	mid = String(mid).valueOf();
	$(".mt"+mid).val(med);
	$(".nv"+mid).val(cant);
	$(".tn"+mid).val(tipo);	
	$(".tn"+mid).attr("DISABLED",true);
	//$(".nv"+mid).attr("DISABLED",true);
	$(".update-id-"+mid).val(id);
	$(".update-quantity-"+mid).val( (parseInt(cant) * parseInt(med)) );
}
var delete_temp_nipple = function (id,mid) {
	$().toastmessage('showToast',{
		text: "Seguro(a) que desea eliminar el niple?",
		type: 'confirm',
		sticky: true,
		buttons: [{value:'No'},{value:'Si'}],
		success: function (result){
			if (result == "Si") {
				mid = String(mid).valueOf();
				var data = {"id": id, "mid": mid, "dni": $(".empdni").val(),"csrfmiddlewaretoken":$("[name=csrfmiddlewaretoken]").val()};
				$.post("/json/post/delete/temp/nipples/item/", data, function (response) {
					if (response.status) {
						mid = String(mid).valueOf();
						list_temp_nipples(mid);
					};
				},"json");
			};
		}
	});
}
var delete_all_temp_nipples = function (mid) {
	$().toastmessage('showToast',{
		text: "Seguro(a) que desea eliminar toda la lista de niples?",
		type: 'confirm',
		sticky: true,
		buttons: [{value:'No'},{value:'Si'}],
		success: function (result){
			if (result == "Si") {
				mid = String(mid).valueOf();
				var data = {"mid": mid, "dni": $(".empdni").val(),"csrfmiddlewaretoken":$("[name=csrfmiddlewaretoken]").val()};
				$.post("/json/post/delete/all/temp/nipples/", data, function (response) {
					if (response.status) {
						mid = String(mid).valueOf();
						list_temp_nipples(mid);
					};
				},"json");
			};
		}
	});
}