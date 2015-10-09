var convertNumber, numberOnly, numberPatterm, validateEmail, validateFormatDate;

validateFormatDate = function(data) {
  var RegExpattern, pass, value;
  value = data;
  pass = false;
  RegExpattern = /^\d{4}\-\d{1,2}\-\d{1,2}$/;
  if (value !== "" && value.match(RegExpattern)) {
    pass = true;
  }
  return pass;
};

validateEmail = function(email) {
  var re;
  re = /\S+@\S+\.\S+/;
  return re.test(email);
};

convertNumber = function(val) {
  var num;
  if (isNaN(val)) {
    num = val.replace(",", ".");
    num = parseFloat(num);
  } else {
    num = parseFloat(val);
  }
  return num;
};

numberOnly = function(event) {
  var key;
  key = window.Event ? event.keyCode : event.which;
  if (key !== 37 && key !== 39 && key !== 8 && key !== 46 && (key < 48 || key > 57)) {
    event.preventDefault();
    return false;
  }
};

numberPatterm = function(event) {
  var RegExpattern, pattern;
  pattern = this.getAttribute("pattern");
  if (pattern) {
    RegExpattern = new RegExp(pattern);
  } else {
    RegExpattern = /^\d*([\.]{1}?\d*|\d*)$/;
  }
  if (!this.value.match(RegExpattern)) {
    $().toastmessage("showWarningToast", "Formato incorrecto. " + this.title);
  }
};

setTimeout(function() {
  $(document).on("keypress", ".numberValid", numberOnly).on("keyup change", ".numberValid", numberPatterm);
}, 110);
