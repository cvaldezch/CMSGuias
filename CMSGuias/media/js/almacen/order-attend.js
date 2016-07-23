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
        if (val === "") {
          element.context.value = max;
        }
        if (!isNaN(val)) {
          element.context.value = max;
        }
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
  return obj;
};

app.factory('attendFactory', factories);

controllers = function($scope, $timeout, attendFactory) {
  $scope.dorders = [];
  angular.element(document).ready(function() {
    console.log("angular load success!");
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
        console.table(tmp);
        $scope.dnip = tmp;
      } else {
        Materialize.toast("Error " + response.raise, 3000, 'rounded');
      }
    });
  };
};

app.controller('attendCtrl', controllers);
