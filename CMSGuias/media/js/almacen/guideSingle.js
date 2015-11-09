var app;

app = angular.module('SGuideApp', ['ngCookies']).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller('SGuideCtrl', function($scope, $http, $cookies) {
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  angular.element(document).ready(function() {
    $('.datepicker').pickadate({
      selectMonths: true,
      selectYears: 15,
      format: 'yyyy-mm-dd'
    });
    $scope.customersList();
    $scope.carrierList();
  });
  $scope.customersList = function() {
    $http.get('', {
      params: {
        customers: true
      }
    }).success(function(response) {
      if (response.status) {
        $scope.customers = response.customers;
      } else {
        swal("Error", "datos de los clientes. " + response.raise, "error");
      }
    });
  };
  $scope.carrierList = function() {
    $http.get('', {
      params: {
        carrier: true
      }
    }).success(function(response) {
      if (response.status) {
        $scope.carriers = response.carrier;
      } else {
        swal("Error", "datos de los Transportista. " + response.raise, "error");
      }
    });
  };
  $scope.detCarriers = function($event) {
    var data;
    data = {
      tra: $event.currentTarget.value,
      detCarrier: true
    };
    return $http.get('', {
      params: data
    }).success(function(response) {
      if (response.status) {
        $scope.drivers = response.driver;
        $scope.transports = response.transport;
      } else {
        swal("Error", "datos de los Transportista. " + response.raise, "error");
      }
    });
  };
});
