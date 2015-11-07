var app, byte2Hex, hextorbga, rgbtohex;

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
    $(".datepicker").pickadate({
      container: 'body',
      format: 'yyyy-mm-dd',
      selectMonths: true,
      selectYears: true
    });
    $scope.lgroup();
    $scope.getDSectorList();
    $(".modal").css("max-height", "80%");
  });
  $scope.$watch('group.colour', function(val, old) {
    $scope.group.rgba = hextorbga(val, 0.5);
  });
  $scope.lgroup = function() {
    var data;
    data = {
      'listg': true
    };
    $http.get('', {
      params: data
    }).success(function(response) {
      if (response.status) {
        $scope.sglist = response.sg;
      } else {
        swal("Error!", "No se han obtenido datos. " + response.raise, "error");
      }
    });
  };
  $scope.saveGroup = function() {
    var data;
    $("#mlgroup").closeModal();
    data = $scope.group;
    data.saveg = true;
    $http({
      url: '',
      method: 'post',
      data: $.param(data)
    }).success(function(response) {
      if (response.status) {
        Materialize.toast('Se guardado correctamente', 1800);
        $("#mgroup").closeModal();
        $scope.listGroup();
      } else {
        swal("Error", "no se a guardado los datos. " + response.raise, "error");
      }
    });
  };
  $scope.listGroup = function() {
    var data;
    data = {
      'listg': true
    };
    $http.get('', {
      params: data
    }).success(function(response) {
      if (response.status) {
        $scope.sglist = response.sg;
        $("#mlgroup").openModal();
        setTimeout(function() {
          $('.dropdown-button').dropdown();
        }, 800);
      } else {
        swal("Error!", "No se han obtenido datos. " + response.raise, "error");
      }
    });
  };
  $scope.showESG = function() {
    $scope.group = {
      sgroup_id: this.$parent.x.pk,
      name: this.$parent.x.fields.name,
      colour: rgbtohex(this.$parent.x.fields.colour),
      observation: this.$parent.x.fields.observation
    };
    $("#mgroup").openModal();
  };
  $scope.saveArea = function() {
    var data, form, k, v;
    data = $scope.dsector;
    data.saveds = true;
    form = new FormData();
    for (k in data) {
      v = data[k];
      console.log(k + " " + v);
      form.append(k, v);
    }
    if ($("[name=plane]").get(0).files.length > 0) {
      form.append("plane", $("[name=plane]").get(0).files[0]);
    }
    form.append("csrfmiddlewaretoken", $("[name=csrfmiddlewaretoken]").val());
    $.ajax({
      url: '',
      data: form,
      type: 'post',
      dataType: 'json',
      contentType: false,
      cache: false,
      processData: false,
      success: function(response) {
        if (response.status) {
          $scope.getDSectorList();
          $("#mdsector").closeModal();
        } else {
          swal("Error!", "No se guardo los datos. " + response.raise, "error");
        }
      }
    });
  };
  $scope.datechk = function() {
    var end, start;
    start = $scope.dsector.datestart.split("-");
    end = $scope.dsector.dateend.split("-");
    start = new Date(start[0], start[1], start[2]);
    end = new Date(end[0], end[1], end[2]);
    if (end < start) {
      console.log("fecha de termino menor a la de inicio");
    }
  };
  $scope.getDSectorList = function() {
    var data;
    data = {
      'listds': true
    };
    $http.get('', {
      params: data
    }).success(function(response) {
      if (response.status) {
        $scope.dslist = response.ds;
      } else {
        swal("Error!", "No se han obtenidos datos. " + response.raise, "error");
      }
    });
  };
  $scope.getPrices = function() {
    $http.get("", {
      params: {
        'valPrices': true
      }
    }).success(function(response) {
      if (response.status) {
        $scope.withoutPrices = response.list;
        console.log($scope.withoutPrices);
        console.log(response.list);
        $("#mwithoutprices").openModal();
        console.log("Se encontraron materielas sin precio");
      } else {
        swal("Alerta", "No se han encontrado materiales sin precios.", "warning");
      }
    });
  };
  $scope.savePricewithout = function($event) {
    var data;
    console.log($event);
    data = {
      savePricewithout: true,
      value: $event.target.value,
      materials: $event.target.dataset.materials,
      field: $event.target.dataset.field
    };
    $http({
      url: '',
      method: 'post',
      data: $.param(data)
    }).success(function(response) {
      if (!response.status) {
        swal("Error", "No se guardo el precio, Intentelo nuevamente.", "warning");
      }
    });
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

rgbtohex = function(rgb) {
  var array, b, g, r;
  if (typeof rgb !== "undefined" && rgb.length > 9) {
    array = rgb.split(',');
    r = parseInt(array[0].split('(')[1]);
    g = parseInt(array[1]);
    b = parseInt(array[2]);
    return "#" + (byte2Hex(r)) + (byte2Hex(g)) + (byte2Hex(b));
  } else {
    console.log("nothing rgba");
  }
};

byte2Hex = function(n) {
  var nybHexString;
  nybHexString = "0123456789ABCDEF";
  return String(nybHexString.substr((n >> 4) & 0x0F, 1)) + nybHexString.substr(n & 0x0F, 1);
};
