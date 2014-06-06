$(document).ready(function() {
	$(".opad").hide();
	$(document).on('keyup',"input[name=cod],input[name=desc]" , keyUpInput);
	$(".btn-register-all-list").on('click',register_all_list);
	$(".btn-list-period").on("click", register_period_pased);
	$("button[name=btn-opad]").click(function(event) {
		$(".opad").toggle("blind",600);
	});
});

// functions
var keyUpInput = function (event) {
	event.preventDefault();
	var key = (event.keyCode ? event.keyCode : event.which);
	if (key == 13) {
		search(this);
	};
}
var search = function (ctrl) {
	var data = new Object();
	// recover data for search data
	data['periodo'] = $("select[name=periodo]").val(); // get value periodo
	data['almacen'] = $("select[name=almacen]").val(); // get value almacen
	data['omat'] = ctrl.value;
	data['tipo'] = ctrl.name;
	data['stkzero'] = $(".stkzero").is(":checked") ? true : false;
	data['stkmin'] = $(".stkmin").is(":checked") ? $(".smin").val() : 'None';
	console.log(data);
	$.get('',data,function (response) {
		var $tbody = $("[data-template-name=list-materials]");
		var template = "<td>{{ item }}</td>
									<td>{{ materiales_id }}</td>
									<td>{{ matnom }}</td>
									<td>{{ matmet }}</td>
									<td>{{ unid }}</td>
									<td>{{ stkmin }}</td>
									<td>{{ stock }}</td>
									<td>{{ ingreso }}</td>
									<td>{{ compra_id }}</td>
									<td></td>";
		$tbody.empty();
		for (var x in response.list) {
			$tbody.append(Mustache.render(template, response.list[x]))
		};
		console.log(response);
	});
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