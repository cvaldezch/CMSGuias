var app;

app = angular.module("compareApp", ['ngCookies']).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.factory('fDSMetrado', function($http, $cookies, $q) {
  var obj, uri;
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  obj = new Object;
  uri = location.pathname;
  obj.getCompare = function() {
    var deffered;
    deffered = $q.defer();
    $http.get("" + uri, {
      params: {
        'glist': true
      }
    }).success(function(response) {
      deffered.resolve(response);
    });
    return deffered.promise;
  };
  obj.getDataMaterials = function(materails) {
    var deffered, prm;
    deffered = $q.defer();
    prm = {
      'setdata': true,
      'materails': materails
    };
    $http.get("", {
      params: prm
    }).success(function(response) {
      deffered.resolve(response);
    });
    return deffered.promise;
  };
  return obj;
});

app.controller('ctrl', function($scope, $cookies, $timeout, $q, fDSMetrado) {
  angular.element(document).ready(function() {
    console.log("estamos listos!");
    $scope.loadList();
  });
  $scope.loadList = function() {
    $scope.loader = false;
    fDSMetrado.getCompare().then(function(data) {
      $scope.list = data.lst;
      $scope.currency = data.currency;
      $scope.symbol = data.symbol;
      $scope.salesap = data.salesap;
      $scope.sales = data.sales;
      $scope.operations = data.operations;
      $scope.diff = data.diff;
      return $scope.loader = true;
    }, function(error) {
      return console.error("error al cargar los datos");
    });
  };
  $scope.openEdit = function($event) {
    var $cell;
    $cell = $event.currentTarget.cells;
    if ($cell[8].innerText !== "") {
      fDSMetrado.getDataMaterials($cell[1].innerText).then(function(data) {
        $("#medit").openModal();
        $scope.brand = data.brand;
        return $scope.model = data.model;
      }, function(error) {
        return console.error(error);
      });
    }
  };
});
