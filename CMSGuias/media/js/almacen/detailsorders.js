$(document).ready(function() {
	$(document).on("change", "input[type=radio]", selectedChk);
	$(document).on("change", "input[type=checkbox]", changeChk);
	$(document).on("click", "button", resgisterMaterial);
	setTimeout(function() {validregisterOld();}, 600);
});

// functions
var resgisterMaterial = function (event) {
	event.preventDefault();
	var name = this.name.substr(3),
			counter = 0,
			arr = new Array();
	// valid checkbox selected
	$("[name=chk"+name+"]").each(function () {
		if (this.checked && !$(this).is(':disabled')) {
			counter += 1;
			arr.push({"oid": name, "mid": this.title, "cant": parseFloat(this.value)});
		};
	});
	if (counter > 0) {
		var data = new Object();
		data['csrfmiddlewaretoken'] = $("input[name=csrfmiddlewaretoken]").val();
		data['mats'] = JSON.stringify(arr);
		data['add-ori'] = 'PE'
		$.post('',data, function(response) {
			if (response.status) {
				for (var i in arr) {
					$("[name=chk"+arr[i].oid+"]").attr("disabled","disabled");
				};
			};
		}, "json");
	}else{
		$().toastmessage("showWarningToast","No se han seleccionado materiales.");
	};
}
var changeChk = function (event) {
	event.preventDefault();
	var name = this.name.substr(3),
			$chk = $("[name=chk"+name+"]"),
			chk = 0;
	$("[name=rdo"+name+"]").each(function (){
		if (this.value == '') {
			this.checked = true;
		}else{
			$("[name=btn"+name+"]").attr("disabled", false);
		};
	});
	$chk.each(function() {
		if (this.checked) {
			chk += 1;
		};
	});
	$("[name=btn"+name+"]").attr("disabled", chk == 0 ? true : false );
};
var selectedChk = function (event) {
	event.preventDefault();
	var name = this.name.substr(3),
			value = Boolean(this.value);
	$("input[name=chk"+name+"]").each(function () {
		if ($(this).is(":disabled")) {
			return true;
		};
		this.checked = value;
	});
	$("button[name=btn"+name+"]").attr('disabled', !value);
};
var validregisterOld = function () {
	$("button").each(function() {
		var name = this.name.substr(3),
				chk = 0,
				$chkt = $("input[name=chk"+name+"]");
		console.log(name);
		$chkt.each(function () {
			if (this.checked) {
				chk += 1;
			};
		});
		console.log(chk);
		if (chk == 1) {
			return true;
		}else if(chk > 1 && chk < $chkt.length || chk == $chkt.length){
			$("[name=rdo"+name+"]").attr("disabled","disabled");
			$("[name=btn"+name+"]").attr("disabled","disabled");
		};
		if (chk > 1 && chk < $chkt.length) {
			$("[name=rdo"+name+"]").attr("disabled",false);
		};
	});
}