(function() {
  'use strict';
  var app;
  app = angular.module("soApp", ['ngCookies', 'ngSanitize']);
  app.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  });
  app.factory('soFactory', function($http, $cookies) {
    var ofac;
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    ofac = new Object();
    ofac.getData = function(options) {
      if (options == null) {
        options = {};
      }
      return $http.get("", {
        params: options
      });
    };
    ofac.getDetails = function(options) {
      if (options == null) {
        options = {};
      }
      return $http.get("", {
        params: options
      });
    };
    ofac.getLetter = function(options) {
      if (options == null) {
        options = {};
      }
      return $http.get("", {
        params: options
      });
    };
    return ofac;
  });
  app.controller('soCtrl', function($scope, $timeout, soFactory) {
    $scope.projects = [];
    $scope.digv = 0;
    $scope.dstotal = 0;
    $scope.dtotal = 0;
    angular.element(document).ready(function() {
      angular.element(".chosen-select").chosen({
        width: '100%'
      });
      $scope.loadData();
    });
    $scope.loadData = function() {
      var prm;
      prm = {
        load: true
      };
      soFactory.getData(prm).success(function(response) {
        if (response.status) {
          $scope.loadDetails();
          $scope.so = response.data;
          $scope.projects = response.projects;
          $scope.suppliers = response.supplier;
          $scope.documents = response.document;
          $scope.methods = response.method;
          $scope.currencys = response.currencys;
          $scope.authorizeds = response.authorized;
          $scope.vigv = response.vigv;
          $timeout(function() {
            return angular.element(".chosen-select").trigger("chosen:updated");
          }, 800);
        } else {
          Materialize.toast("<i class='fa fa-warning fa-2x amber-text'></i>&nbsp; No se ha cargado los datos!", 4000);
        }
      });
    };
    $scope.loadDetails = function() {
      var prm;
      prm = {
        details: true
      };
      soFactory.getDetails(prm).success(function(response) {
        if (response.status) {
          $scope.details = response.details;
          $scope.calc();
        } else {
          Materialize.toast("<i class='fa fa-warning fa-2x amber-text'></i>&nbsp;No hay detalle para mostrar.", 4000);
        }
      });
    };
    $scope.calc = function() {
      angular.forEach($scope.details, function(obj) {
        $scope.dtotal += obj.fields.price * obj.fields.quantity;
      });
    };
    $scope.$watch('so.sigv', function(nw, old) {
      if (nw === true) {
        return $scope.digv = $scope.vigv;
      } else {
        return $scope.digv = 0;
      }
    });
    $scope.$watch('dtotal', function(nw, old) {
      var prm;
      if (nw !== old) {
        $scope.dtotal = parseFloat($scope.dtotal).toFixed(2);
        prm = {
          'lnumber': true,
          'number': $scope.dtotal
        };
        soFactory.getLetter(prm).success(function(response) {
          if (response.status) {
            $scope.letter = response.letter;
            $scope.lcur = angular.element("#currency option:selected").text();
          }
        });
      }
    });
  });
})();
