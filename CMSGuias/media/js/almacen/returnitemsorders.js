var app;

app = angular.module('rioApp', ['ngCookies']);

app.config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.factory('rioF', function($http, $cookies) {
  var obj;
  obj = new Object;
  obj.getDetails = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get("", {
      params: options
    });
  };
  return obj;
});

app.controller('rioC', function($scope, rioF) {
  $scope.mat = [];
  angular.element(document).ready(function() {
    $scope.getDetails();
  });
  $scope.checkall = function(mat) {
    if ($scope.all && !$scope.nothing) {
      $scope.mat[mat] = true;
      return true;
    } else {
      $scope.mat[mat] = false;
      return false;
    }
  };
  $scope.getDetails = function() {
    var prm;
    prm = {
      'getorder': true
    };
    rioF.getDetails(prm).success(function(response) {
      if (response.status) {
        $scope.details = response.details;
      } else {
        swal("Error", "" + response.raise, "error");
      }
    });
  };
  $scope.returnItems = function() {
    console.log($scope.mat);
  };
});
