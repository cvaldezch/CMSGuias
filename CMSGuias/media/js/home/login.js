$(function () {
	$('#id_username,#id_password').addClass('form-control');
	if ($.trim($('.msg').html()).length > 0) {
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