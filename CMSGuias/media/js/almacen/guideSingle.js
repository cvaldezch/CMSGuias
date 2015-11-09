var app;

app = angular.module('SGuideApp', ['ngCookies']).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller('SGuideCtrl', function($scope, $http, $cookies) {
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  angular.element(document).ready(function() {
    $('.datepicker').pickadate({
      selectMonths: true,
      selectYears: 15,
      format: 'yyyy-mm-dd'
    });
    $scope.customersList();
    $scope.carrierList();
    $scope.listTemp();
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
  $scope.saveDetalle = function() {
    var data;
    data = {
      saveMaterial: true,
      materials: $(".id-mat").text(),
      quantity: $scope.mat.quantity,
      brand: $scope.mat.brand,
      model: $scope.mat.model
    };
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
          $scope.listTemp();
          Materialize.toast('Guardado OK', 2600);
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
        setTimeout(function() {
          return $('.dropdown-button').dropdown();
        }, 800);
      } else {
        swal("Error", "no data lista", "error");
      }
    });
  };
  $scope.showEdit = function($event) {
    $scope.shwaddm = true;
    $scope.mat.code = $event.currentTarget.parentElement.parentElement.parentElement.parentElement.children[1].innerText;
    setTimeout(function() {
      var e;
      e = $.Event('keypress', {
        keyCode: 13
      });
      $("[name=code]").trigger(e);
    }, 100);
    setTimeout(function() {
      $scope.mat.quantity = parseFloat($event.currentTarget.parentElement.parentElement.parentElement.parentElement.children[6].innerText);
      $scope.mat.brand = $event.currentTarget.dataset.brand;
      $scope.mat.model = $event.currentTarget.dataset.model;
    }, 600);
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
});
