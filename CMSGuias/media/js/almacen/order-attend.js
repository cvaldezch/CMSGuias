var app, controllers, factories;

app = angular.module('attendApp', ['ngCookies', 'angular.filter']);

app.config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.directive('cinmam', function($parse) {
  return {
    link: function(scope, element, attrs, ngModel) {
      element.bind('change, blur', function(event) {
        var max, min, val;
        val = parseFloat(element.context.value);
        max = parseFloat(attrs.max);
        min = parseFloat(attrs.min);
        if (val > max) {
          element.context.value = max;
        }
        if (val < min) {
          element.context.value = min;
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
      promises.push({
        materials: el.attributes["data-materials"].value,
        name: el.attributes["data-mname"].value,
        brand: el.attributes["data-brand"].value,
        model: el.attributes["data-model"].value,
        nbrand: el.attributes["data-nbrand"].value,
        nmodel: el.attributes["data-nmodel"].value,
        quantity: el.attributes['data-quantity'].value
      });
    });
    $q.all(promises).then(function(response) {
      defer.resolve(response);
    });
    return defer.promise;
  };
  $scope.getStock = function() {
    validStock().then(function(result) {
      $scope.cstock = result;
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
            $scope.istock = response.stock;
            $scope.qmax = parseFloat(prm.quantity);
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
      if (result.value) {
        return Materialize.toast("Complete!", 3000);
      } else {
        return console.log("Falta");
      }
    });
  };
  $scope.validSelectStock = function() {
    console.log($scope.stks);
    console.info(JSON.stringify($scope.stks));
  };
};

app.controller('attendCtrl', controllers);
