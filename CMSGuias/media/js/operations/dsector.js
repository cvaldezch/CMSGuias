var app;

app = angular.module('dsApp', ['ngCookies']).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller('DSCtrl', function($scope, $http, $cookies) {
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  angular.element(document).ready(function() {
    $scope.mat = {
      ppurchase: 0,
      psales: 0
    };
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
  $scope.saveMateial = function() {
    var data;
    data = $scope.mat;
    data.savepmat = true;
    data.ppurchase = $("[name=precio]").val();
    data.psales = $("[name=sales]").val();
    data.brand = $("[name=brand]").val();
    data.model = $("[name=model]").val();
    data.code = $(".id-mat").text();
    console.log(data);
  };
  $scope.$watch('gui.smat', function() {
    $(".floatThead").floatThead('reflow');
  });
});
