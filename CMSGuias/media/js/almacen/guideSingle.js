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
      format: 'yyyy-mm-dd',
      min: '0',
      closeOnSelect: true
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
    var $code, data;
    $code = $(".id-mat");
    data = {
      gstock: true,
      brand: $scope.mat.brand,
      model: $scope.mat.model
    };
    if ($code.text()) {
      data.code = $code.text();
    } else {
      data.gstock = false;
      Materialize.toast("El codigo del material no es correcto", 2000);
    }
    if (data.gstock) {
      $http.get('', {
        params: data
      }).success(function(response) {
        if (response.status) {
          if (response.exact.length) {
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
            if (data.quantity <= 0 || typeof data.quantity === "undefined") {
              Materialize.toast("Cantidad Invalida", 4600);
              data.saveMaterial = false;
            }
            if (data.saveMaterial) {
              if (response.exact[0].fields.stock >= data.quantity) {
                $scope.exact = [];
                $scope.alternative = [];
                $scope.stkg = [];
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
              } else {
                swal("Alerta!", "Stock es menor o no existe en el inventario", "warning");
                $scope.exact = response.exact;
                $scope.alternative = response.list;
                $scope.stkg = response.stocka;
                return false;
              }
            }
          } else {
            $scope.alternative = response.list;
            $scope.stkg = response.stocka;
            $scope.exact = response.exact;
            swal("Alerta!", "El Material no cuenta con Stock", "warning");
          }
        } else {
          Materialize.toast("No se ha encontrado Stock", 2000);
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
  $scope.validExistGuide = function() {
    var data;
    data = {
      valid: true,
      code: $scope.guide.guide
    };
    $http({
      url: '',
      method: 'post',
      data: $.param(data)
    }).success(function(response) {
      $scope.vguide = !response.status;
      if (!response.status) {
        swal("Información!", "El Nro de guia ingresado ya existe!", "info");
      }
    });
  };
  $scope.delallDetails = function() {
    swal({
      title: "Eliminar Detalle?",
      text: "desea eliminar todo la lista de detalle?",
      type: "warning",
      showCancelButton: true,
      confirmButtonText: "Si!, eliminar",
      confirmButtonColor: "#dd6b55",
      closeOnCancel: true
    }, function(isConfirm) {
      var data;
      if (isConfirm) {
        data = {
          delAllDetails: true
        };
        $http({
          url: '',
          method: 'post',
          data: $.param(data)
        }).success(function(response) {
          if (response.status) {
            $scope.listTemp();
          }
        });
      }
    });
  };
  $scope.refresh = function() {
    $scope.customersList();
    $scope.carrierList();
    $scope.listTemp();
    $scope.brandmodel();
  };
  $scope.recycleData = function() {
    $scope.customersList();
    $scope.carrierList();
    $scope.listTemp();
    $scope.brandmodel();
    $scope.guide.guide = '';
    $scope.guide.transfer = '';
    $scope.guide.dotarrival = '';
    $scope.guide.driver = '';
    $scope.guide.transport = '';
    $scope.guide.motive = '';
    $scope.guide.observation = '';
    return $scope.guide.note = '';
  };
  $scope.saveGuide = function() {
    var data, k, v;
    data = {
      save: true,
      guide: $scope.guide.guide,
      ruccliente: $scope.guide.customer,
      dotoutput: $scope.guide.dotout,
      puntollegada: $scope.guide.dotarrival,
      traslado: $scope.guide.transfer,
      traruc: $scope.guide.carrier,
      condni: $scope.guide.driver,
      nropla: $scope.guide.transport,
      motive: $scope.guide.motive,
      observation: $scope.guide.observation,
      nota: $scope.guide.note
    };
    for (k in data) {
      v = data[k];
      if (typeof v === 'undefined') {
        switch (k) {
          case 'guide':
            swal('Alerta!', 'Nro guia invalida.', 'warning');
            data.save = false;
            break;
          case 'traslado':
            swal('Alerta!', 'Fecha de traslado invalido.', 'warning');
            data.save = false;
            break;
          case 'ruccliente':
            swal('Alerta!', 'Cliente invalido.', 'warning');
            data.save = false;
            break;
          case 'dotoutput':
            swal('Alerta!', 'Punto de salida invalida.', 'warning');
            data.save = false;
            break;
          case 'puntollegada':
            swal('Alerta!', 'Punto de llegada invalida.', 'warning');
            data.save = false;
            break;
          case 'traduc':
            swal('Alerta!', 'Transportita invalido.', 'warning');
            data.save = false;
            break;
          case 'condni':
            swal('Alerta!', 'Conductor invalido.', 'warning');
            data.save = false;
            break;
          case 'nropla':
            swal('Alerta!', 'Transporte invalido.', 'warning');
            data.save = false;
            break;
        }
      }
    }
    if (new Date(data.traslado) < new Date()) {
      swal('Alerta!', 'La fecha ingresada es menor', 'warning');
      data.save = false;
    }
    if (data.save) {
      data.traslado = (data.traslado.getFullYear()) + "-" + (data.traslado.getMonth() + 1) + "-" + (data.traslado.getDate());
      data.genGuide = true;
      $http({
        url: '',
        method: 'post',
        data: $.param(data)
      }).success(function(response) {
        if (response.status) {
          swal('Felicidades!', 'se a generado la Guia de Remision', 'success');
          $timeout(function() {
            location.reload();
          }, 2600);
        } else {
          swal('Error', 'No se a generado la Guia Remision', 'error');
        }
      });
    }
  };
  $scope.showObs = function($event) {
    $scope.obs = $event.currentTarget.dataset;
    $('#mobs').openModal();
  };
  $scope.saveObser = function($event) {
    var $data;
    $data = $scope.obs;
    $data.saveObs = true;
    $http({
      url: '',
      method: 'post',
      data: $.param($data)
    }).success(function(response) {
      if (response.status) {
        Materialize.toast("Guardado OK", 1600);
        $scope.obs = {
          materials: '',
          brand: '',
          model: '',
          observation: ''
        };
        $('#mobs').closeModal();
      } else {
        swal("Error", "No se guardo la observación.", "error");
      }
    });
  };
});
