var app;

app = angular.module('guideApp', ['ngCookies']).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.factory('fGuide', function($http, $cookies, $q) {
  var obj;
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  obj = new Object;
  obj.getDetails = function(options) {
    return $http.get('', {
      params: options
    });
  };
  obj.getCarrier = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get('/json/get/carries/', {
      params: options
    });
  };
  obj.getTransport = function(options) {
    return $http.get("/json/get/list/transport/" + options + "/");
  };
  obj.getDriver = function(options) {
    return $http.get("/json/get/list/conductor/" + options + "/", {
      params: options
    });
  };
  obj.saveGuide = function(options) {
    var form;
    if (options == null) {
      options = {};
    }
    form = new FormData;
    form.append('puntollegada', options.puntollegada);
    form.append('traslado', options.traslado);
    form.append('traruc_id', options.traruc_id);
    form.append('condni_id', options.condni_id);
    form.append('nropla_id', options.nropla_id);
    form.append('comment', options.comment);
    form.append('nota', options.nota);
    form.append('saveGuide', true);
    return $http({
      url: "",
      method: "POST",
      data: form,
      transformRequest: angular.identity,
      headers: {
        'Content-Type': undefined
      }
    });
  };
  return obj;
});

app.controller('cGuide', function($scope, $timeout, $q, fGuide) {
  $scope.carrier = '';
  $scope.guide = [];
  angular.element(document).ready(function() {
    angular.element(".datepicker").pickadate({
      container: "body",
      closeOnSelect: true,
      min: new Date(),
      selectMonths: true,
      selectYears: 15,
      format: "yyyy-mm-dd"
    });
    fGuide.getDetails({
      'details': true
    }).success(function(response) {
      if (response.status) {
        $scope.details = response.list;
      }
    });
    fGuide.getCarrier().success(function(response) {
      if (response.status) {
        $scope.carriers = response.carrier;
      }
    });
    fGuide.getTransport($scope.carrier).success(function(response) {
      if (response.status) {
        $scope.transports = response.list;
      }
    });
    fGuide.getDriver($scope.carrier).success(function(response) {
      if (response.status) {
        $scope.drivers = response.list;
      }
    });
  });
  $scope.getdriversandtransport = function($event) {
    fGuide.getDriver($scope.guide['traruc_id']).success(function(response) {
      if (response.status) {
        $scope.drivers = response.list;
      }
    });
    fGuide.getTransport($scope.guide['traruc_id']).success(function(response) {
      if (response.status) {
        $scope.transports = response.list;
      }
    });
  };
  $scope.saveGuide = function() {
    fGuide.saveGuide($scope.guide).success(function(response) {
      if (response.status) {
        $timeout(function() {
          return location.href = '/almacen/list/guide/referral/';
        }, 2600);
        swal({
          title: "Felicidades!",
          text: "Se ha guardado en los cambios.",
          type: "success",
          timer: 2600
        });
      } else {
        swal({
          title: 'Error!',
          text: 'No se ha guardo los datos.',
          type: 'error'
        });
      }
    });
  };
});
