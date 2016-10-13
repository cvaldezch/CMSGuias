var app;

app = angular.module('appReturnWith', ['ngCookies']);

app.config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeadername = 'X-CSRFToken';
});

app.directive('onlyNumberHyphen', function() {
  return {
    restrict: 'AE',
    require: '?ngModel',
    link: function(scope, element, attrs, ngModel) {
      element.bind('keyup', function(event) {
        var key, vl;
        key = event.which || event.keyCode;
        vl = element.val();
        if (RegExp(/(?=[0-9]{3}[-]{1}[0-9]{8}).{12}$/).test(vl)) {
          scope.$apply(function() {
            scope.valid = true;
          });
          if (key === 13) {
            scope.$apply(function() {
              scope.guide = scope.tmpg;
            });
          }
        } else {
          scope.$apply(function() {
            scope.valid = false;
          });
        }
      });
      element.bind('keypress', function(event) {
        var keycode;
        keycode = event.which || event.keyCode;
        console.log(keycode);
        if ((keycode < 48 || keycode > 57) && keycode !== 8 && keycode !== 45) {
          console.log("key block", keycode);
          event.preventDefault();
          return false;
        }
      });
    }
  };
});

app.directive('vminmax', valMinandMax);

app.factory('returnFactory', function($http, $cookies) {
  var formd, obj;
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  obj = new Object;
  formd = function(options) {
    var form, i, k, len, v;
    if (options == null) {
      options = {};
    }
    form = new FormData();
    for (v = i = 0, len = options.length; i < len; v = ++i) {
      k = options[v];
      form.append(k, v);
    }
    return form;
  };
  obj.getDetailsGuide = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get("", {
      params: options
    });
  };
  return obj;
});

app.controller('ctrlReturnWith', function($scope, $timeout, $q, returnFactory) {
  $scope.valid = false;
  $scope.guide = '';
  $scope.sald = false;
  $scope.returns = [];
  $scope.chkdet = false;
  angular.element(document).ready(function() {
    console.log("Document ready");
  });
  $scope.returnInventory = function() {
    var available;
    available = function() {
      var defer, i, len, promises, ref, x;
      defer = $q.defer();
      promises = new Array;
      ref = $scope.returns;
      for (i = 0, len = ref.length; i < len; i++) {
        x = ref[i];
        if (x.check === true && x.qreturn > 0) {
          promises.push(x);
        }
      }
      $q.all(promises).then(function(result) {
        defer.resolve(result);
      });
      return defer.promise;
    };
    available().then(function(result) {
      if (result.length > 0) {
        swal({
          title: 'Realmente desea retornar el/los accesorio(s) seleccionado(s)?.',
          text: '',
          type: 'warning',
          confirmButtonColor: '#3085d6',
          confirmButtonText: 'Si! Retornar',
          cancelButtonText: 'No!',
          showCancelButton: true,
          closeOnConfirm: true,
          closeOnCancel: true
        }, function(isConfirm) {
          if (isConfirm) {
            console.log("return");
          }
        });
      } else {
        Materialize.toast("<i class='fa fa-warning fa-2x amber-text'></i>&nbsp;<spam>Debe de selecionar al menos un item y su cantidad tiene que ser mayor a 0.</spam>", 9000, 'rounded');
      }
    });
  };
  $scope.test = function() {
    console.log($scope.valid);
    console.log($scope.tmpg);
    console.log($scope.guide);
  };
  $scope.$watch('guide', function(nw, old) {
    var prm;
    if (nw !== old) {
      $scope.sald = true;
      prm = {
        getdetails: true,
        guide: nw
      };
      returnFactory.getDetailsGuide(prm).success(function(response) {
        if (response.status) {
          $scope.dguide = response.details;
          $scope.sguide = response.guide;
          $scope.returns = [];
          $scope.sald = false;
          if (response.details.length === 0) {
            Materialize.toast("<i class=\"fa fa-meh-o fa-2x red-text\"></i>&nbsp;Oops! Noy hay un detalle que coincida con el Nro de Guia ingresado \"" + $scope.tmpg + "\" ", 12000, "rounded");
          }
        } else {
          Materialize.toast("<i class='fa fa-times red-text fa-2x'></i> No se cargo el detalle del número de guia ", 4000);
        }
      });
    }
  });
  $scope.$watch('chkdet', function(nw, old) {
    var i, len, ref, results, x;
    ref = $scope.returns;
    results = [];
    for (i = 0, len = ref.length; i < len; i++) {
      x = ref[i];
      results.push(x.check = nw);
    }
    return results;
  });
});
