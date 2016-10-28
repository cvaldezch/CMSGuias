(function() {
  'use strict';
  var app, cpFactories;
  app = angular.module('cpApp', ['ngCookies']);
  app.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  });
  cpFactories = function($http, $cookies) {
    var fd, obj;
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    fd = function(options) {
      var form, k, v;
      if (options == null) {
        options = {};
      }
      form = new FormData();
      for (k in options) {
        v = options[k];
        form.append(k, v);
      }
      return form;
    };
    obj = new Object();
    obj.getComplete = function(options) {
      if (options == null) {
        options = {};
      }
      return $http.get("", {
        params: options
      });
    };
    obj.formData = function(options) {
      if (options == null) {
        options = {};
      }
      return $http.post("", fd(options), {
        transformRequest: angular.identity,
        headers: {
          'Content-Type': void 0
        }
      });
    };
    return obj;
  };
  app.factory('cpFactory', cpFactories);
  app.controller('cpCtrl', function($rootScope, $scope, $log, cpFactory) {
    $scope.call = false;
    $scope.mstyle = '';
    $scope.ctrl = {
      'storage': false,
      'operations': false,
      'quality': false,
      'accounting': false,
      'sales': false
    };
    angular.element(document).ready(function() {
      $scope.validArea();
      angular.element('.collapsible').collapsible();
      angular.element('.scrollspy').scrollSpy();
      $scope.sComplete();
    });
    $scope.sComplete = function() {
      cpFactory.getComplete({
        'gcomplete': true
      }).success(function(response) {
        if (response.status) {
          $scope.sh = response.complete;
        } else {
          Materialize.toast("" + response.raise, 2000);
          $scope.sh = response.complete;
        }
      });
    };
    $scope.validArea = function() {
      var x;
      switch ($scope.uarea) {
        case 'administrator' || 'ventas' || 'logistica':
          for (x in $scope.ctrl) {
            $scope.ctrl[x] = true;
          }
          break;
        case 'operaciones':
          $scope.ctrl['operations'] = true;
          break;
        case 'calidad':
          $scope.ctrl['quality'] = true;
          break;
        case 'almacen':
          $scope.ctrl['storage'] = true;
      }
    };
    $scope.storageClosed = function() {
      swal({
        title: "Realmanete desea Cerrar el Almacén?",
        text: '',
        type: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Si!, cerrar',
        confirmButtonColor: "#e82a37",
        closeOnCancel: true,
        closeOnConfirm: true
      }, function(isConfirm) {
        if (isConfirm) {
          $log.info("yes closed");
          cpFactory.formData({
            'storage': true
          }).success(function(response) {
            if (response.status) {
              $scope.sComplete();
              Materialize.toast("<i class='fa fa-check fa-lg green-text'></i>&nbps;Almacén Cerrado", 4000);
            } else {
              Materialize.toast("<i class='fa fa-times fa-lg red-text'></i>&nbps;" + repsonse.raise, 4000);
            }
          });
        } else {
          $scope.$apply(function() {
            $scope.closedstorage = false;
          });
        }
      });
    };
    $scope.letterClosed = function() {
      if (angular.element("#letterup")[0].files.length === 0) {
        Materialize.toast("<i class='fa fa-warning amber-text fa-lg'></i> Debe seleccionar por lo menos un archivo.", 4000);
        return false;
      }
      swal({
        title: "Realmanete desea cargar la Carta de Entrega?",
        text: '',
        type: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Si!, subir',
        confirmButtonColor: "#f82432",
        closeOnCancel: true,
        closeOnConfirm: true
      }, function(isConfirm) {
        var prm;
        if (isConfirm) {
          $log.info("yes closed");
          prm = {
            'operations': true,
            'letter': angular.element("#letterup")[0].files[0]
          };
          cpFactory.formData.success(function(response) {
            if (response.status) {
              $scope.sComplete();
              Materialize.toast("<i class='fa fa-check fa-lg green-text'></i>&nbps;Archivo subido.", 4000);
            } else {
              Materialize.toast("<i class='fa fa-times fa-lg red-text'></i>&nbps;" + repsonse.raise, 4000);
            }
          });
        }
      });
    };
    $scope.$watch('call', function(nw, old) {
      if (nw !== void 0) {
        if (nw === false) {
          $scope.mstyle = {
            'display': 'hide'
          };
        } else {
          $scope.mstyle = {
            'display': 'block'
          };
        }
      }
    });
    $scope.$watch('closedstorage', function(nw, old) {
      if (nw !== void 0) {
        if (nw === true) {
          $scope.storageClosed();
        }
      }
    });
  });
})();
