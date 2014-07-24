var CreateProject, showCountry, showCustomer, showDepartament, showDistrict, showProvince, showaddProject;

$(document).ready(function() {
  $(".btn-save, .panel-pro").hide();
  $("input[name=comienzo], input[name=fin]").datepicker({
    "changeMonth": true,
    "changeYear": true,
    "showAnim": "slide",
    "dateFormat": "yy-mm-dd"
  });
  $(".btn-open > span").mouseenter(function(event) {
    event.preventDefault();
    $(this).removeClass("glyphicon-folder-close").addClass("glyphicon-folder-open");
  }).mouseout(function(event) {
    event.preventDefault();
    $(this).removeClass("glyphicon-folder-open").addClass("glyphicon-folder-close");
  });
  tinymce.init({
    selector: "textarea[name=obser]",
    theme: "modern",
    menubar: false,
    statusbar: false,
    plugins: "link contextmenu fullscreen",
    fullpage_default_doctype: "<!DOCTYPE html>",
    font_size_style_values: "10px,12px,13px,14px,16px,18px,20px",
    toolbar1: "styleselect | fontsizeselect | fullscreen |",
    toolbar2: "undo redo | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent |"
  });
  setTimeout(function() {
    $(document).find("#mceu_2").click(function(event) {
      if ($(this).attr("aria-pressed") === "false" || $(this).attr("aria-pressed") === void 0) {
        $(".navbar").hide();
      } else if ($(this).attr("aria-pressed") === "true") {
        $(".navbar").show();
      }
    });
  }, 2000);
  $("[name=pais]").on("click", getDepartamentOption);
  $("[name=departamento]").on("click", getProvinceOption);
  $("[name=provincia]").on("click", getDistrictOption);
  $(".btn-country-refresh").on("click", getCountryOption);
  $(".btn-departament-refresh").on("click", getDepartamentOption);
  $(".btn-province-refresh").on("click", getProvinceOption);
  $(".btn-district-refresh").on("click", getDistrictOption);
  $(".btn-add").on("click", showaddProject);
  $(".btn-add-customers").on("click", showCustomer);
  $(".btn-add-country").on("click", showCountry);
  $(".btn-add-departament").on("click", showDepartament);
  $(".btn-add-province").on("click", showProvince);
  $(".btn-add-district").on("click", showDistrict);
  $(".btn-save").on("click", CreateProject);
});

showaddProject = function(event) {
  var $btn;
  event.preventDefault();
  $btn = $(this);
  $(".panel-pro").toggle(function() {
    if ($(this).is(":hidden")) {
      $btn.find("span").eq(0).removeClass("glyphicon-remove").addClass("glyphicon-plus");
      $btn.find("span").eq(1).html(" Nuevo Proyecto");
      $(".btn-save").hide();
    } else {
      $btn.find("span").eq(0).removeClass("glyphicon-plus").addClass("glyphicon-remove");
      $btn.find("span").eq(1).html(" Cancelar");
      $(".btn-save").show();
    }
  });
};

showCustomer = function(event) {
  var url;
  event.preventDefault();
  url = "/customers/new/";
  return window.open(url, "Customers", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600");
};

showCountry = function(event) {
  var url;
  event.preventDefault();
  url = "/country/new/";
  return window.open(url, "Country", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=500");
};

showDepartament = function(event) {
  var url;
  event.preventDefault();
  url = "/departament/new/";
  return window.open(url, "Departament", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=500");
};

showProvince = function(event) {
  var url;
  event.preventDefault();
  url = "/province/new/";
  return window.open(url, "Province", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=500");
};

showDistrict = function(event) {
  var url;
  event.preventDefault();
  url = "/district/new/";
  return window.open(url, "District", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=500");
};

CreateProject = function(event) {
  var data, pass;
  pass = false;
  data = new Object();
  $(".panel-pro").find("input, select").each(function() {
    if (this.value === "" || this.value === null) {
      console.log(this.name);
      this.focus();
      pass = false;
      $().toastmessage("showWarningToast", "campo vacio " + this.name + ".");
      return pass;
    } else {
      data[this.name] = $(this).val();
      pass = true;
    }
  });
  console.log(data);
  if (pass) {
    data['obser'] = $("#obser_ifr").contents().find("body").html();
    data['type'] = "new";
    $.post("", data, function(response) {
      if (response.status) {
        return $().toastmessage("showNoticeToast", "Se registro el proyecto " + data['nompro'] + " correctamente!");
      } else {
        return $().toastmessage("showErrorToast", "Error en la transacción " + response.raise + ".");
      }
    });
  }
};