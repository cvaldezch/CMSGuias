$(document).ready(function() {
	$(".content").hide();
	$(document).on("change","[name=sel]", changeSelect);
});

// functions

var changeSelect = function (event) {
	event.preventDefault();
	var rdo = this;
	$("[name=chk]").each(function () {
		this.checked = Boolean(rdo.value);
	});
}