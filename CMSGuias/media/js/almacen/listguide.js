$(document).ready(function() {
	$(".btn-show-gv").click(function (event) {
		event.preventDefault();
		$(".btn-gv").val(this.value);
		$(".mview").modal("show");
	});
	$(".btn-gv").click(function (event) {
		event.preventDefault();
		url= "/reports/guidereferral/"+this.value+"/"+this.name+"/";
		window.open(url,"_blank");
	});
});