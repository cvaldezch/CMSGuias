var app, getBudgetData, saveBudget, showBudget, showBudgetEdit, showSearchBudget;

$(function() {
  $("select").material_select();
  $(".modal-trigger").leanModal();
  $("[name=finish]").pickadate({
    closeOnSelect: true,
    container: 'body',
    selectMonths: true,
    selectYears: 15,
    format: 'yyyy-mm-dd'
  });
  $("[name=showBudget]").on("click", showBudget);
  $("[name=saveBudget]").on("click", saveBudget);
  $(".bsearchbudget").on("click", showSearchBudget);
  $(".showbudgetdetails").on("click", getBudgetData);
  $(".showbudgetedit").on("click", showBudgetEdit);
  tinymce.init({
    selector: "textarea[name=observation]",
    menubar: false,
    toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image"
  });
  $(".modal.bottom-sheet").css("max-height", "65%");
});

showBudget = function(event) {
  $("[name=budget]").val("");
  $("#nbudget").openModal();
  console.log("leanModal");
};

showSearchBudget = function(event) {
  $(".panel-sbudget").toggle("linear");
};

saveBudget = function(event) {
  $.validate({
    form: "#newBudget",
    errorMessagePosition: "top",
    scrollToTopOnError: true,
    onError: function() {
      return false;
    },
    onSuccess: function() {
      var $edit, params;
      event.preventDefault();
      params = new Object;
      params.name = $("[name=name]").val();
      params.customers = $("[name=customers]").val();
      params.address = $("[name=address]").val();
      params.country = $("[name=pais]").val();
      params.departament = $("[name=departamento]").val();
      params.province = $("[name=provincia]").val();
      params.district = $("[name=distrito]").val();
      params.hourwork = $("[name=hours]").val();
      params.finish = $("[name=finish]").val();
      params.base = $("[name=base]").val();
      params.offer = $("[name=offer]").val();
      params.currency = $("[name=currency]").val();
      params.exchange = $("[name=exchange]").val();
      params.observation = $("#observation_ifr").contents().find("body").html();
      params.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
      params.saveBudget = true;
      $edit = $("[name=budget]");
      if ($edit.val() != null) {
        params.edit = true;
        params.budget = $edit.val();
      }
      $.post("", params, function(response) {
        if (response.status) {
          location.reload();
        } else {
          swal("Oops Alert!", "No se han guardado lo datos correctamente. " + response.raise, "warning");
        }
      }, "json");
      return false;
    }
  });
};

showBudgetEdit = function(event) {
  $("[name=budget]").val(this.getAttribute("data-value"));
};

getBudgetData = function(event) {
  var params;
  params = new Object;
  params.budgetData = true;
  params.budget = this.getAttribute("data-value");
  console.log(params);
  $.getJSON("", params, function(response) {
    var colone, coltwo;
    if (response.status) {
      colone = "<dt>Presupuesto</dt>\n<dd>{{ budget.budget_id }}</dd>\n<dt>Cliente</dt>\n<dd>{{ budget.customers }}</dd>\n<dt>Dirección</dt>\n<dd>{{ budget.address }}, {{ budget.country }}, {{ budget.departament }}, {{ budget.province }}, {{ budget.district }}</dd>\n<dt>Observación</dt>\n<dd>{{ budget.observation }}</dd>";
      coltwo = "<dt>Registrado</dt>\n<dd>{{ budget.register }}</dd>\n<dt>Jornada Diaria</dt>\n<dd>{{ budget.hourwork }}</dd>\n<dt>F. Entrega</dt>\n<dd>{{ budget.finish }}</dd>\n<dt>Moneda</dt>\n<dd>{{ budget.currency }}</dd>";
      $(".colone").html(Mustache.render(colone, response));
      return $(".coltwo").html(Mustache.render(coltwo, response));
    } else {
      swal("Alerta!", "No se encontraron datos. " + response.raise, "warning");
    }
  });
};

app = angular.module('BudgetApp', ['ngCookies', 'ngSanitize']).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.controller('BudgetCtrl', function($scope, $http, $cookies) {
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  $scope.ssearch = false;
  $scope.bgbedside = false;
  $scope.bgdetails = false;
  $scope.details = {};
  $scope.items = {};
  $scope.showDetails = function(target) {
    var params;
    params = new Object;
    params.budgetData = true;
    params.budget = target;
    $scope.bgbedside = true;
    console.log(params);
    $http({
      url: "",
      params: params,
      method: "GET"
    }).success(function(response) {
      if (response.status) {
        $scope.details = response.budget;
        $scope.bgdetails = true;
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
        return $scope.listItems = response.items;
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
  $scope.$watch('bgdetails', function(val) {
    console.log(val);
    if (val) {
      $scope.ssearch = false;
      $scope.getItems();
    }
    if (!val) {
      $scope.details['budget_id'] = '';
    }
  });
  $scope.test = function() {
    console.log("you dblclick me!");
  };
});
