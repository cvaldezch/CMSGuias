// load funtions of page
$(function () {
	$('.description, .block-add-mat').hide();
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
			var template = "<li id='li{{id}}' onclick=getidli(this);><a class='text-primary' onclick='selectMaterial(this);'>{{matnom}}</a></li>";
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
});
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
											"<a data-toggle='collapse' class='collapsed' data-parent='#niples' href='#des{{materiales_id}}'>{{matnom}} - {{matmed}}</a>"+
											"<span class='pull-right badge'>{{cantidad}} {{unidad}}</span>"+
											"</h4>"+
										"</div>"+
										"<div id='des{{materiales_id}}' class='panel-collapse collapse'>"+
											"<div class='panel-body c{{materiales_id}}'>"+
											"<div class='table-responsive'>"+
												"<table class='table table-condensed table-hover'>"+
													"<caption class='text-left'><div class='row'><div class='col-md-4'><div class='btn-group'>"+
														"<button class='btn btn-default btn-xs' type='Button' data-loading-text='Proccess...'><span class='glyphicon glyphicon-plus-sign'></span> Agregar</button>"+
														"<button class='btn btn-default btn-xs' type='Button' data-loading-text='Proccess...'><span class='glyphicon glyphicon-refresh'></span> Recargar</button>"+
														"<button class='btn btn-danger btn-xs' type='Button' data-loading-text='Proccess...'><span class='glyphicon glyphicon-trash'></span> Eliminar Todo</button>"+
													"</div></div>"+
													"<div class='col-md-8'><div class='form-inline'>"+
														"<div class='form-group'>"+
															"<select name='typenipple' class='form-control input-sm' title='Tipo Niple' placeholder='Tipo Niple' id='>"+
																"<option value='A'>Roscado</option><option value='B'>Ranurado</option><option value='C'>Roscado - Ranurado</option>"+
															"</select>"+
														"</div>"+
														"<div class='form-group'>"+
															"<input type='number' step='0.01' placeholder='Ingresa Metrado' min='0' class='form-control input-sm'>"+
														"</div>"+
														"<div class='form-group'>"+
															"<input type='number' placeholder='Repetir n veces' min='1' class='form-control input-sm'>"+
														"</div>"+
														"<button class='btn btn-success text-black btn-sm'><span class='glyphicon glyphicon-floppy-save'></span> Guardar</button>"+
													"</div></div>"+
													"</caption>"+
													"<thead><th>Item</th><th>Codigo</th><th>Descripción</th><th>Medida</th><th>Unidad</th><th>Meter</th><th>Editar</th><th>Eliminar</th></thead>"+
													"<tobody class='tb{{materiales_id}}'></tbody>"+
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
			alert("No se a encontrado Tuberia");
		};
	});
}