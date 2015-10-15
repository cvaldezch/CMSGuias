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
    $scope.getListAreaMaterials();
    $scope.getProject();
    $('.modal-trigger').leanModal();
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
        console.log(response);
        $scope.dsmaterials = response.list;
        console.log($scope.dsmaterials);
      } else {
        swal("Error!", "al obtener la lista de materiales del área", "error");
      }
    });
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
    console.log(data);
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
        $scope.ascsector = response.sector;
      } else {
        swal("Error", "No se pudo cargar los datos del sector", "error");
      }
    });
  };
});
