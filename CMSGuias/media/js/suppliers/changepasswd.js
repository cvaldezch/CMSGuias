var verifyEqual;

$(document).ready(function() {
  $("input[name=confirm]").on("keyup", verifyEqual);
});

verifyEqual = function(event) {
  var confirm, passwd;
  passwd = $.trim($("input[name=passwd]").val());
  confirm = $.trim(this.value);
  if (passwd === confirm) {
    $("span.confirm > span").addClass("glyphicon-ok").addClass("text-success").removeClass("glyphicon-remove").removeClass("text-danger");
    $("button.btn-primary").attr("disabled", false);
  } else {
    $("span.confirm > span").addClass("glyphicon-remove").addClass("text-danger").removeClass("glyphicon-ok").removeClass("text-success");
    $("button.btn-primary").attr("disabled", true);
  }
};
