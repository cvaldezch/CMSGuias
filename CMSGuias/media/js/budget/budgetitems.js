var app;

app = angular.module('bItemsApp', ['ngCookies', 'ngSanitize']).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller('BItemsCtrl', function($scope, $http, $cookies) {
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  angular.element(document).ready(function() {
    console.log("init document");
    $('.modal-trigger').leanModal();
    $(".modal.bottom-sheet").css("max-height", "80%");
    $scope.showDetails();
  });
  $scope.bgdetails = false;
  $scope.details = {};
  $scope.items = {};
  $scope.showDetails = function() {
    var params;
    params = new Object;
    params.budgetData = true;
    $scope.bgbedside = true;
    console.log(params);
    $http({
      url: "",
      params: params,
      method: "GET"
    }).success(function(response) {
      if (response.status) {
        $scope.details = response.budget;
        $scope.getItems();
      } else {
        swal("Alerta!", "No se encontraron datos. " + response.raise, "warning");
      }
    });
  };
  $scope.saveItemBudget = function() {
    var params;
    console.log($scope.items);
    params = $scope.items;
    if (!Object.getOwnPropertyNames(params).length) {
      swal("Alerta!", "Los campos se encontran vacios!", "warning");
      return false;
    }
    params.itag = $("[name=itag]").is(":checked");
    if (params.iname === 'undefined') {
      return false;
    }
    if (params.ibase === 'undefined') {
      return false;
    }
    if (params.ioffer === 'undefined') {
      return false;
    }
    params.saveItemBudget = true;
    params.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
    params.name = params.iname;
    params.offer = params.ioffer;
    params.base = params.ibase;
    params.tag = params.itag;
    if (typeof params.iedit !== "undefined") {
      params.editItem = params.iedit;
      params.budgeti = params.ibudgeti;
    }
    if ($("[name=budget]").val() !== "" || !typeof ($("[name=budget]").val()) === "undefined") {
      params.budget_id = $("[name=budget]").val();
    } else {
      swal("Alerta!", "No se a encontrado el código del presupuesto.", "warning");
      return false;
    }
    $http({
      url: "",
      method: "POST",
      data: $.param(params),
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }).success(function(response) {
      if (response.status) {
        console.log(response);
        $scope.getItems();
        $scope.items = {};
        $("#mitems").closeModal();
      } else {
        swal("Alerta!", "No se guardado los datos. " + response.raise + ".", "error");
      }
    });
  };
  $scope.getItems = function() {
    var params;
    params = {
      listItems: true,
      budget: $scope.details.budget_id
    };
    console.log(params);
    $http.get("", {
      params: params
    }).success(function(response) {
      if (response.status) {
        $scope.listItems = response.items;
        return setTimeout(function() {
          return $('.dropdown-button').dropdown();
        }, 800);
      } else {
        swal("Error.", "No se ha encontrado datos.  " + response.raise, "error");
      }
    });
  };
  $scope.showEditItem = function() {
    console.log(this.mi);
    $scope.items = {
      iname: this.mi.name,
      ibase: this.mi.base,
      ioffer: this.mi.offer,
      itag: this.mi.tag,
      iedit: true,
      ibudgeti: this.mi.budgeti
    };
    console.log($scope.items);
    $("#mitems").openModal();
  };
  $scope.actionCopy = function() {};
  return $scope.actionDelete = function() {
    var params;
    console.log(this.mi);
    params = {
      delitems: true,
      budgeti: this.mi.budgeti
    };
    console.log(params);
    if (typeof params.budgeti === "undefined") {
      swal("Alerta!", "Parametro  incorrecto.", "warning");
      return false;
    }
    swal({
      title: "Eliminar Item?",
      text: "desea eliminar el item con todo su contenido?",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#dd6b55",
      confirButtonText: "Eliminar!",
      closeOnConfirm: true
    }, function(isConfirm) {
      if (isConfirm) {
        $http.post("", {
          params: params
        }).success(function(response) {
          if (response.status) {
            $scope.getItems();
          } else {
            swal("Error!", "Error al eliminar el item. " + response.raise, "error");
          }
        });
      }
    });
  };
});
