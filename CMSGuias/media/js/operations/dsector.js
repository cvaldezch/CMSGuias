var app;

app = angular.module('dsApp', ['ngCookies']).config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  return $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}).directive('stringToNumber', function() {
  return {
    require: 'ngModel',
    link: function(scope, element, attrs, ngModel) {
      ngModel.$parsers.push(function(value) {
        return '' + value;
      });
      ngModel.$formatters.push(function(value) {
        return parseFloat(value, 10);
      });
    }
  };
});

app.controller('DSCtrl', function($scope, $http, $cookies) {
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  angular.element(document).ready(function() {
    var $table;
    $('.modal-trigger').leanModal();
    $scope.getListAreaMaterials();
    $scope.getProject();
    $scope.listTypeNip();
    $table = $(".floatThead");
    $table.floatThead({
      position: 'absolute',
      top: 65,
      scrollContainer: function($table) {
        return $table.closest('.wrapper');
      }
    });
  });
  $scope.getListAreaMaterials = function() {
    var data;
    data = {
      dslist: true
    };
    $http.get("", {
      params: data
    }).success(function(response) {
      if (response.status) {
        $scope.dsmaterials = response.list;
        $(".floatThead").floatThead('reflow');
        $scope.inDropdownTable(".table-withoutApproved");
      } else {
        swal("Error!", "al obtener la lista de materiales del área", "error");
      }
    });
  };
  $scope.inDropdownTable = function(table) {
    if ($(table + " > tbody > tr").length > 0) {
      $('.dropdown-button').dropdown();
      return false;
    } else {
      setTimeout(function() {
        return $scope.inDropdownTable(table);
      }, 1400);
    }
  };
  $scope.saveMateial = function() {
    var data;
    data = $scope.mat;
    data.savepmat = true;
    data.ppurchase = $("[name=precio]").val();
    data.psales = $("[name=sales]").val();
    data.brand = $("[name=brand]").val();
    data.model = $("[name=model]").val();
    data.code = $(".id-mat").text();
    if (data.quantity <= 0) {
      swal("Alerta!", "Debe de ingresar una cantidad!", "warning");
      data.savepmat = false;
    }
    if (data.ppurchase <= 0) {
      swal("Alerta!", "Debe de ingresar un precio de Compra!", "warning");
      data.savepmat = false;
    }
    if (data.psales <= 0) {
      swal("Alerta!", "Debe de ingresar un precio de Venta!", "warning");
      data.savepmat = false;
    }
    if (data.savepmat) {
      $http({
        url: "",
        data: $.param(data),
        method: "post"
      }).success(function(response) {
        if (response.status) {
          $scope.getListAreaMaterials();
        } else {
          swal("Error", " No se guardado los datos", "error");
        }
      });
    }
  };
  $scope.getProject = function() {
    $http.get("/sales/projects/", {
      params: {
        'ascAllProjects': true
      }
    }).success(function(response) {
      if (response.status) {
        $scope.ascprojects = response.projects;
      } else {
        swal("Error", "No se a cargado los proyectos", "error");
      }
    });
  };
  $scope.getsector = function(project) {
    $http.get("/sales/projects/sectors/crud/", {
      params: {
        'pro': project,
        'sub': ''
      }
    }).success(function(response) {
      if (response.status) {
        $scope.ascsector = response.list;
      } else {
        swal("Error", "No se pudo cargar los datos del sector", "error");
      }
    });
  };
  $scope.ccopyps = function(sector) {
    swal({
      title: 'Copiar lista de Sector?',
      text: 'Realmente desea realizar la copia.',
      type: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#dd6b55',
      confirmButtonText: 'Si, Copiar',
      cancelButtonText: 'No, Cancelar',
      closeOnConfirm: true,
      closeOnCancel: true
    }, function(isConfirm) {
      var data;
      if (isConfirm) {
        if (sector) {
          data = {
            project: sector.substring(0, 7),
            sector: sector,
            copysector: true
          };
          $http({
            url: "",
            method: "post",
            data: $.param(data)
          }).success(function(response) {
            if (response.status) {
              location.reload();
            } else {
              swal("Error", "No se a guardado los datos.", "error");
            }
          });
        } else {
          swal("Alerta!", "El código de sector no es valido.", "warning");
        }
      }
    });
  };
  $scope.delAreaMA = function() {
    swal({
      title: 'Realmente desea eliminar?',
      text: 'toda la lista de materiales de esta area.',
      type: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#dd6b55',
      confirmButtonText: 'Si, Eliminar',
      cancelButtonText: 'No, Cancelar'
    }, function(isConfirm) {
      if (isConfirm) {
        $http({
          url: "",
          data: $.param({
            'delAreaMA': true
          }),
          method: 'post'
        }).success(function(response) {
          if (response.status) {
            location.reload();
          } else {
            swal("Alerta", "no se elimino los materiales del área", "warning");
          }
        });
      }
    });
  };
  $scope.availableNipple = function() {
    var mat;
    mat = this;
    swal({
      title: "Desea generar Niples de este materiales?",
      text: mat.$parent.x.fields.materials.fields.matnom + " " + mat.$parent.x.fields.materials.fields.matmed,
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#dd6b55",
      confirmButtonText: "Si, habilitar Niple",
      cancelButtonText: "No",
      timer: 2000
    }, function(isConfirm) {
      if (isConfirm) {
        $http({
          url: "",
          data: $.param({
            'availableNipple': true,
            'materials': mat.$parent.x.fields.materials.pk,
            'brand': mat.$parent.x.fields.brand.pk,
            'model': mat.$parent.x.fields.model.pk
          }),
          method: "post"
        }).success(function(response) {
          if (response.status) {
            swal("Información", "Nipple habilitado para el material", "info");
          }
        });
      }
    });
  };
  $scope.listNipple = function() {
    var data;
    data = {
      'lstnipp': true,
      'materials': this.$parent.x.fields.materials.pk
    };
    $http.get("", {
      params: data
    }).success(function(response) {
      var $dest, $det, $ori, script;
      if (response.status) {
        console.log(response);
        response.desc = function(type) {
          var k, ref, v;
          console.log(type);
          ref = response.dnip;
          for (k in ref) {
            v = ref[k];
            console.log(k, v);
            if (k === type) {
              return v;
            }
          }
        };
        script = "{{#nip}}<tr><td></td><td>{{fields.cantidad}}</td><td>{{desc(fields.tipo)}}</td><td>x</td><td>{{fields.materiales.fields.matmed}}</td><td>{{fields.metrado}}</td><td>{{fields.comment}}</td><td></td></tr>{{/nip}}";
        $det = $(".nip" + data.materials);
        $det.empty();
        $det.append(Mustache.render(script, response));
        $ori = $("#typenip > option").clone();
        $dest = $(".t" + data.materials);
        $dest.empty();
        $dest.append($ori);
      } else {
        console.log("nothing data");
      }
    });
  };
  $scope.listTypeNip = function() {
    $http.get("", {
      params: {
        'typeNipple': true
      }
    }).success(function(response) {
      if (response.status) {

      }
    });
  };
  $scope.saveNipple = function() {
    var data, row;
    row = this;
    console.log(row);
    data = {
      metrado: $("#nipple" + row.$parent.x.fields.materials.pk + "measure").val(),
      tipo: $("#nipple" + row.$parent.x.fields.materials.pk + "type").val(),
      cantidad: $("#nipple" + row.$parent.x.fields.materials.pk + "quantity").val(),
      cantshop: $("#nipple" + row.$parent.x.fields.materials.pk + "quantity").val(),
      comment: $("#nipple" + row.$parent.x.fields.materials.pk + "observation").val(),
      materiales: row.$parent.x.fields.materials.pk,
      nipplesav: true
    };
    console.log(data);
    if (data.measure === "") {
      swal("Alerta!", "No se ha ingresado una medida para este niple.", "warning");
      data.nipplesav = false;
    }
    if (data.quantity === "") {
      swal("Alerta!", "No se ha ingresado una cantidad para este niple.", "warning");
      data.nipplesav = false;
    }
    if (data.nipplesav) {
      $http({
        url: "",
        method: "post",
        data: $.param(data)
      }).success(function(response) {
        if (response.status) {
          $scope.listNipple();
        } else {
          swal("Error", "No se a guardado el niple.", "error");
        }
      });
    }
  };
  $scope.$watch('ascsector', function() {
    if ($scope.ascsector) {
      $scope.fsl = true;
      $scope.fpl = true;
    }
  });
  $scope.$watch('dsmaterials', function() {
    var count, k;
    count = 0;
    for (k in $scope.dsmaterials) {
      if ($scope.dsmaterials[k].fields.nipple) {
        count++;
      }
    }
    console.log(count);
    if (count) {
      $scope.snipple = true;
      setTimeout(function() {
        $('.collapsible').collapsible();
      }, 800);
    }
  });
});
