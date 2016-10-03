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
        if (RegExp(/[0-9]{3}[-]{1}[0-9]{8}/).test(vl)) {
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
  angular.element(document).ready(function() {
    console.log("Document ready");
  });
  $scope.getdetailsGuide = function() {};
  $scope.test = function() {
    console.log($scope.valid);
    console.log($scope.tmpg);
    console.log($scope.guide);
  };
  $scope.$watch('guide', function(nw, old) {
    var prm;
    if (nw !== old) {
      console.log(nw);
      prm = {
        getdetails: true,
        guide: nw
      };
      returnFactory.getDetailsGuide(prm).success(function(response) {
        if (response.status) {
          $scope.dguide = response.details;
        } else {
          Materialize.toast("<i class='fa fa-times red fa-2x'></i> No se cargo el detalle del número de guia ", 4000);
        }
      });
    }
  });
});
