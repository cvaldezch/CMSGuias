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
	data['stkzero'] = $(".stkzero").is(":checked") ? true : false;
	data['stkmin'] = $(".stkmin").is(":checked") ? $(".smin").val() : 'None';
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
									"<td></td></tr>";
		$tbody.empty();
		for (var x in response.list) {
			response.list[x].status = response.list[x].stock <= 0 ? 'danger' : response.list[x].stock >= response.list[x].stkmin ? 'success' : 'warning'
			response.list[x].item = (parseInt(x) + 1);
			$tbody.append(Mustache.render(template, response.list[x]))
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