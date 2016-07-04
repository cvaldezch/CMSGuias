var app;

app = angular.module('rioApp', ['ngCookies']);

app.config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.directive('minandmax', function($parse) {
  return {
    restrict: 'A',
    require: 'ngModel',
    link: function(scope, element, attrs, ctrl) {
      element.bind('change', function(event) {
        if (parseFloat(ctrl.$viewValue < parseFloat(attrs.min || parseFloat(ctrl.$viewValue > parseFloat(attrs.max))))) {
          scope.valid = false;
          ctrl.$setViewValue(attrs.max);
          ctrl.$render();
          scope.$apply();
          Materialize.toast('El valor no es valido!', 4000);
        } else {
          scope.valid = true;
        }
      });
    }
  };
});

app.factory('rioF', function($http, $cookies) {
  var convertForm, obj;
  obj = new Object;
  convertForm = function(options) {
    var form;
    if (options == null) {
      options = {};
    }
    form = new FormData;
    angular.forEach(options, function(val, key) {
      form.append(key, val);
    });
    return form;
  };
  obj.getDetails = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get("", {
      params: options
    });
  };
  obj.returnList = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.post("", convertForm(options), {
      transformRequest: angular.identity,
      headers: {
        'Content-Type': void 0
      }
    });
  };
  return obj;
});

app.controller('rioC', function($scope, rioF) {
  $scope.mat = [];
  $scope.quantity = [];
  $scope.valid = true;
  angular.element(document).ready(function() {
    $scope.getDetails();
  });
  $scope.checkall = function() {
    angular.forEach($scope.mat, function(value, key) {
      $scope.mat[key] = $scope.selAll.chk;
    });
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
    var tmp;
    tmp = new Array;
    $scope.datareturn = tmp;
    angular.forEach($scope.mat, function(value, key) {
      if (value === true) {
        angular.forEach($scope.details, function(obj, ik) {
          if (obj.pk === key) {
            console.log(obj.pk);
            console.info(key);
            tmp.push({
              'id': obj.pk,
              'materials': obj.fields.materiales.pk,
              'name': obj.fields.materiales.fields.matnom + " " + obj.fields.materiales.fields.matmed,
              'unit': obj.fields.materiales.fields.unidad,
              'brand': obj.fields.brand.fields.brand,
              'brand_id': obj.fields.brand.pk,
              'model': obj.fields.model.fields.model,
              'model_id': obj.fields.model.pk,
              'quantity': $scope.quantity[obj.pk]
            });
          }
        });
      }
    });
    $scope.datareturn = tmp;
    angular.element("#mview").openModal();
  };
  $scope.sendReturnList = function() {
    swal({
      title: "Esta seguro?",
      text: "Regresar los materiales a la lista de proyecto.",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: '#dd6b55',
      confirmButtonText: 'Si!, Retornar',
      cancelButtonText: 'No!',
      closeOnConfirm: true
    }, function(isConfirm) {
      var prm;
      if (isConfirm) {
        prm = {
          'details': JSON.stringify($scope.datareturn),
          'saveReturn': true
        };
        rioF.returnList(prm).success(function(response) {
          if (response.status) {
            Materialize.toast("Se ha devuelto los materiales seleccionados.", 4000);
          } else {
            swal("Error!", "" + response.raise, "error");
          }
        });
      }
    });
  };
});
