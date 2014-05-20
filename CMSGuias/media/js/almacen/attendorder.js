$(document).ready(function() {
	$("[name=bedside]").change(function (event) {
		event.preventDefault();
		if (this.checked){
			var chk = document.getElementsByName("bed");
			for (var i = 0; i < chk.length; i++) {
				chk[i].checked = this.value == 'true' ? true : false
				$(".bed"+chk[i].value).attr("disabled", chk[i].checked ? false : true );
			};
		}
	});
	$("input[name=bed]").change(function () {
		$(".bed"+this.value).attr("disabled", $(this).is(':checked') ? false : true );
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