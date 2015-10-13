var app;

app = angular.module('dsApp', ['ngCookies']).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  return $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}).directive('stringToNumber', function() {
  return {
    require: 'ngModel',
    link: function(scope, element, attrs, ngModel) {
      ngModel.$parsers.push(function(value) {
        return '' + value;
      });
      ngModel.$formatters.push(function(value) {
        return parseFloat(value, 10);
      });
    }
  };
});

app.controller('DSCtrl', function($scope, $http, $cookies) {
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  angular.element(document).ready(function() {
    $(".floatThead").floatThead({
      zIndex: 998
    });
  });
  $scope.getListArea = function() {
    var data;
    data = {
      glist: true
    };
    $http.get("", {
      params: data
    }, function(response) {
      if (response.status) {
        $scope.dsmaterials = response.list;
      } else {
        swal("Error!", "al obtener la lista de materiales del área", "error");
      }
    });
  };
  $scope.unitList = function() {
    $http.get('/unit/list', {
      list: true
    }).success(function(response) {
      if (response.status) {
        return $scope.unit = response.unit;
      } else {
        swal("Error", "no hay datos para mostrar, Unidad", "error");
      }
    });
  };
  $scope.saveMateial = function() {
    var data;
    data = $scope.mat;
    data.savepmat = true;
    data.ppurchase = $("[name=precio]").val();
    data.psales = $("[name=sales]").val();
    data.brand = $("[name=brand]").val();
    data.model = $("[name=model]").val();
    data.code = $(".id-mat").text();
    data.unid = '';
    console.log(data);
  };
  $scope.$watch('gui.smat', function() {
    $(".floatThead").floatThead('reflow');
  });
});
