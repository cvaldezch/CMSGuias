var CreateProject, app, deleteProject, openUpdateProject, openWindow, showCountry, showCustomer, showDepartament, showDistrict, showGroup, showProvince, showTable, showaddProject;

$(document).ready(function() {
  $(".btn-save, .panel-pro, div.panel-second").hide();
  $("input[name=comienzo], input[name=fin]").datepicker({
    "changeMonth": true,
    "changeYear": true,
    "showAnim": "slide",
    "dateFormat": "yy-mm-dd"
  });
  $("h4 > a").click(function(event) {
    console.log(this.getAttribute("data-value"));
  });
  tinymce.init({
    selector: "textarea[name=obser]",
    theme: "modern",
    height: 500,
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
    $(".btn-add").on("click", showaddProject);
    $("[name=pais]").on("click", getDepartamentOption);
    $("[name=departamento]").on("click", getProvinceOption);
    $("[name=provincia]").on("click", getDistrictOption);
    $(".btn-country-refresh").on("click", getCountryOption);
    $(".btn-departament-refresh").on("click", getDepartamentOption);
    $(".btn-province-refresh").on("click", getProvinceOption);
    $(".btn-district-refresh").on("click", getDistrictOption);
    $(".btn-add-customers").on("click", showCustomer);
    $(".btn-add-country").on("click", showCountry);
    $(".btn-add-departament").on("click", showDepartament);
    $(".btn-add-province").on("click", showProvince);
    $(".btn-add-district").on("click", showDistrict);
    $(".btn-save").on("click", CreateProject);
    $(".btn-show-edit").on("click", openUpdateProject);
    $(".btn-show-delete").on("click", deleteProject);
  }, 2000);
  $(".btn-link").hover(function() {
    $(this).css("color", "#808080");
  }, function() {
    $(this).css("color", "#000");
  });
  $(".btn-show-group").on("click", showGroup);
  $(".btn-show-table").on("click", showTable);
});

showaddProject = function(event) {
  var $btn;
  $btn = $(this);
  $(".panel-pro").toggle(function() {
    if ($(this).is(":hidden")) {
      $btn.find("span").eq(0).removeClass("glyphicon-remove").addClass("glyphicon-plus");
      $btn.find("span").eq(1).html(" Nuevo Proyecto");
      return $(".btn-save").hide();
    } else {
      $btn.find("span").eq(0).removeClass("glyphicon-plus").addClass("glyphicon-remove");
      $btn.find("span").eq(1).html(" Cancelar");
      return $(".btn-save").show();
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
        $().toastmessage("showNoticeToast", "Se registro el proyecto " + data['nompro'] + " correctamente!");
        return setTimeout(function() {
          return location.reload();
        }, 2000);
      } else {
        return $().toastmessage("showErrorToast", "Error en la transacción " + response.raise + ".");
      }
    });
    return;
  }
};

openUpdateProject = function(event) {
  var pro, url;
  pro = this.value;
  url = "/almacen/keep/project/" + pro + "/edit/";
  openWindow(url);
};

openWindow = function(url) {
  var interval, win;
  win = window.open(url, "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600");
  interval = window.setInterval(function() {
    if (win === null || win.closed) {
      window.clearInterval(interval);
      location.reload;
    }
  }, 1000);
  return win;
};

deleteProject = function() {
  var value;
  value = this.value;
  $().toastmessage("showToast", {
    text: "Eliminar Proyecto, recuerde que al eliminar a " + this.title + " sera permanentemente.<br>Desea Eliminar el Proyecto?",
    sticky: true,
    type: "confirm",
    position: "middle-center",
    buttons: [
      {
        value: 'No'
      }, {
        value: 'Si'
      }
    ],
    success: function(result) {
      var data;
      if (result === "Si") {
        data = {
          "proid": value,
          "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
        };
        $.post("/almacen/keep/project/", data, function(response) {
          if (response.status) {
            if ($("table tbody > tr").length > 1) {
              $(".tr-" + value).remove();
            } else {
              location.reload();
            }
          }
        }, "json");
      }
    }
  });
};

showGroup = function(event) {
  $("div.panel-second").fadeOut();
  return $("div.panel-first").fadeIn();
};

showTable = function(event) {
  $("div.panel-first").fadeOut();
  return $("div.panel-second").fadeIn();
};

app = angular.module('proApp', ['ngSanitize', 'ngCookies']).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller('proCtrl', function($scope, $http, $cookies) {
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  $scope.customers = [];
  angular.element(document).ready(function() {
    $scope.listCustomers();
  });
  $scope.listCustomers = function() {
    var params;
    params = {
      getCustomers: true
    };
    $http.get('', {
      params: params
    }).success(function(response) {
      if (response.status) {
        $scope.customers = response.customers;
        setTimeout(function() {
          $('.collapsible').collapsible();
        }, 400);
      } else {
        console.log("No result. " + response.raise);
      }
    });
  };
  $scope.getProjects = function() {
    var data;
    console.log(this);
    data = {
      getProjects: true,
      customer: this.x.fields.ruccliente.pk
    };
    console.log(data);
    $http.get('', params).success(function(response) {
      if (response.status) {
        $scope[data.customer] = response;
      } else {
        console.log("No data project. " + response.raise);
      }
    });
  };
});
