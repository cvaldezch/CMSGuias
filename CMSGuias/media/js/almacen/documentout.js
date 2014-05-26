$(document).ready(function() {
	$("#guide,#note").hide();
	$(".btn-guide-show").click(function  (event) {
		event.preventDefault();
		$("#note").hide('blind', 600);
		$("#guide").show('blind', 600);
	});
	$(".btn-note-show").click(function  (event) {
		event.preventDefault();
		$("#guide").hide('blind', 600);
		$("#note").show('blind', 600);
	});
});