var app, controllers, factories;

app = angular.module('attendApp', ['ngCookies', 'angular.filter']);

app.config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.directive('cinmam', function($parse) {
  return {
    restrict: 'A',
    require: '?ngModel',
    scope: '@',
    link: function(scope, element, attrs, ngModel) {
      element.bind('change, blur', function(event) {
        var max, min, result, val;
        if (!isNaN(element.context.value) && element.context.value !== "") {
          val = parseFloat(element.context.value);
        } else {
          val = parseFloat(attrs.max);
        }
        max = parseFloat(attrs.max);
        min = parseFloat(attrs.min);
        result = 0;
        if (val > max) {
          result = max;
        } else if (val < min) {
          result = min;
        } else {
          result = val;
        }
        if (attrs.hasOwnProperty('ngModel')) {
          ngModel.$setViewValue(result);
          ngModel.$render();
          scope.$apply();
        } else {
          element.context.value = result;
        }
      });
    }
  };
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
  obj.getDetNiples = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get("", {
      params: options
    });
  };
  obj.getStockItem = function(options) {
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

controllers = function($scope, $timeout, $q, attendFactory) {
  var validStock;
  $scope.dorders = [];
  $scope.vstock = false;
  $scope.cstock = new Array();
  $scope.qmax = 0;
  $scope.stks = [];
  $scope.dguide = new Array();
  angular.element(document).ready(function() {
    if ($scope.init === true) {
      $scope.sDetailsOrders();
    }
  });
  $scope.sDetailsOrders = function() {
    attendFactory.getDetailsOrder({
      'details': true
    }).success(function(response) {
      if (response.status) {
        $timeout(function() {
          $scope.dorders = response.details;
          $scope.getNiple();
          return console.log("is execute!!");
        }, 80);
      } else {
        console.log("error in data " + response.raise);
      }
    });
  };
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
  $scope.getNiple = function() {
    attendFactory.getDetNiples({
      'detailsnip': true
    }).success(function(response) {
      var tmp;
      if (response.status) {
        tmp = new Array();
        angular.forEach(response.nip, function(value) {
          tmp.push({
            'materials': value.fields.materiales.pk,
            'name': value.fields.materiales.fields.matnom + " " + value.fields.materiales.fields.matmed + " " + value.fields.materiales.fields.unidad,
            'description': "Niple " + response.types[value.fields.tipo] + " ",
            'brand': value.fields.brand.pk,
            'bname': value.fields.brand.fields.brand,
            'model': value.fields.model.pk,
            'mname': value.fields.model.fields.model,
            'tipo': value.fields.tipo,
            'meter': value.fields.metrado,
            'quantity': value.fields.cantidad,
            'send': value.fields.cantshop,
            'guide': value.fields.cantguide
          });
        });
        $scope.dnip = tmp;
        angular.forEach($scope.dnip, function(object, index) {
          var a;
          a = angular.element("#q" + object.materials + object.brand + object.model);
        });
      } else {
        Materialize.toast("Error " + response.raise, 3000, 'rounded');
      }
    });
  };
  $scope.chkAll = function() {
    angular.forEach(angular.element("[name=chk]"), function(el) {
      el.checked = $scope.chk;
    });
  };
  validStock = function() {
    var defer, promises;
    defer = $q.defer();
    promises = [];
    angular.forEach(angular.element("[name=chk]"), function(el) {
      if (angular.element(el).is(":checked")) {
        promises.push({
          materials: el.attributes["data-materials"].value,
          name: el.attributes["data-mname"].value,
          brand: el.attributes["data-brand"].value,
          model: el.attributes["data-model"].value,
          nbrand: el.attributes["data-nbrand"].value,
          nmodel: el.attributes["data-nmodel"].value,
          quantity: el.attributes['data-quantity'].value
        });
      }
    });
    $q.all(promises).then(function(response) {
      defer.resolve(response);
    });
    return defer.promise;
  };
  $scope.getStock = function() {
    validStock().then(function(result) {
      $scope.cstock = result;
      $scope.dguide = new Array();
      $scope.stock();
    });
  };
  $scope.stock = function() {
    var deferred, nextStep;
    deferred = $q.defer();
    nextStep = function() {
      var prm;
      if ($scope.cstock.length > 0) {
        prm = $scope.cstock[0];
        prm['gstock'] = true;
        attendFactory.getStockItem(prm).success(function(response) {
          if (response.status) {
            $scope.stks = new Array();
            $scope.istock = response.stock;
            $scope.qmax = parseFloat(prm.quantity);
            $scope.gbrand = prm.brand;
            $scope.gmodel = prm.model;
            $scope.gmaterials = prm.materials;
            angular.element("#sd").text(prm.name + " " + prm.nbrand + " " + prm.nmodel);
            $scope.dstock = {
              'materials': prm.materials,
              'brand': prm.brand,
              'model': prm.model
            };
            angular.element("#mstock").openModal({
              dismissible: false
            });
            console.info(prm);
            $scope.cstock.splice(0, 1);
            console.log($scope.cstock);
            deferred.resolve(false);
          } else {
            console.log(response.raise);
            deferred.resolve(false);
          }
        });
      } else {
        deferred.resolve(true);
      }
    };
    nextStep();
    return deferred.promise;
  };
  $scope.selectStock = function($event) {
    var stk;
    console.log(this);
    stk = angular.element("#stk" + this.x.fields.materials.pk + $scope.dstock['brand'] + $scope.dstock['model']);
    stk[0].value = this.x.fields.stock;
    angular.element("#mstock").closeModal();
    $scope.stock().then(function(result) {
      console.warn(result);
      if (result) {
        return Materialize.toast("Complete!", 3000);
      } else {
        return console.log("Falta");
      }
    });
  };
  $scope.showNip = function() {
    var brand, mat, model, tmp;
    mat = $scope.gmaterials === obj.materials;
    brand = $scope.gbrand === obj.brand;
    model = $scoep.gmodel === obj.model;
    tmp = new Array();
    angular.forEach($scope.dnip, function(obj, index) {
      if (mat && brand && model) {
        tmp.push(obj);
      }
    });
  };
  $scope.validSelectStock = function() {
    var amount, stk, tmp;
    tmp = new Array();
    amount = 0;
    angular.forEach($scope.stks, function(obj, index) {
      amount += obj['quantity'];
    });
    console.log(amount);
    if (amount > $scope.qmax) {
      Materialize.toast("<i class='fa fa-times fa-3x red-text'></i>&nbsp;Cantidad mayor a la requerida.", 6000);
    } else if (amount < 0) {
      Materialize.toast("<i class='fa fa-times fa-3x red-text'></i>&nbsp;Cantidad menor que 0.", 6000);
    } else {
      stk = angular.element("#q" + $scope.gmaterials + $scope.gbrand + $scope.gmodel);
      $scope.dguide.push({
        'materials': $scope.gmaterials,
        'brand': $scope.gbrand,
        'model': $scope.gmodel,
        'details': new Array()
      });
      angular.forEach($scope.dguide, function(obj, index) {
        var b, m, o;
        m = obj.materials === $scope.gmaterials;
        b = obj.brand === $scope.gbrand;
        o = obj.model === $scope.gmodel;
        if (m && b && o) {
          angular.forEach($scope.stks, function(stk, i) {
            obj.details.push({
              'materials': $scope.gmaterials,
              'brand': stk.brand,
              'model': stk.model,
              'quantity': stk.quantity
            });
          });
        }
      });
      console.log(stk);
      stk[0].value = amount;
      console.info("Nothing generate guide");
      console.warn($scope.dguide);
      $scope.stock().then(function(result) {
        console.warn(result);
        if (result) {
          angular.element("#mstock").closeModal();
          Materialize.toast("Completo!", 3000);
        } else {
          console.log("Falta");
        }
      });
    }
  };
};

app.controller('attendCtrl', controllers);
