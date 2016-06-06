var app;

app = angular.module('cpurApp', ['ngCookies']);

app.config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.factory('fPuchase', function($http, $cookies) {
  var obj;
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  obj = new Object;
  obj.filterPurchase = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get('', {
      params: options
    });
  };
  obj.filterMaterials = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get('', {
      params: options
    });
  };
  obj.filterHist = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get('', {
      params: options
    });
  };
  return obj;
});

app.controller('cPurchase', function($scope, $timeout, fPuchase) {
  $scope.filterNroPurchase = function() {
    var prm;
    if ($scope.filpur !== '' && $scope.filpur.length === 10) {
      $scope.purchase = [];
      prm = {
        'byPurchase': true,
        'compra': $scope.filpur
      };
      fPuchase.filterPurchase(prm).success(function(response) {
        if (response.status) {
          $scope.purchase = response.details;
          $scope.purbedside = response.bedside[0];
        } else {
          swal({
            title: "No se ha encontrado datos",
            text: "",
            type: "warning",
            timer: 2600
          });
        }
      });
    }
  };
  $scope.filterMaterialsByYear = function($event) {
    var prm;
    if ($scope.filmat !== '' && $event.which === 13) {
      $scope.lsearch = [];
      prm = {
        'byMaterials': true,
        'materials': $scope.filmat
      };
      fPuchase.filterMaterials(prm).success(function(response) {
        if (response.status) {
          $scope.resultmat = response.result;
          angular.element("#mresult").openModal();
        } else {
          swal({
            title: "No se ha encontrado datos",
            text: "",
            type: "warning",
            timer: 2600
          });
        }
      });
    }
  };
  $scope.getHistotyMat = function(mat) {
    var prm;
    if (mat == null) {
      mat = '';
    }
    prm = {};
    if (mat === '') {
      mat = $scope.hmat;
      prm['year'] = $scope.sbyear;
    } else {
      $scope.hmat = mat;
    }
    prm['materiales'] = mat;
    prm['getMaterialHist'] = true;
    fPuchase.filterHist(prm).success(function(response) {
      if (response.status) {
        $scope.resumen = response.resumen;
        angular.element("#mresult").closeModal();
        $scope.syears = response.years;
        $scope.sbyear = response.resumen[0].fields.compra.fields.registrado.substr(0, 4);
      } else {
        swal({
          title: "No se ha encontrado datos",
          text: "",
          type: "warning",
          timer: 2600
        });
      }
    });
  };
  $scope.$watch('fop', function(nval) {
    if (nval === true) {
      $scope.fm = false;
    }
  });
  $scope.$watch('fm', function(nval) {
    if (nval === true) {
      $scope.fop = false;
    }
  });
});
