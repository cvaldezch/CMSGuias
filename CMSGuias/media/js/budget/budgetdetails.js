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
    $scope.getItem();
  });
  $scope.getItem = function() {
    $http.get("", {
      params: {
        item: true
      }
    }, function(response) {
      if (response.status) {
        console.log(response);
        $scope.item = response.lit;
      } else {
        swal("Error", "no se han encontrado datos. " + response.raise, "error");
      }
    });
  };
});
