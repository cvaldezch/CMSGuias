var app;

app = angular.module('dsApp', ['ngCookies']).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  return $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}).directive('stringToNumber', function() {
  return {
    require: 'ngModel',
    link: function(scope, element, attrs, ngModel) {
      ngModel.$parsers.push(function(value) {
        return '' + value;
      });
      ngModel.$formatters.push(function(value) {
        return parseFloat(value, 10);
      });
    }
  };
});

app.controller('DSCtrl', function($scope, $http, $cookies) {
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  angular.element(document).ready(function() {
    var $table;
    $('.modal-trigger').leanModal();
    $scope.getListAreaMaterials();
    $scope.getProject();
    $table = $(".floatThead");
    $table.floatThead({
      position: 'absolute',
      top: 65,
      scrollContainer: function($table) {
        return $table.closest('.wrapper');
      }
    });
  });
  $scope.getListAreaMaterials = function() {
    var data;
    data = {
      dslist: true
    };
    $http.get("", {
      params: data
    }).success(function(response) {
      if (response.status) {
        $scope.dsmaterials = response.list;
        $(".floatThead").floatThead('reflow');
        $scope.inDropdownTable(".table-withoutApproved");
      } else {
        swal("Error!", "al obtener la lista de materiales del área", "error");
      }
    });
  };
  $scope.inDropdownTable = function(table) {
    console.log($(table + " > tbody > tr").length);
    if ($(table + " > tbody > tr").length > 0) {
      $('.dropdown-button').dropdown();
      return false;
    } else {
      setTimeout(function() {
        return $scope.inDropdownTable(table);
      }, 1400);
    }
  };
  $scope.saveMateial = function() {
    var data;
    data = $scope.mat;
    data.savepmat = true;
    data.ppurchase = $("[name=precio]").val();
    data.psales = $("[name=sales]").val();
    data.brand = $("[name=brand]").val();
    data.model = $("[name=model]").val();
    data.code = $(".id-mat").text();
    if (data.quantity <= 0) {
      swal("Alerta!", "Debe de ingresar una cantidad!", "warning");
      data.savepmat = false;
    }
    if (data.ppurchase <= 0) {
      swal("Alerta!", "Debe de ingresar un precio de Compra!", "warning");
      data.savepmat = false;
    }
    if (data.psales <= 0) {
      swal("Alerta!", "Debe de ingresar un precio de Venta!", "warning");
      data.savepmat = false;
    }
    if (data.savepmat) {
      $http({
        url: "",
        data: $.param(data),
        method: "post"
      }).success(function(response) {
        if (response.status) {
          $scope.getListAreaMaterials();
        } else {
          swal("Error", " No se guardado los datos", "error");
        }
      });
    }
  };
  $scope.getProject = function() {
    $http.get("/sales/projects/", {
      params: {
        'ascAllProjects': true
      }
    }).success(function(response) {
      if (response.status) {
        $scope.ascprojects = response.projects;
      } else {
        swal("Error", "No se a cargado los proyectos", "error");
      }
    });
  };
  $scope.getsector = function(project) {
    $http.get("/sales/projects/sectors/crud/", {
      params: {
        'pro': project,
        'sub': ''
      }
    }).success(function(response) {
      if (response.status) {
        $scope.ascsector = response.list;
      } else {
        swal("Error", "No se pudo cargar los datos del sector", "error");
      }
    });
  };
  $scope.ccopyps = function(sector) {
    swal({
      title: 'Copiar lista de Sector?',
      text: 'Realmente desea realizar la copia.',
      type: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#dd6b55',
      confirmButtonText: 'Si, Copiar',
      cancelButtonText: 'No, Cancelar',
      closeOnConfirm: true,
      closeOnCancel: true
    }, function(isConfirm) {
      var data;
      if (isConfirm) {
        if (sector) {
          data = {
            project: sector.substring(0, 7),
            sector: sector,
            copysector: true
          };
          $http({
            url: "",
            method: "post",
            data: $.param(data)
          }).success(function(response) {
            if (response.status) {
              location.reload();
            } else {
              swal("Error", "No se a guardado los datos.", "error");
            }
          });
        } else {
          swal("Alerta!", "El código de sector no es valido.", "warning");
        }
      }
    });
  };
  $scope.delAreaMA = function() {
    swal({
      title: 'Realmente desea eliminar?',
      text: 'toda la lista de materiales de esta area.',
      type: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#dd6b55',
      confirmButtonText: 'Si, Eliminar',
      cancelButtonText: 'No, Cancelar'
    }, function(isConfirm) {
      if (isConfirm) {
        $http({
          url: "",
          data: $.param({
            'delAreaMA': true
          }),
          method: 'post'
        }).success(function(response) {
          if (response.status) {
            location.reload();
          } else {
            swal("Alerta", "no se elimino los materiales del área", "warning");
          }
        });
      }
    });
  };
  $scope.$watch('ascsector', function() {
    if ($scope.ascsector) {
      $scope.fsl = true;
      $scope.fpl = true;
    }
  });
});
