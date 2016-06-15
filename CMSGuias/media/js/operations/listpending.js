var app;

app = angular.module('cpApp', ['ngCookies']);

app.config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.factory('cpf', function($http, $cookies) {
  var obj;
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  obj = new Object;
  obj.getSGroup = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get("", {
      params: options
    });
  };
  obj.getDSector = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get("", {
      params: options
    });
  };
  obj.getData = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get("", {
      params: options
    });
  };
  obj.getDataG = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get("", {
      params: options
    });
  };
  obj.getDetails = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get("", {
      params: options
    });
  };
  return obj;
});

app.controller('cpC', function($scope, $timeout, cpf) {
  $scope.selected = {};
  angular.element(document).ready(function() {});
  $scope.getSGroup = function() {
    var prm;
    prm = {
      'gsgroup': true
    };
    cpf.getSGroup(prm).success(function(response) {
      if (response.status) {
        $scope.ds = [];
        $scope.sg = response.sg;
        $scope.bsearch = 'sgroup';
        angular.element("#mselection").openModal();
      } else {
        swal("Error", "" + response.raise, "warning");
      }
    });
  };
  $scope.getDSector = function() {
    var prm;
    prm = {
      'gdsector': true
    };
    cpf.getDSector(prm).success(function(response) {
      if (response.status) {
        $scope.sg = [];
        $scope.ds = response.ds;
        $scope.bsearch = 'dsector';
        angular.element("#mselection").openModal();
      } else {
        swal("Error", "" + response.raise, "warning");
      }
    });
  };
  $scope.getData = function() {
    var obj, prm;
    $scope.gdata = [];
    prm = new Object;
    obj = angular.extend({}, $scope.selected);
    console.log(obj);
    angular.forEach(obj, function(value, key) {
      if (value === true) {
        if (!prm.hasOwnProperty('keys')) {
          prm['keys'] = key;
        } else {
          prm['keys'] += "," + key;
        }
      }
    });
    prm['searchby'] = $scope.bsearch;
    prm['getPendingData'] = true;
    return cpf.getData(prm).success(function(response) {
      if (response.status) {
        $scope.gdata = response.dataset;
        angular.element("#mselection").closeModal();
      } else {
        swal("Alerta!", "" + response.raise, "warning");
      }
    });
  };
  $scope.getDataG = function() {
    var prm;
    prm = {
      'getGlobal': true
    };
    return cpf.getDataG(prm).success(function(response) {
      if (response.status) {
        $scope.gdata = response.dataset;
      } else {
        swal("Alerta!", "" + response.raise, "warning");
      }
    });
  };
  $scope.getDetails = function(materials) {
    var obj, prm;
    prm = new Object;
    obj = $scope.selected;
    angular.forEach(obj, function(value, key) {
      if (value === true) {
        if (!prm.hasOwnProperty('keys')) {
          prm['keys'] = key;
        } else {
          prm['keys'] += "," + key;
        }
      }
    });
    prm['searchby'] = $scope.bsearch;
    prm['materials'] = materials;
    prm['getDetails'] = true;
    cpf.getDetails(prm).success(function(response) {
      console.log(response);
      if (response.status) {
        $scope.dataDetails = response.data;
        angular.element("#mdetails").openModal();
      } else {
        swal("Alerta!", "" + response.raise, "warning");
      }
    });
  };
  $scope.test = function() {
    console.log($scope.chsec);
  };
});
