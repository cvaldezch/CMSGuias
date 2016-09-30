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
    }
  };
});

app.controller('ctrlReturnWith', function($scope, $timeout) {
  $scope.valid = false;
  $scope.guide = '';
  angular.element(document).ready(function() {
    console.log("Document ready");
  });
  $scope.test = function() {
    console.log($scope.valid);
    console.log($scope.tmpg);
    console.log($scope.guide);
  };
});
