var app, controller, factories;

app = angular.module('inventoryApp', ['ngCookies']);

app.config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.directive('fileModel', function($parse) {
  return {
    restrict: 'A',
    link: function(scope, element, attrs) {
      var model, modelSetter;
      model = $parse(attrs.fileModel);
      modelSetter = model.assign;
      element.bind('change', function() {
        scope.$apply(function() {
          modelSetter(scope, element[0].files[0]);
        });
      });
    }
  };
});

factories = function($http, $cookies) {
  var formd, obj;
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  obj = new Object;
  formd = function(options) {
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
  obj.getMaterials = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get("", {
      params: options
    });
  };
  obj.getDetails = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get("", {
      params: options
    });
  };
  obj.loadInventory = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.post("", formd(options), {
      transformRequest: angular.identity,
      headers: {
        'Content-Type': undefined
      }
    });
  };
  obj.delInventory = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.post("", formd(options), {
      transformRequest: angular.identity,
      headers: {
        'Content-Type': void 0
      }
    });
  };
  obj.sendOrder = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.post("", formd(options), {
      transformRequest: angular.identity,
      headers: {
        'content-Type': void 0
      }
    });
  };
  return obj;
};

app.factory('inventoryFactory', factories);

controller = function($scope, $timeout, $q, inventoryFactory) {
  $scope.lstinv = [];
  $scope.parea = '';
  $scope.pcargo = '';
  angular.element(document).ready(function() {
    angular.element('.modal-trigger').leanModal({
      dismissible: false
    });
  });
  $scope.getMaterials = function($event) {
    var prms;
    if ($event.keyCode === 13) {
      prms = {
        'getmat': true,
        'desc': $scope.desc
      };
      inventoryFactory.getMaterials(prms).success(function(response) {
        if (response.status) {
          console.log(response);
          $scope.lstinv = response.materials;
          console.info($scope.lstinv);
        } else {
          console.error("Error " + response.raise);
        }
      });
    }
  };
  $scope.getDetails = function(matid) {
    var prms;
    prms = {
      details: true,
      materials: matid
    };
    inventoryFactory.getDetails(prms).success(function(response) {
      if (response.status) {
        $scope.details = response.materials;
        $scope.amount = response.amount;
        angular.element("#mdetails").openModal({
          dismissible: false
        });
      } else {
        console.error("Error " + response.raise);
      }
    });
  };
  $scope.delInventory = function() {
    swal({
      title: 'Eliminar todo el Inventario?',
      text: '',
      type: 'warning',
      confirmButtonColor: "#dd6b55",
      confirmButtonText: "Si!, eliminar",
      showCancelButton: true,
      closeOnConfirm: true,
      closeOnCancel: true
    }, function(isConfirm) {
      var prms;
      console.log(isConfirm);
      if (isConfirm) {
        $scope.bdel = !$scope.bdel;
        prms = {
          'delInventory': true
        };
        inventoryFactory.delInventory(prms).success(function(response) {
          console.info(response);
          if (response.status && typeof response.raise === 'boolean') {
            Materialize.toast("<i class='fa fa-check fa-2x green-text'></i>&nbsp;&nbsp;Eliminación Completa!", 4000);
            $timeout(function() {
              location.reload();
            }, 4000);
          } else {
            $scope.bdel = false;
            Materialize.toast("<i class='fa fa-times fa-2x red-text'></i>&nbsp;&nbsp;Eliminación abortada!&nbsp;<p>" + response.raise + "</p>", 4000);
          }
        });
        console.log("Inventory Delete");
      }
    });
  };
  $scope.loadInventory = function() {
    swal({
      title: 'Desea cargar al Inventario?',
      text: '',
      type: 'warning',
      confirmButtonColor: "#dd6b55",
      confirmButtonText: "Si!, cargar",
      showCancelButton: true,
      closeOnConfirm: true,
      closeOnCancel: true
    }, function(isConfirm) {
      var prms;
      $scope.bload = !$scope.bload;
      if (isConfirm) {
        if ($scope.fload === undefined) {
          Materialize.toast("<i class='fa fa-exclamation amber-text fa-2x'></i>&nbsp;Seleccione un Archivo!", 5000);
          return false;
        }
        prms = {
          loadInventory: true,
          fload: $scope.fload
        };
        inventoryFactory.loadInventory(prms).success(function(response) {
          if (response.status) {
            Materialize.toast("<i class='fa fa-check green-text'></i>&nbsp; Archivo Cargado!", 4000);
            $timeout(function() {
              angular.element("#mupload").closeModal();
              $scope.bload = !$scope.bload;
            }, 4000);
          } else {
            $scope.bload = !$scope.bload;
            Materialize.toast("<i class='fa fa-times red-text'></i>&nbsp;Error al Cargar los datos. " + response.raise, 4000);
          }
        });
      }
    });
  };
  $scope.loadOrderStk = function() {
    swal({
      title: "Ingrese Nro de Pedido:",
      type: "input",
      showCancelButton: true,
      closeOnConfirm: true,
      animation: 'slide-from-top',
      inputPlaceholder: "PEAA000000"
    }, function(inputval) {
      var prms;
      if (inputval === false) {
        return false;
      }
      if (inputval === "") {
        Materialize.toast("No puede estar Vacio!", 3600);
        return false;
      }
      if (inputval.length < 10) {
        Materialize.toast("Formato Incorrencto!", 3600);
        return false;
      }
      prms = {
        putorder: true,
        order: inputval
      };
      return inventoryFactory.sendOrder(prms).success(function(response) {
        if (response.status) {
          Materialize.toast("Tarea Finalizada!", 3600);
          $timeout(function() {
            return location.reload();
          }, 3600);
        } else {
          Materialize.toast("Error! " + response.raise, 3600);
        }
      });
    });
  };
};

app.controller('inventoryCtrl', controller);
