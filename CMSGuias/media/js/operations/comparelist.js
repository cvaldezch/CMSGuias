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
  obj.getModel = function(brand) {
    var prm;
    prm = {
      'modelbybrand': true,
      'brand': brand
    };
    return $http.get("/brand/list/", {
      params: prm
    });
  };
  obj.update = function(options) {
    var prm;
    if (options == null) {
      options = {};
    }
    prm = options;
    return $http.get("", {
      params: prm
    });
  };
  return obj;
});

app.controller('ctrl', function($scope, $cookies, $timeout, $q, fDSMetrado) {
  $scope.ebrand = "";
  $scope.brand = [];
  $scope.model = [];
  $scope.ename = "";
  $scope.eunit = "";
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
    if ($cell[9].innerText.replace(' ', '') !== "") {
      fDSMetrado.getDataMaterials($cell[1].innerText).then(function(response) {
        $("#medit").openModal();
        $scope.brand = response.data;
        $timeout(function() {
          $scope.ename = $cell[2].innerText;
          $scope.eunit = $cell[5].innerText;
          $scope.ematc = $cell[1].innerText;
          $scope.eprice = $cell[6].innerText;
          $scope.esales = $cell[7].innerText;
          $scope.ebrand = $cell[0].children[0].dataset.brand;
          $scope.obrand = $cell[0].children[0].dataset.brand;
          $scope.omodel = $cell[0].children[0].dataset.model;
          $scope.lmodel();
        }, 600);
        $timeout(function() {
          $scope.emodel = $cell[0].children[0].dataset.model;
        }, 1200);
      }, function(error) {
        return console.error(error);
      });
    }
  };
  $scope.lmodel = function() {
    fDSMetrado.getModel($scope.ebrand).success(function(response) {
      console.log(response);
      return $scope.model = response.model;
    });
  };
  $scope.saveChange = function($event) {
    var obj;
    obj = {
      materials: $scope.ematc,
      brand: $scope.ebrand,
      model: $scope.emodel,
      obrand: $scope.obrand,
      omodel: $scope.omodel,
      ppurchase: $scope.eprice,
      psales: $scope.esales,
      'saveChange': true
    };
    fDSMetrado.update(obj).success(function(response) {
      if (response.status) {
        swal({
          title: "Felicidades!",
          text: "",
          type: "success",
          allowOutsideClick: false,
          timer: 2600
        });
        $scope.ematc = "";
        $scope.ename = "";
        $scope.eunit = "";
        $scope.obrand = "";
        $scope.omodel = "";
        $scope.loadList();
        $("#medit").closeModal();
      } else {
        swal("No se ha guardado los cambios", "", "warning");
      }
    });
  };
});
