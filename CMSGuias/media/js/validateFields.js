/*
 functions for validate fields in a form
*/

var validateFormatDate = function (data) {
	var value = data,
			pass = false,
			RegExpattern = /^\d{4}\-\d{1,2}\-\d{1,2}$/; // Format DDBB /^\d{2}\/\d{2}\/\d{4}$/
	if ( (value != "") && (value.match(RegExpattern)) ) {
		pass = true;
	};
	return pass;
}