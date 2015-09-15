var app, hextorbga;

app = angular.module('programingApp', ['ngCookies']).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller('programingCtrl', function($scope, $http, $cookies) {
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  $scope.group = {
    rgba: ""
  };
  angular.element(document).ready(function() {
    $('.modal-trigger').leanModal();
  });
  $scope.$watch('group.colour', function(val, old) {
    $scope.group.rgba = hextorbga(val, 0.5);
  });
  $scope.saveGroup = function() {
    var data;
    data = $scope.group;
    data.saveg = true;
    console.log(data);

    /*$http
      url: ''
      method: 'post'
      data: $.param data
    , success (response) ->
      if response.status
        swal "Felicidades", "se guardo los datos correctamente.", "success"
        return
      else
        swal "Error", "no se a guardado los datos. #{response.raise}", "error"
        return
     */
  };
});

hextorbga = function(hex, alf) {
  var b, g, r;
  if (alf == null) {
    alf = 1;
  }
  if (typeof(hex) == "undefined"){
    hex = ""
  };
  if (hex.charAt(0) === "#") {
    hex = hex.substring(1, 7);
    r = parseInt(hex.substring(0, 2), 16);
    g = parseInt(hex.substring(2, 4), 16);
    b = parseInt(hex.substring(4, 6), 16);
    return "rgba(" + r + "," + g + "," + b + "," + alf + ")";
  } else {
    return hex;
  }
};
