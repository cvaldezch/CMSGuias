var getBudgetData, saveBudget, showBudget, showSearchBudget;

$(function() {
  $(".panel-sbudget, .panel-details-budget").hide();
  $("[name=finish]").datepicker({
    changeMonth: true,
    changeYear: true,
    minDate: "0",
    dateFormat: "yy-mm-dd"
  });
  $("[name=showBudget]").on("click", showBudget);
  $(".bsearchbudget").on("click", showSearchBudget);
  $("[name=saveBudget]").on("click", saveBudget);
  tinymce.init({
    selector: "textarea[name=observation]",
    menubar: false,
    toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image"
  });
});

showBudget = function(event) {
  $("#nbudget").modal("show");
};

showSearchBudget = function(event) {
  $(".panel-sbudget").toggle("linear");
};

saveBudget = function(event) {
  $.validate({
    form: "#newBudget",
    errorMessagePosition: "top",
    scrollToTopOnError: true,
    onError: function() {
      return false;
    },
    onSuccess: function() {
      var params;
      event.preventDefault();
      params = new Object;
      params.name = $("[name=name]").val();
      params.customers = $("[name=customers]").val();
      params.address = $("[name=address]").val();
      params.country = $("[name=pais]").val();
      params.departament = $("[name=departamento]").val();
      params.province = $("[name=provincia]").val();
      params.district = $("[name=distrito]").val();
      params.hourwork = $("[name=hours]").val();
      params.finish = $("[name=finish]").val();
      params.base = $("[name=base]").val();
      params.offer = $("[name=offer]").val();
      params.currency = $("[name=currency]").val();
      params.exchange = $("[name=exchange]").val();
      params.observation = $("#observation_ifr").contents().find("body").html();
      params.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
      params.saveBudget = true;
      $.post("", params, function(response) {
        if (response.status) {
          location.reload();
        } else {
          $().toastmessage("showErrorToast", "No se han guardado lo datos correctamente. " + response.raise);
        }
      }, "json");
      return false;
    }
  });
};

getBudgetData = function(event) {
  var params;
  params = new Object;
  params.budgetData = true;
  params.budget = this.getAttribute("data-value");
  $.getJSON("", param, function(repsonse) {
    var colone, coltwo;
    if (response.status) {
      colone = "<dt>Presupuesto</dt>\n<dd>{{  }}</dd>\n<dt>Cliente</dt>\n<dd></dd>\n<dt>Dirección</dt>\n<dd></dd>\n<dt>Observación</dt>\n<dd></dd>";
      coltwo = "<dt>Registrado</dt>\n<dd></dd>\n<dt>Jornada Diaria</dt>\n<dd></dd>\n<dt>F. Entrega</dt>\n<dd></dd>\n<dt>Moneda</dt>\n<dd></dd>";
      return $(".panel-budgets").toggle(800, "linear");
    } else {
      $().toastmessage("showErrorToast", "No se encontraron datos. " + response.raise);
    }
  });
};
