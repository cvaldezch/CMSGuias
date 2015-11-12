var app;

app = angular.module('SGuideApp', ['ngCookies']).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller('SGuideCtrl', function($scope, $http, $cookies, $timeout) {
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  $scope.mat = {};
  angular.element(document).ready(function() {
    $('.datepicker').pickadate({
      selectMonths: true,
      selectYears: 15,
      format: 'yyyy-mm-dd'
    });
    $scope.customersList();
    $scope.carrierList();
    $scope.listTemp();
    $scope.brandmodel();
  });
  $scope.customersList = function() {
    $http.get('', {
      params: {
        customers: true
      }
    }).success(function(response) {
      if (response.status) {
        $scope.customers = response.customers;
      } else {
        swal("Error", "datos de los clientes. " + response.raise, "error");
      }
    });
  };
  $scope.carrierList = function() {
    $http.get('', {
      params: {
        carrier: true
      }
    }).success(function(response) {
      if (response.status) {
        $scope.carriers = response.carrier;
      } else {
        swal("Error", "datos de los Transportista. " + response.raise, "error");
      }
    });
  };
  $scope.detCarriers = function($event) {
    var data;
    data = {
      tra: $event.currentTarget.value,
      detCarrier: true
    };
    $http.get('', {
      params: data
    }).success(function(response) {
      if (response.status) {
        $scope.drivers = response.driver;
        $scope.transports = response.transport;
      } else {
        swal("Error", "datos de los Transportista. " + response.raise, "error");
      }
    });
  };
  $scope.brandmodel = function() {
    $http.get('', {
      params: {
        brandandmodel: true
      }
    }).success(function(response) {
      if (response.status) {
        $scope.brand = response.brand;
        $scope.model = response.model;
        $scope.mat.brand = 'BR000';
        $scope.mat.model = 'MO000';
      } else {
        console.log("No loads brand and model");
      }
    });
  };
  $scope.saveDetalle = function() {
    var data;
    data = {
      saveMaterial: true,
      materials: $(".id-mat").text(),
      quantity: $scope.mat.quantity,
      brand: $scope.mat.brand,
      model: $scope.mat.model
    };
    if ($scope.mat.obrand !== "") {
      data.obrand = $scope.mat.obrand;
    }
    if ($scope.mat.omodel !== "") {
      data.omodel = $scope.mat.omodel;
    }
    if ($scope.mat.quantity <= 0) {
      Materialize.toast("Cantidad Invalida", 3600);
      data.saveMaterial = false;
    }
    console.log(data);
    if (data.saveMaterial) {
      $http({
        url: '',
        data: $.param(data),
        method: 'post'
      }).success(function(response) {
        if (response.status) {
          if ($scope.mat.hasOwnProperty('obrand')) {
            $scope.mat.obrand = '';
          }
          if ($scope.mat.hasOwnProperty('omodel')) {
            $scope.mat.omodel = '';
          }
          $scope.listTemp();
          Materialize.toast('Guardado OK', 2600);
          $scope.mat.brand = 'BR000';
          $scope.mat.model = 'MO000';
          $scope.mat.quantity = 0;
        } else {
          swal("Error", "No se guardo los datos", "error");
        }
      });
    }
  };
  $scope.listTemp = function() {
    $http.get('', {
      params: {
        listTemp: true
      }
    }).success(function(response) {
      if (response.status) {
        $scope.list = response.list;
        $timeout(function() {
          return $('.dropdown-button').dropdown();
        }, 800);
      } else {
        swal("Error", "no data lista", "error");
      }
    });
  };
  $scope.showEdit = function($event) {
    $scope.mat.code = $event.currentTarget.parentElement.parentElement.parentElement.parentElement.children[1].innerText;
    $timeout(function() {
      var e;
      e = $.Event('keypress', {
        keyCode: 13
      });
      $("[name=code]").trigger(e);
    }, 100);
    $timeout(function() {
      var quantity;
      quantity = parseFloat($event.currentTarget.parentElement.parentElement.parentElement.parentElement.children[6].innerText);
      $scope.shwaddm = true;
      $scope.mat = {
        quantity: parseFloat(quantity),
        brand: $event.currentTarget.dataset.brand,
        model: $event.currentTarget.dataset.model,
        obrand: $event.currentTarget.dataset.brand,
        omodel: $event.currentTarget.dataset.model
      };
    }, 300);
  };
  $scope.delItem = function($event) {
    var text;
    text = $event.currentTarget.parentElement.parentElement.parentElement.parentElement.children[2].innerText + " " + $event.currentTarget.parentElement.parentElement.parentElement.parentElement.children[3].innerText + " " + $event.currentTarget.parentElement.parentElement.parentElement.parentElement.children[4].innerText;
    swal({
      title: "Eliminar Material",
      text: text,
      type: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#dd6b55',
      confirmButtonText: 'Si!, Eliminar',
      closeOnConfirm: true,
      closeOnCancel: true
    }, function(isConfirm) {
      var data;
      if (isConfirm) {
        data = {
          delItem: true,
          materials: $event.currentTarget.parentElement.parentElement.parentElement.parentElement.children[1].innerText,
          brand: $event.currentTarget.dataset.brand,
          model: $event.currentTarget.dataset.model
        };
        $http({
          url: '',
          data: $.param(data),
          method: 'post'
        }).success(function(response) {
          if (response.status) {
            $scope.listTemp();
          } else {
            swal("Error", "No se a eliminad", "error");
          }
        });
      }
    });
  };
  $scope.getStock = function() {
    var $code, data;
    $code = $(".id-mat");
    data = {
      gstock: true,
      brand: $scope.mat.brand,
      model: $scope.mat.model
    };
    console.log(data);
    if ($code.val()) {
      data.code = $code.val();
    } else {
      data.gstock = false;
    }
    if (data.gstock) {
      $http({
        url: '',
        data: $.param(data),
        method: 'post'
      }).success(function(response) {
        if (response.status) {

        } else {
          Materialize.toast("No se ha encontrado Stock", 2000);
        }
      });
    }
  };
  $scope.validExistGuide = function() {
    var data;
    data = {
      valid: true,
      guide: $scope.guide
    };
    $http({
      url: '',
      method: 'post',
      data: $.param(data)
    }).success(function(response) {
      if (response.status) {

      }
    });
  };
  $scope.change = function() {
    console.log("this object to change");
  };
  $scope.$watch('summary', function(old, nw) {
    console.log(old, nw);
  });
});
