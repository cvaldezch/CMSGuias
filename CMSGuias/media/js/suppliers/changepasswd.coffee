$(document).ready ->
	$("input[name=confirm]").on "keyup", verifyEqual
	return

verifyEqual = (event) ->
	passwd = $.trim $("input[name=passwd]").val()
	confirm = $.trim @value
	if passwd is confirm
		$("span.confirm > span").addClass "glyphicon-ok"
		.addClass "text-success"
		.removeClass "glyphicon-remove"
		.removeClass "text-danger"
		$("button.btn-primary").attr "disabled", false
	else
		$("span.confirm > span").addClass "glyphicon-remove"
		.addClass "text-danger"
		.removeClass "glyphicon-ok"
		.removeClass "text-success"
		$("button.btn-primary").attr "disabled", true
	return