var app;

app = angular.module('supApp', ['ngCookies', 'ngSanitize']).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller('supCtrl', function($scope, $http, $cookies) {
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  angular.element(document).ready(function() {
    console.log("ready");
    $('.datepicker').pickadate({
      container: 'body',
      format: 'yyyy-mm-dd'
    });
    $('.modal-trigger').leanModal();
    $(".modal.bottom-sheet").css("max-height", "60%");
    $scope.listSupplier();
  });
  $scope.listSupplier = function() {
    $http.get('', {
      params: {
        'list': true
      }
    }).success(function(response) {
      console.log(response);
      if (response.status) {
        $scope.list = response.supplier;
      } else {
        swal("Alerta!", "No se han encontrado datos.", "warning");
      }
    });
  };
  $scope.saveSupplier = function() {
    var params;
    if (typeof $scope.supplier.proveedor_id === "undefined") {
      return false;
    }
    params = $scope.supplier;
    params.save = true;
    params.pais = $("[name=pais]").val();
    params.departamento = $("[name=departamento]").val();
    params.provincia = $("[name=provincia]").val();
    params.distrito = $("[name=distrito]").val();
    console.log(params);
  };
  $scope.showEdit = function() {
    var option;
    $scope.supplier = {
      proveedor_id: this.x.pk,
      razonsocial: this.x.fields.razonsocial,
      direccion: this.x.fields.direccion,
      telefono: this.x.fields.telefono,
      tipo: this.x.fields.tipo,
      origen: this.x.fields.origen,
      contact: this.x.fields.contact,
      email: this.x.fields.email
    };
    option = this;
    $("[name=pais]").val(option.x.fields.pais.pk).click();
    setTimeout(function() {
      return $("[name=departamento]").val(option.x.fields.departamento.pk).click();
    }, 800);
    setTimeout(function() {
      return $("[name=provincia]").val(option.x.fields.provincia.pk).click();
    }, 1800);
    setTimeout(function() {
      return $("[name=distrito]").val(option.x.fields.distrito.pk);
    }, 2600);
    $("#madd").openModal();
    console.log($scope.supplier);
  };
});
