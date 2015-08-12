var app;

app = angular.module('bidApp', ['ngCookies', 'ngSanitize']).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller('bidCtrl', function($scope, $http, $cookies) {
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  angular.element(document).ready(function() {
    console.log('init document');
    $(".modal-trigger").leanModal();
    $scope.getItem();
  });
  $scope.item = {};
  $scope.getItem = function() {
    $http.get("", {
      params: {
        item: true
      }
    }).success(function(response) {
      if (response.status) {
        $scope.item = response.lit[0];
      } else {
        swal("Error", "no se han encontrado datos. " + response.raise, "error");
      }
    });
  };
  $scope.listDetails = function() {
    $http.get("", {
      params: params
    }).success(function(response) {
      if (response.status) {
        $scope.details = response.details;
      } else {
        swal("Alerta!", "No se han encontrado datos. " + response.raise, "warning");
      }
    });
  };
  $scope.actionEdit = function() {
    var params;
    params = details;
    $http({
      url: '',
      method: 'post',
      data: $.param(params)
    }).success(function(response) {
      if (response.status) {
        return $scope.list;
      } else {
        swal("Error!", "No se a podido guardar los cambios. " + response.raise, "error");
      }
    });
  };
  $scope.searchAnalysis = function($event) {
    var params;
    if ($event.keyCode === 13) {
      params = {
        searchBy: $event.currentTarget.name,
        searchVal: $event.currentTarget.value,
        searchAnalysis: true
      };
      $http.get("", {
        params: params
      }).success(function(response) {
        if (response.status) {
          $scope.listAnalysis = response.analysis;
        } else {
          swal("Alerta!", "No hay datos para tu busqueda", "info");
        }
      });
    }
  };
  $scope.addAnalysis = function() {
    $scope.adda = {
      code: this.x.analysis,
      name: this.x.name,
      unit: this.x.unidad,
      performance: this.x.performance,
      amount: this.x.amount
    };
    $("#manalysis").closeModal();
  };
});
