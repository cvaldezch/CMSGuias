(function() {
  'use strict';
  var app, cpFactories;
  app = angular.module('cpApp', ['ngCookies']);
  app.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  });
  app.directive("vcode", function() {
    return {
      restrict: 'AE',
      require: '?ngModel',
      link: function(scope, element, attrs) {
        element.bind('keypress', function(event) {
          var code;
          code = String(element.val());
          console.info(code);
          if (code.length > 5) {
            event.preventDefault();
          }
        });
      }
    };
  });
  cpFactories = function($http, $cookies) {
    var fd, obj;
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    fd = function(options) {
      var form, k, v;
      if (options == null) {
        options = {};
      }
      form = new FormData();
      for (k in options) {
        v = options[k];
        form.append(k, v);
      }
      return form;
    };
    obj = new Object();
    obj.getComplete = function(options) {
      if (options == null) {
        options = {};
      }
      return $http.get("", {
        params: options
      });
    };
    obj.formData = function(options) {
      if (options == null) {
        options = {};
      }
      return $http.post("", fd(options), {
        transformRequest: angular.identity,
        headers: {
          'Content-Type': void 0
        }
      });
    };
    obj.formCross = function(uri, options) {
      if (uri == null) {
        uri = "";
      }
      if (options == null) {
        options = {};
      }
      return $http.jsonp(uri, {
        params: options
      });
    };
    return obj;
  };
  app.factory('cpFactory', cpFactories);
  app.controller('cpCtrl', function($rootScope, $scope, $log, cpFactory) {
    $scope.call = false;
    $scope.mstyle = '';
    $scope.ctrl = {
      'storage': false,
      'operations': false,
      'quality': false,
      'accounting': false,
      'sales': false
    };
    angular.element(document).ready(function() {
      $scope.validArea();
      angular.element('.collapsible').collapsible();
      angular.element('.scrollspy').scrollSpy();
      $scope.sComplete();
    });
    $scope.sComplete = function() {
      cpFactory.getComplete({
        'gcomplete': true
      }).success(function(response) {
        if (response.status) {
          $scope.sh = response.complete;
        } else {
          Materialize.toast("" + response.raise, 2000);
          $scope.sh = response.complete;
        }
      });
    };
    $scope.validArea = function() {
      var x;
      switch ($scope.uarea) {
        case 'administrator' || 'ventas' || 'logistica':
          for (x in $scope.ctrl) {
            $scope.ctrl[x] = true;
          }
          break;
        case 'operaciones':
          $scope.ctrl['operations'] = true;
          break;
        case 'calidad':
          $scope.ctrl['quality'] = true;
          break;
        case 'almacen':
          $scope.ctrl['storage'] = true;
      }
    };
    $scope.storageClosed = function() {
      swal({
        title: "Realmanete desea Cerrar el Almacén?",
        text: '',
        type: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Si!, cerrar',
        confirmButtonColor: "#e82a37",
        closeOnCancel: true,
        closeOnConfirm: true
      }, function(isConfirm) {
        if (isConfirm) {
          $log.info("yes closed");
          cpFactory.formData({
            'storage': true
          }).success(function(response) {
            if (response.status) {
              $scope.sComplete();
              Materialize.toast("<i class='fa fa-check fa-lg green-text'></i>&nbsp;Almacén Cerrado", 4000);
            } else {
              Materialize.toast("<i class='fa fa-times fa-lg red-text'></i>&nbsp;" + repsonse.raise, 4000);
            }
          });
        } else {
          $scope.$apply(function() {
            $scope.closedstorage = false;
          });
        }
      });
    };
    $scope.letterClosed = function() {
      if (angular.element("#letterup")[0].files.length === 0) {
        Materialize.toast("<i class='fa fa-warning amber-text fa-lg'></i> Debe seleccionar por lo menos un archivo.", 4000);
        return false;
      }
      swal({
        title: "Realmanete desea cargar la Carta de Entrega?",
        text: '',
        type: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Si!, subir',
        confirmButtonColor: "#f82432",
        closeOnCancel: true,
        closeOnConfirm: true
      }, function(isConfirm) {
        var prm;
        if (isConfirm) {
          prm = {
            'operations': true,
            'letter': angular.element("#letterup")[0].files[0]
          };
          cpFactory.formData(prm).success(function(response) {
            if (response.status) {
              $scope.sComplete();
              Materialize.toast("<i class='fa fa-check fa-lg green-text'></i>&nbsp;Archivo subido.", 4000);
            } else {
              Materialize.toast("<i class='fa fa-times fa-lg red-text'></i>&nbsp;" + repsonse.raise, 4000);
            }
          });
        }
      });
    };
    $scope.qualityClosed = function() {
      if (angular.element("#qualityfile")[0].files.length === 0) {
        Materialize.toast("<i class='fa fa-warning amber-text fa-lg'></i> Debe seleccionar por lo menos un archivo.", 4000);
        return false;
      }
      swal({
        title: "Realmanete desea cargar los documentos de calidad?",
        text: '',
        type: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Si!, subir',
        confirmButtonColor: "#f82432",
        closeOnCancel: true,
        closeOnConfirm: true
      }, function(isConfirm) {
        var prm;
        if (isConfirm) {
          prm = {
            'quality': true,
            'documents': angular.element("#qualityfile")[0].files[0]
          };
          cpFactory.formData(prm).success(function(response) {
            if (response.status) {
              $scope.sComplete();
              Materialize.toast("<i class='fa fa-check fa-lg green-text'></i>&nbsp;Archivo subido.", 4000);
            } else {
              Materialize.toast("<i class='fa fa-times fa-lg red-text'></i>&nbsp;" + repsonse.raise, 4000);
            }
          });
        }
      });
    };
    $scope.accountingClosed = function() {
      var prm;
      prm = {
        accounting: true,
        tinvoice: $scope.acctinvoice,
        tiva: $scope.acctiva,
        otherin: $scope.acctotherin,
        otherout: $scope.acctotherout,
        retention: $scope.acctretention
      };
      if (angular.element("#accountingfile")[0].files.length > 0) {
        prm['fileaccounting'] = angular.element("#accountingfile")[0].files[0];
      }
      swal({
        title: "Realmanete desea cargar los documentos de calidad?",
        text: '',
        type: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Si!, subir',
        confirmButtonColor: "#f82432",
        closeOnCancel: true,
        closeOnConfirm: true
      }, function(isConfirm) {
        if (isConfirm) {
          cpFactory.formData(prm).success(function(response) {
            if (response.status) {
              $scope.sComplete();
              Materialize.toast("<i class='fa fa-check fa-lg green-text'></i>&nbsp;Archivo subido.", 4000);
            } else {
              Materialize.toast("<i class='fa fa-times fa-lg red-text'></i>&nbsp;" + repsonse.raise, 4000);
            }
          });
        }
      });
    };
    $scope.accountingQuit = function() {
      swal({
        title: "Realmanete desea cargar los documentos de calidad?",
        text: '',
        type: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Si!, subir',
        confirmButtonColor: "#f82432",
        closeOnCancel: true,
        closeOnConfirm: true
      }, function(isConfirm) {
        var prm;
        if (isConfirm) {
          prm = {
            'sales': true,
            'closed': true,
            'confirm': $scope.gpin
          };
          cpFactory.formData(prm).success(function(response) {
            if (response.status) {
              $scope.sComplete();
              Materialize.toast("<i class='fa fa-check fa-lg green-text'></i>&nbsp;Contabilidad cerrada.", 4000);
            } else {
              Materialize.toast("<i class='fa fa-times fa-lg red-text'></i>&nbsp;" + repsonse.raise, 4000);
            }
          });
        }
      });
    };
    $scope.getPin = function() {
      var prm;
      Materialize.toast('<i class="fa fa-cog fa-spin fa-2x"></i>&nbsp;&nbsp;Generando PIN, espere!', 'some', 'lime lighten-1 grey-text text-darken-3 toast-static');
      prm = {
        genpin: true,
        sales: true
      };
      cpFactory.formData(prm).success(function(response) {
        if (response.status) {
          angular.element(".toast-static").remove();
          Materialize.toast('<i class="fa fa-envelope-o fa-lg"></i>&nbsp Estamos enviando el PIN a su correo.', 'some', 'toast-static');
          prm = {
            forsb: response.mail,
            issue: "PIN DE CIERRE PROYECTO " + response.pro,
            body: "<p><strong><strong>" + response.company + " |</strong></strong> Operaciones Frecuentes</p><p>Generar PIN para cierre de proyecto | <strong>" + (new Date().toString()) + "</strong></p><p><strong>PIN:&nbsp;" + response.pin + "</strong></p><p><strong>Proyecto:&nbsp;" + response.pro + " " + response.name + "</strong></p>",
            callback: 'JSON_CALLBACK'
          };
          cpFactory.formCross("http://190.41.246.91:3000/mailer/", prm).success(function(rescross) {
            if (rescross.status) {
              angular.element(".toast-static").remove();
              Materialize.toast('<i class="fa fa-paper-plane-o fa-lg"></i>&nbsp; Se a envio correntamente el correo', 4000);
            } else {
              Materialize.toast('Se ha producido algun error #{rescross}', 7000);
            }
          });
        } else {
          Materialize.toast("<i class='fa fa-times fa-lg red-text'></i> " + response.raise);
        }
      });
    };
    $scope.$watch('call', function(nw, old) {
      if (nw !== void 0) {
        if (nw === false) {
          $scope.mstyle = {
            'display': 'hide'
          };
        } else {
          $scope.mstyle = {
            'display': 'block'
          };
        }
      }
    });
    $scope.$watch('closedstorage', function(nw, old) {
      if (nw !== void 0) {
        if (nw === true) {
          $scope.storageClosed();
        }
      }
    });
  });
})();
