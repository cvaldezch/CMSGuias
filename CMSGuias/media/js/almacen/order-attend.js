var app, controllers, factories;

app = angular.module('attendApp', ['ngCookies']);

app.config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

factories = function($http, $cookies) {
  var obj;
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  obj = new Object;
  obj.getDetailsOrder = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get("", {
      params: options
    });
  };
  return obj;
};

app.factory('attendFactory', factories);

controllers = function($scope, $timeout, attendFactory) {
  angular.element(document).ready(function() {
    console.log("angular load success!");
  });
  $scope.getDetailsOrder = function() {
    attendFactory.getDetailsOrder({
      'details': true
    }).success(function(response) {
      if (response.status) {
        $scope.sdetails = response.details;
        angular.element("#midetails").openModal();
      } else {
        Materialize.toast('No hay datos para mostrar', 3600, 'rounded');
      }
    });
  };
};

app.controller('attendCtrl', controllers);
