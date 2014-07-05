$(function () {
	$('#id_username,#id_password').addClass('form-control');
	if ($('.msg').html().trim().length > 0) {
		$('.content-msg').css('display','block');
		$('#id_username,#id_password').each(function () {
			var item = this;
			if (item.value == '') {
				item.focus();
				return false;
			};
		});
	};
});