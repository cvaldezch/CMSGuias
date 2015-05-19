var saveBudget, showBudget, showSearchBudget, vali;

$(function() {
  $(".panel-sbudget, .panel-details-budget").hide();
  $("[name=finish]").datepicker({
    changeMonth: true,
    changeYear: true,
    minDate: "0",
    dateFormat: "dd-mm-yy"
  });
  $("[name=showBudget]").on("click", showBudget);
  $(".bsearchbudget").on("click", showSearchBudget);
  $("[name=observation]").tny;
  tinymce.init({
    selector: "textarea[name=observation]",
    menubar: false,
    toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image"
  });
  $.validator.setDefaults({
    debug: true
  });
  $("#newBudget").validate({
    onfocusout: false,
    onclick: false,
    errorElement: "div",
    errorPlacement: function(error, element) {
      console.log(element);
      element.appendTo("div#errors2");
    },
    rules: {
      name: {
        required: true
      }
    },
    messages: {
      name: {
        required: "Este campo no puede estas vacio!"
      }
    }
  });
});

showBudget = function(event) {
  $("#nbudget").modal("show");
};

showSearchBudget = function(event) {
  $(".panel-sbudget").toggle("linear");
};

saveBudget = function(event) {
  var params;
  params = new Object;
  params.name = $("[name=name]").val();
  params.address = $("[name=address]").val();
  params.country = $("[name=pais]").val();
  params.departament = $("[name=departamento]").val();
  params.province = $("[name=provincia]").val();
  params.district = $("[name=distrito]").val();
  params.hours = $("[nam=hours]").val();
  params.finish = $("[name=finish]").val();
  params.base = $("[name=base]").val();
  params.offer = $("[name=offer]").val();
  params.currency = $("[name=currency]").val();
  params.exchange = $("[name=exchange]").val();
  params.observation = $("#observation_ifr").contents().find("body").html();
};

vali = function(event) {
  $(".modal-body").validate({
    onfocusout: true,
    onclick: false,
    errorElement: "div",
    errorPlacement: function(error, element) {
      error.appendTo("div#errors2");
    },
    rules: {
      "name": {
        required: true
      },
      messages: {
        "name": {
          required: "Este campo no puede estas vacio!"
        }
      }
    }
  });
};
