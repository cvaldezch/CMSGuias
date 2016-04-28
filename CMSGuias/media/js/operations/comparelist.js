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
  obj.getDataMaterials = function(materials) {
    var deffered, prm;
    deffered = $q.defer();
    prm = {
      'brandbymaterials': true,
      'materials': materials
    };
    $http.get("/brand/list/", {
      params: prm
    }).success(function(response) {
      deffered.resolve(response);
    });
    return deffered.promise;
  };
  return obj;
});

app.controller('ctrl', function($scope, $cookies, $timeout, $q, fDSMetrado) {
  $scope.ebrand = "";
  $scope.brand = [];
  $scope.model = [];
  angular.element(document).ready(function() {
    angular.element("select").material_select();
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
      fDSMetrado.getDataMaterials($cell[1].innerText).then(function(response) {
        console.log($scope.brand);
        $("#medit").openModal();
        $scope.brand = response.data;
        console.log(response.data);
        console.log($scope.brand);
        $timeout(function() {
          return angular.element("select").material_select("update");
        }, 800);
      }, function(error) {
        return console.error(error);
      });
    }
  };
  $scope.lmodel = function() {
    console.info($scope.ebrand);
  };
});
