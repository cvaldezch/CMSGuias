$(document).ready(function() {
	$("[name=bedside]").change(function (event) {
		event.preventDefault();
		if (this.checked){
			var chk = document.getElementsByName("bed");
			for (var i = 0; i < chk.length; i++) {
				chk[i].checked = this.value == 'true' ? true : false
				$(".bed"+chk[i].value).attr("disabled", chk[i].checked ? false : true );
				$("[name="+chk[i].value+"]").attr("disabled", chk[i].checked ? false : true );
				$("[name=sc"+chk[i].value+"]").attr("disabled", chk[i].checked ? false : true );
				checkeded(String('sc'+chk[i].value).valueOf(), chk[i].checked ? true : false);
			};
		}
	});
	$("input[name=bed]").change(function () {
		$(".bed"+this.value).attr("disabled", $(this).is(':checked') ? false : true );
		$("[name="+this.value+"]").attr("disabled", $(this).is(':checked') ? false : true );
		$("[name=sc"+this.value+"]").attr("disabled", $(this).is(':checked') ? false : true );
		checkeded(String("sc"+this.value).valueOf(), $(this).is(':checked') ? true : false);
	});
	$(".btn-attend").click(function (event) {
		event.preventDefault();
		$().toastmessage("showToast",{
			type: 'confirm',
			sticky: true,
			text: "Atender el pedido y generar un documento de salida de almacén. Deseas atender el pedido?",
			buttons: [{value:'Si'},{value:'No'}],
			success: function (result) {
				if (result == 'Si') {
					attendOrders();
				};
			}
		});
	});
});
var changeradio = function (id) {
	var item = id;
	if (item.checked) {
		var chk = document.getElementsByName('sc'+item.name);
		for (var i = 0; i < chk.length; i++) {
			chk[i].checked = item.value == "true" ? true : false
			$(".n"+chk[i].value).attr('disabled', chk[i].checked ? false : true );
		};
	};
}
var checkeded = function (name,sts) {
	var rdo = document.getElementsByName(name.substr(2));
	for (var i = 0; i < rdo.length; i++) {
		if (rdo[i].value == String(sts).valueOf() && !rdo[i].checked) {
			rdo[i].checked = true;
		};
	};
	var chk = document.getElementsByName(name);
	for (var i = 0; i < chk.length; i++) {
		chk[i].checked = sts;
		$(".n"+chk[i].value).attr('disabled', !sts );
	};
}
var enablenquantitynip = function (id) {
	$(".n"+id.value).attr('disabled', id.checked ? false : true );
}
var attendOrders = function () { 
	var pass = false;
	// valid detail orders
	var cd = 0, cn = 0, ctu = 0, mid = new Array();
	$("[name=bed]").each(function () {
		if (this.checked) {
			cd+= 1;
			if (this.value.substr(0,3) == '115'){
				ctu+= 1;
				mid.push(this.value);
			}
		};
	});
	// valid enable nipples
	$(".chknip").each(function () {
		cn += this.checked ? 1 : 0
	});
	// validating selections materials
	if (cd > 0) {
		if (ctu > 0) {
			if (cn > 0) {
				pass = true;
				for (var i = 0; i < mid.length; i++) {
					var j = 0;
					$('[name=sc'+mid[i]+']').each(function () {
						if (this.checked) {
							j++;
						};
					});
					pass= j > 0 ? true : false
					if (!pass) { $().toastmessage('showWarningToast', 'Hay niples sin seleccionar'); return pass; };
				};
			}else{
				$().toastmessage('showWarningToast',"Existe tuberia seleccionada pero no se han seleccionado niples.");
				pass = false;
				return false;
			};
		}
		pass = true;
	}else{
		$().toastmessage('showWarningToast',"No se han seleccionado materiales para atender.");
		pass = false;
		return false;
	};
	if (pass) {
		// loading parameters
		var data = new Object(), am = new Array(), an = new Array();
		$("[name=bed]").each(function () {
			if (this.checked) {
				am.push( {'matid': this.value, 'quantityshop': $('.bed'+this.value).val(), 'quantity': $('.bed'+this.value).attr('name') } );
			};
		});
		$(".chknip").each(function () {
			if (this.checked) {
				an.push( { 'nid': this.value, 'matid': $('.n'+this.value).attr('title'), 'quantityshop': $('.n'+this.value).val(),'quantity': $('.n'+this.value).attr('name'),'meter': $('.n'+this.value).attr('id') } );
			};
		});
		data['materials']= JSON.stringify(am);
		data['nipples']= JSON.stringify(an);
		data['csrfmiddlewaretoken'] = $("[name=csrfmiddlewaretoken]").val();
		data['oid']= $(".oid").val();
		console.info(data);
		$.post('', data, function (response) {
			console.warn(response);
			if (response.status) {
				location.href="/almacen/generate/"+$(".oid").val()+"/document/out/";
			}else{
				$().toastmessage("showErrorToast","Transaction not found");
			};
		});
	}else{
		$().toastmessage("showErrorToast","Transaction incorrect!");
	};
}