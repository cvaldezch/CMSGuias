var CreateProject, app, deleteProject, openUpdateProject, openWindow, showCountry, showCustomer, showDepartament, showDistrict, showProvince, showaddProject;

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
      swal("Alerta!", "campo vacio " + this.name + ".", "warning");
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
        swal("Felicidades!", "Se registro el proyecto " + data['nompro'] + " correctamente!", "success");
        return setTimeout(function() {
          return location.reload();
        }, 2000);
      } else {
        return swal("Alerta!", "Error en la transacción " + response.raise + ".", "warning");
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

app = angular.module('proApp', ['ngSanitize', 'ngCookies']).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller('proCtrl', function($scope, $http, $cookies) {
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  $scope.sfcustomers = false;
  $scope.sfprojects = false;
  $scope.pcustomers = true;
  $scope.pprojects = false;
  $scope.tadmin = false;
  angular.element(document).ready(function() {
    $scope.lCustomersCbox();
    $scope.listCustomers();
    $scope.permission = angular.element("[name=permission]").val();
    if ($scope.permission === 'administrator' || $scope.permission === 'ventas') {
      $scope.tadmin = true;
    }
    if ($scope.permission === 'operaciones') {
      $scope.pprojects = true;
      $scope.pcustomers = false;
      $scope.sfcustomers = false;
      $scope.sfprojects = false;
      $scope.sTable();
    }
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
  $scope.lCustomersCbox = function() {
    var params;
    params = {
      lCustomers: 'true'
    };
    $http.get('', {
      params: params
    }).success(function(response) {
      if (response.status) {
        $scope.ccustomers = response.customers;
      } else {
        swal("Error", "No hay clientes para cargar.", "error");
      }
    });
  };
  $scope.getProjects = function() {
    var data;
    data = {
      getProjects: true,
      customer: this.x.fields.ruccliente.pk
    };
    if (!$("#" + data.customer).parent().is(":visible")) {
      $('.collapsible').collapsible();
      $http.get('', {
        params: data
      }).success(function(response) {
        if (response.status) {
          $("#" + data.customer).html(Mustache.render("{{#projects}} <li class=\"collection-item avatar\" ondblclick=\"location.href='manager/{{pk}}/'\">\n  <i class=\"fa fa-building circle\" onClick=\"location.href='manager/{{pk}}/'\"></i>\n  <span class=\"title\"><strong>{{pk}} - {{fields.nompro}}</strong></span>\n  <div class=\"row\">\n    <div class=\"col l6\">\n      <strong>Contacto: </strong> {{fields.contact}}\n    </div>\n    <div class=\"col l6\"><strong>Correo: </strong> {{fields.email}}</div>\n    <div class=\"col l4\">\n      <strong>Registrado: </strong> {{fields.registrado}}\n    </div>\n    <div class=\"col l4\">\n      <strong>Inicio: </strong> {{fields.comienzo}}\n    </div>\n    <div class=\"col l4\">\n      <strong>Termino: </strong> {{fields.fin}}\n    </div>\n  </div>\n  <a href=\"/almacen/keep/project/{{pk}}/edit/\" data-ng-show=\"tadmin\" target=\"popup\" class=\"secondary-content grey-text text-darken-3s " + (!$scope.tadmin ? 'hide' : void 0) + "\"><i class=\"fa fa-edit\"></i></a>\n</li>{{/projects}}", response));
        } else {
          console.log("No data project. " + response.raise);
        }
      });
    }
  };
  $scope.ProjectsAll = function() {
    var data;
    data = {
      allProjects: true
    };
    $http.get('', {
      params: data
    }).success(function(response) {
      if (response.status) {
        $scope.allprojects = response.projects;
      } else {
        console.log("error data. " + response.raise);
      }
    });
  };
  $scope.showFilter = function() {
    if ($scope.pcustomers) {
      $scope.sfcustomers = !$scope.sfcustomers;
    }
    if ($scope.pprojects) {
      $scope.sfprojects = !$scope.sfprojects;
    }
  };
  $scope.sTable = function() {
    var row;
    row = angular.element("#lprojects > tbody > tr");
    if (!row.length) {
      $scope.ProjectsAll();
    }
  };
  $scope.$watch('scustomers', function() {
    $('.collapsible').collapsible();
  });
  $scope.$watch('permission', function() {
    console.log($scope.permission);
    console.log($scope.tadmin);
  });
});
