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
    var fd, ofac;
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    ofac = new Object();
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
    ofac.saveOrder = function(options) {
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
    ofac.editDetails = function(options) {
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
    return ofac;
  });
  app.controller('soCtrl', function($scope, $timeout, $q, soFactory) {
    $scope.projects = [];
    $scope.digv = 0;
    $scope.dstotal = 0;
    $scope.ddsct = 0;
    $scope.dsigv = 0;
    $scope.dtotal = 0;
    $scope.edit = [];
    $scope.dels = [];
    angular.element(document).ready(function() {
      angular.element(".modal-trigger").leanModal();
      angular.element(".chosen-select").chosen({
        width: '100%'
      });
      angular.element("#desc").trumbowyg();
      angular.element('.trumbowyg-editor, .trumbowyg-box').css("min-height", "200px").css("margin", "0px auto");
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
          $scope.units = response.unit;
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
          $timeout(function() {
            $scope.calc();
          }, 600);
        } else {
          Materialize.toast("<i class='fa fa-warning fa-2x amber-text'></i>&nbsp;No hay detalle para mostrar.", 4000);
        }
      });
    };
    $scope.calc = function() {
      var getsubtotal;
      getsubtotal = function() {
        var defer, promises;
        defer = $q.defer();
        promises = 0;
        angular.forEach($scope.details, function(obj) {
          promises += obj.fields.price * obj.fields.quantity;
        });
        defer.resolve(promises);
        return defer.promise;
      };
      getsubtotal().then(function(result) {
        var _stt;
        $scope.dstotal = Number(result.toFixed(3));
        $scope.ddsct = Number((($scope.dstotal * $scope.so.dsct) / 100).toFixed(3));
        _stt = Number(($scope.dstotal - $scope.ddsct).toFixed(3));
        if ($scope.so.sigv === true) {
          $scope.dsigv = Number((($scope.dstotal * $scope.digv) / 100).toFixed(3));
          _stt += $scope.dsigv;
        }
        $scope.dtotal = _stt;
      });
    };
    $scope.showEdit = function(pk, obj) {
      angular.element("#desc").trumbowyg('html', obj.description);
      $scope.edit.pk = pk;
      $scope.edit.quantity = obj.quantity;
      $scope.edit.price = Number(obj.price);
      $scope.edit.unit = obj.unit;
      angular.element("#eDetails").openModal();
    };
    $scope.applyDetails = function() {
      $scope.edit.description = angular.element("#desc").trumbowyg('html');
      if ($scope.edit.hasOwnProperty("pk")) {
        angular.forEach($scope.details, function(obj) {
          if (obj.pk === $scope.edit.pk) {
            obj.fields = $scope.edit;
          }
        });
      } else {
        $scope.details.push({
          pk: $scope.details.length + 1,
          model: "add",
          fields: $scope.edit
        });
      }
      $scope.calc();
      $scope.eClean();
    };
    $scope.eClean = function() {
      $scope.edit = [];
      angular.element("#desc").trumbowyg('html', '');
    };
    $scope.delItem = function(pk) {
      swal({
        title: 'Realmente desea eliminar el item?',
        text: '',
        type: 'warning',
        showCancelButton: true,
        closeOnCancel: true,
        closeOnConfirm: true,
        cancelButtonText: 'No!',
        confirmButtonText: 'Si!, eliminar',
        confirmButtonColor: '#dd6b55'
      }, function(isConfirm) {
        if (isConfirm) {
          angular.forEach($scope.details, function(obj, index) {
            if (obj.pk === pk) {
              $scope.dels.push(obj.pk);
              $scope.details.splice(index, 1);
              $scope.$apply();
              Materialize.toast("<i class='fa fa-fire fa-lg red-text'></i>&nbsp;Item eliminado!", 2600);
              $scope.calc();
            }
          });
        }
      });
    };
    $scope.saveOrderService = function() {
      swal({
        title: 'Desea guardar los datos?',
        text: '',
        type: 'warning',
        confirmButtonText: 'Si!, Guardar',
        confirmButtonColor: '#dd6b55',
        cancelButtonText: 'No',
        showCancelButton: true,
        closeOnConfirm: true,
        closeOnCancel: true
      }, function(isConfirm) {
        if (isConfirm) {
          soFactory.saveOrder().success(function(response) {
            if (response.status) {
              Materialize.toast("<i class='fa fa-check fa-lg green-text'></i> &nbsp;Se actualizo correctamente!", 2500);
              $timeout(function() {
                location.href = '/logistics/services/orders/';
              }, 2500);
            } else {
              Materialize.toast("NO se han guardado los datos", 4000);
            }
          });
        }
      });
    };
    $scope.$watch('so.dsct', function(nw, old) {
      if (nw !== old) {
        $scope.calc();
      }
    });
    $scope.$watch('so.sigv', function(nw, old) {
      if (nw !== void 0) {
        if (nw === true) {
          $scope.digv = $scope.vigv;
        } else {
          $scope.digv = 0;
          $scope.dsigv = 0;
        }
        $scope.calc();
      }
    });
    $scope.$watch('so.currency', function(nw, old) {
      if (nw !== void 0) {
        return $scope.lcur = angular.element("#currency option:selected").text();
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
