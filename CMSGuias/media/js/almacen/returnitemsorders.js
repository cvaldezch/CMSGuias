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
    scope: '@',
    link: function(scope, element, attrs, ctrl) {
      element.bind('change', function(event) {
        if (parseFloat(attrs.$$element[0].value) < parseFloat(attrs.min) || parseFloat(attrs.$$element[0].value) > parseFloat(attrs.max)) {
          Materialize.toast('El valor no es valido!', 4000);
          scope.valid = false;
          ctrl.$setViewValue(parseFloat(attrs.max));
          ctrl.$render();
          scope.$apply();
          console.log(scope);
        } else {
          scope.valid = true;
        }
      });
    }
  };
});

app.directive('status', function($parse) {
  return {
    require: 'ngModel',
    link: function(scope, element, attrs, ngModel) {
      scope.$watch(function() {
        return ngModel.$modelValue;
      }, function(newValue) {
        var el;
        el = document.getElementsByName("" + attrs.id);
        if (newValue === true) {
          angular.forEach(el, function(val) {
            return val.value = val.attributes.max.value;
          });
          console.log("change data");
        } else {
          angular.forEach(el, function(val) {
            val.value = 0;
          });
        }
        return console.log(newValue);
      });
    }
  };
});

app.directive('tmandm', function($parse) {
  return {
    link: function(scope, element, attrs, ngModel) {
      element.bind('change, click', function(event) {
        var max, min, val;
        console.log(element);
        val = parseFloat(element.context.value);
        max = parseFloat(attrs.max);
        min = parseFloat(attrs.min);
        if (val > max) {
          element.context.value = max;
          return;
        }
        if (val < min) {
          element.context.value = min;
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
  obj.getNiples = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get('', {
      params: options
    });
  };
  return obj;
});

app.controller('rioC', function($scope, rioF) {
  $scope.mat = [];
  $scope.quantity = [];
  $scope.valid = true;
  $scope.showNipple = false;
  $scope.vnip = false;
  $scope.np = [];
  $scope.dnp = [];
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
    if (!$scope.showNipple && !$scope.vnip) {
      $scope.getNipples();
      return false;
    } else {
      swal({
        title: "Esta seguro?",
        text: "Regresar los materiales a la lista de proyecto.",
        type: "input",
        showCancelButton: true,
        cancelButtonText: 'No!',
        confirmButtonColor: '#dd6b55',
        confirmButtonText: 'Si!, Retornar',
        showLoaderOnConfirm: true,
        closeOnConfirm: false,
        animation: "slide-from-top",
        inputPlaceholder: "Observación"
      }, function(inputValue) {
        var prm;
        if (inputValue === false) {
          return false;
        }
        if (inputValue === "") {
          swal.showInputError("Nesecitas ingresar una Observación.");
          return false;
        }
        if (inputValue !== "") {
          prm = {
            'details': JSON.stringify($scope.datareturn),
            'saveReturn': true,
            'observation': inputValue,
            'nip': new Array()
          };
          angular.forEach($scope.datareturn, function(value, keys) {
            var el, obj1, tmp;
            el = document.getElementsByName(value.materials);
            if (el.length > 0) {
              tmp = new Array;
              angular.forEach(el, function(val) {
                console.log(prm['nip']["" + value.materials]);
                tmp.push({
                  'id': val.attributes.id.value,
                  'materials': value.materials,
                  'quantity': val.value,
                  'meter': val.attributes.metrado.value,
                  'type': val.attributes.nip.value,
                  'import': parseFloat(val.value) * parseFloat(val.attributes.metrado.value)
                });
              });
              prm['nip'].push((
                obj1 = {},
                obj1["" + value.materials] = tmp,
                obj1
              ));
            }
          });
          prm['nip'] = JSON.stringify(prm['nip']);
          rioF.returnList(prm).success(function(response) {
            if (response.status) {
              Materialize.toast("Se ha devuelto los materiales seleccionados.", 2800);
              setTimeout(function() {
                return location.reload();
              }, 2800);
            } else {
              swal("Error!", "" + response.raise, "error");
            }
          });
        } else {
          swal.showInputError("Nesecitas ingresar una Observación.");
          $scope.sendReturnList();
          return false;
        }
      });
    }
  };
  $scope.getNipples = function() {
    var prm, tmp;
    tmp = new Array;
    angular.forEach($scope.mat, function(value, key) {
      if (value === true) {
        angular.forEach($scope.details, function(obj, ik) {
          if (obj.pk === key) {
            tmp.push({
              'materials': obj.fields.materiales.pk,
              'brand': obj.fields.brand.pk,
              'model': obj.fields.model.pk
            });
          }
        });
      }
    });
    prm = {
      check: JSON.stringify(tmp),
      getNipples: true
    };
    rioF.getNiples(prm).success(function(response) {
      $scope.vnip = true;
      if (response.status === true && response.valid === true) {
        $scope.gnp = response.gnp;
        $scope.showNipple = true;
        angular.element("#mnp").openModal();
      } else {
        $scope.vnip = true;
        $scope.showNipple = true;
        $scope.sendReturnList();
        return Materialize.toast("El pedido no tiene niples registrados", 2600);
      }
    });
  };
  $scope.test = function() {
    return console.log($scope);
  };
});
