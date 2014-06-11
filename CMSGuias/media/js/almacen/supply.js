$(document).ready(function() {
	$(".content,.data-condensed").hide();
	$(document).on("change","[name=sel]", changeSelect);
	$(".btn-gen").on("click", showGen);
	$(".btn-compress").on("click", compressList);
	$(".btn-back").on("click", backlist);
	$(".obser").focusin(function (event) {
		this.rows = 3;
	}).focusout(function (event) {
		this.rows = 1;
	});
	$("input[name=ingreso]").datepicker({ minDate: "0", maxDate: "+6M", showAdnim: "blind", dateFormat: "yy-mm-dd" });
	$(".btn-generate").on("click", generateSupply);
});

// functions
var generateSupply = function (event) {
	var chk, pass, arr = new Array(), data = new Object();
	// validate materials checked
	$("input[name=quote]").each(function () {
		if (this.checked) {
			arr.push({"mid": this.title, "cant": this.value });
			pass = true;
		}else{
			pass = false;
		};
	});
	$("[name=almacen],[name=ingreso]").each(function () {
		if ($(this).val() != '') {
			data[this.name] = $(this).val();
		}else{
			pass = false;
		};
	});
	if (pass) {
		data['mats'] = arr;
		data['obser'] = $("[name=obser]").val();
		data['csrfmiddlewaretoken'] = $("input[name=csrfmiddlewaretoken]").val();
		console.log(data);
		$.post("", data, function(response) {
			console.log(response);
			if (response.status) {
				location.reload();
			};
		});
	}else{
		$().toastmessage("showWarningToast","Se a encontrado un campo vacio.");
	};
}
var backlist = function (event) {
	event.preventDefault();
	$(".table-first").show('slide', 400);
  $(".data-condensed").hide('blind', 200);
  $(".btn-gen").click();
}
var compressList = function (event) {
	event.preventDefault();
	var array  = new Array();
	// recover id materials
	$("input[name=chk]").each(function () {
		if (this.checked) {
			array.push(this.value);
		};
	});
	if (array.length > 0) {
		var data = new Object();
		data['mats'] = JSON.stringify(array);
		$.getJSON("", data, function (response) {
			console.log(response);
			if (response.status) {
				var $tb = $(".data-condensed > tbody"),
				template = "<tr><td>{{ item }}</td><td><input type='checkbox' name='quote' value='{{ cantidad }}' title='{{ materiales_id }}' checked DISABLED /></td><td>{{ materiales_id }}</td><td>{{ matnom }}</td><td>{{ matmed }}</td><td>{{ unidad }}</td><td>{{ cantidad }}</td></tr>";
				$tb.empty();
				for (var x in response.list) {
					response.list[x].item = (parseInt(x) + 1);
					$tb.append(Mustache.render(template, response.list[x]));
				};
				$(".table-first").hide('slide', 200);
				$(".data-condensed").show('blind', 400);
			};
		});
	}else{
		$().toastmessage("showWarningToast", "No se han seleccionado materiales, para comprimir");
	};
}
var showGen = function (event) {
	event.preventDefault();
	$(".content").toggle(function () {
		if (!$(this).is(":hidden")) {
			$(".btn-gen > span").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
		}else{
			$(".btn-gen > span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
		};
	});
}
var changeSelect = function (event) {
	event.preventDefault();
	var rdo = this;
	$("[name=chk]").each(function () {
		this.checked = Boolean(rdo.value);
	});
}