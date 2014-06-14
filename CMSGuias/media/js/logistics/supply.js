$(document).ready(function() {
	$("[name=fi-su],[name=ff-su]").datepicker({ showAnim : "slide", dateFormat : "yy-mm-dd" });
	$("[name=id-su],[name=fi-su],[name=ff-su]").attr('disabled', true);
	$("[name=rdo]").on("change", changeRadio);
	$(".btn-proccess").hover(
		function () {
			$(".btn-proccess > span").addClass("glyphicon-check").removeClass('glyphicon-unchecked');
		},
		function () {
			$(".btn-proccess > span").removeClass("glyphicon-check").addClass("glyphicon-unchecked");
		}
	);
});

// functions
var changeRadio = function (event) {
	event.preventDefault();
	if (this.checked) {
		if (this.value == 'code') {
			$("[name=id-su]").attr('disabled',false);
			$("[name=fi-su],[name=ff-su]").attr('disabled',true);
		}else if(this.value == 'date'){
			$("[name=fi-su],[name=ff-su]").attr('disabled',false);
			$("[name=id-su]").attr('disabled',true);
		};
	};
}