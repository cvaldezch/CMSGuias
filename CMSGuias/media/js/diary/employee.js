var app;

app = angular.module('EmpApp', ['ngCookies', 'ngSanitize']).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller("empCtrl", function($scope, $http, $cookies) {
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  angular.element(document).ready(function() {
    console.log("ready");
    $('.datepicker').pickadate({
      container: 'body',
      format: 'yyyy-mm-dd'
    });
    $('.modal-trigger').leanModal();
    $scope.listEmployee();
  });
  $scope.predicate = 'fields.firstname';
  $scope.listEmployee = function() {
    $http.get('', {
      params: {
        'list': true
      }
    }).success(function(response) {
      console.log(response);
      if (response.status) {
        $scope.list = response.employee;
      } else {
        swal("Alerta!", "No se han encontrado datos.", "warning");
      }
    });
  };
});
