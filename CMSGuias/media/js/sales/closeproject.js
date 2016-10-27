(function() {
  var app, cpCtrl;
  app = angular.module('cpApp', []);
  cpCtrl = function($rootScope, $scope, $log) {
    $scope.call = false;
    $scope.mstyle = '';
    angular.element(document).ready(function() {
      angular.element('.collapsible').collapsible();
      angular.element('.scrollspy').scrollSpy();
    });
    $scope.$watch('call', function(nw, old) {
      if (nw !== void 0) {
        if (nw === false) {
          $scope.mstyle = {
            'display': 'hide'
          };
        } else {
          $scope.mstyle = {
            'display': 'block'
          };
        }
      }
    });
  };
  'use strict';
  app.controller('cpCtrl', cpCtrl);
})();
