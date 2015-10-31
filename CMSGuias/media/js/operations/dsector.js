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

app.controller('DSCtrl', function($scope, $http, $cookies, $compile) {
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
      var $dest, $det, $edit, $ori, count, el, script, tbs;
      if (response.status) {
        count = 1;
        response.desc = function() {
          return function(type, render) {
            var k, ref, v;
            ref = response.dnip;
            for (k in ref) {
              v = ref[k];
              if (k === this.fields.tipo) {
                return render(v);
              }
            }
          };
        };
        response.index = function() {
          return count++;
        };
        script = "{{#nip}}<tr class=\"text-12\"><td class=\"center-align\">{{index}}</td><td class=\"center-align\">{{fields.cantidad}}</td><td class=\"center-align\">{{fields.cantshop}}</td><td class=\"center-align\">{{fields.tipo}}</td><td>Niple {{#desc}}{{>fields.tipo}}{{/desc}}</td><td>{{fields.materiales.fields.matmed}}</td><td>x</td><td>{{fields.metrado}} cm</td><td>{{fields.comment}}</td><td><a href=\"#\" ng-click=\"nedit($event)\" data-pk=\"{{pk}}\" data-materials=\"{{fields.materiales.pk}}\"><i class=\"fa fa-edit\"></i></a></td><td><a href=\"#\" ng-click=\"ndel($event)\" data-pk=\"{{pk}}\" data-materials=\"{{fields.materiales.pk}}\" class=\"red-text text-darken-1\"><i class=\"fa fa-trash\"></i></a></td></tr>{{/nip}}";
        $det = $(".nip" + data.materials);
        $det.empty();
        tbs = Mustache.render(script, response);
        el = $compile(tbs)($scope);
        $det.html(el);
        $ori = $("#typenip > option").clone();
        $dest = $(".t" + data.materials);
        $dest.empty();
        $dest.append($ori);
        $scope.calNipple(data.materials);
        $edit = $("#nipple" + data.materials + "edit");
        $edit.val("");
        $edit.removeAttr("data-materials");
        $edit.removeAttr("data-meter");
        $edit.removeAttr("data-quantity");
      } else {
        console.log("nothing data");
      }
    });
  };
  $scope.calNipple = function(materials) {
    var dis, ing, tot;
    tot = parseFloat($(".to" + materials).text() * 100);
    ing = 0;
    $(".nip" + materials + " > tr").each(function() {
      var $td;
      $td = $(this).find("td");
      ing += parseFloat($td.eq(1).text()) * parseFloat($td.eq(7).text().split(" cm"));
    });
    dis = tot - ing;
    console.log(tot);
    console.log(ing);
    console.log(dis);
    $(".co" + materials).html(ing);
    $(".dis" + materials).html(dis);
  };
  $scope.ndel = function($event) {
    swal({
      title: "Eliminar Niple?",
      text: $event.target.offsetParent.parentElement.childNodes[1].innerText + " " + $event.target.offsetParent.parentElement.childNodes[4].innerText + " " + $event.target.offsetParent.parentElement.childNodes[7].innerText,
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#dd6b55",
      confirmButtonText: "Si, eliminar!",
      cancelButtonText: "No!",
      closeOnCancel: true,
      closeOnConfirm: true
    }, function(isConfirm) {
      var data;
      if (isConfirm) {
        data = {
          delnipp: true,
          id: $event.currentTarget.dataset.pk,
          materials: $event.currentTarget.dataset.materials
        };
        $http({
          url: "",
          method: "post",
          data: $.param(data)
        }).success(function(response) {
          var $edit;
          if (response.status) {
            $edit = $("#nipple" + data.materials + "edit");
            $edit.val("");
            $edit.removeAttr("data-materials");
            $edit.removeAttr("data-meter");
            $edit.removeAttr("data-quantity");
            setTimeout(function() {
              $(".rf" + data.materials).trigger('click');
            }, 100);
          } else {
            swal("Error", "No se a eliminado el niple", "error");
          }
        });
      }
    });
  };
  $scope.nedit = function($event) {
    var materials;
    materials = $event.currentTarget.dataset.materials;
    $("#nipple" + materials + "measure").val($event.target.offsetParent.parentElement.childNodes[7].innerText.split(" cm")[0]);
    $("#nipple" + materials + "type").val($event.target.offsetParent.parentElement.childNodes[3].innerText);
    $("#nipple" + materials + "quantity").val($event.target.offsetParent.parentElement.childNodes[1].innerText);
    $("#nipple" + materials + "observation").val($event.target.offsetParent.parentElement.childNodes[8].innerText);
    $("#nipple" + materials + "edit").val($event.currentTarget.dataset.pk).attr("data-materials", materials).attr("data-quantity", $event.target.offsetParent.parentElement.childNodes[1].innerText).attr("data-meter", $event.target.offsetParent.parentElement.childNodes[7].innerText.split(" cm")[0]);
    setTimeout(function() {
      $(".sdnip" + materials).click();
    }, 100);
  };
  $scope.listTypeNip = function() {
    $http.get("", {
      params: {
        'typeNipple': true
      }
    }).success(function(response) {
      if (response.status) {
        $scope.tnipple = response.type;
      }
    });
  };
  $scope.saveNipple = function() {
    var $edit, cl, data, dis, meter, nw, quantity, row;
    row = this;
    data = {
      metrado: $("#nipple" + row.$parent.x.fields.materials.pk + "measure").val(),
      tipo: $("#nipple" + row.$parent.x.fields.materials.pk + "type").val(),
      cantidad: $("#nipple" + row.$parent.x.fields.materials.pk + "quantity").val(),
      cantshop: $("#nipple" + row.$parent.x.fields.materials.pk + "quantity").val(),
      comment: $("#nipple" + row.$parent.x.fields.materials.pk + "observation").val(),
      materiales: row.$parent.x.fields.materials.pk,
      nipplesav: true
    };
    if (data.measure === "") {
      swal("Alerta!", "No se ha ingresado una medida para este niple.", "warning");
      data.nipplesav = false;
    }
    if (data.quantity === "") {
      swal("Alerta!", "No se ha ingresado una cantidad para este niple.", "warning");
      data.nipplesav = false;
    }
    $edit = $("#nipple" + data.materiales + "edit");
    dis = parseFloat($(".dis" + data.materiales).text());
    nw = parseFloat(data.cantidad) * parseFloat(data.metrado);
    if ($edit.val() !== "") {
      data.edit = true;
      data.id = $edit.val();
      data.materiales = $edit.attr("data-materials");
      meter = parseFloat($edit.attr("data-meter"));
      quantity = parseFloat($edit.attr("data-quantity"));
      if (nw <= (meter * quantity)) {
        dis += (meter * quantity) - nw;
      }
    }
    console.log(dis);
    console.log(nw);
    cl = dis - nw;
    console.log(cl);
    if (cl < 0) {
      swal("Alerta!", "La cantidad ingresada es mayor a la cantidad disponible de la tuberia.", "warning");
      data.nipplesav = false;
    }
    if (data.nipplesav) {
      $http({
        url: "",
        method: "post",
        data: $.param(data)
      }).success(function(response) {
        if (response.status) {
          $edit.val("").removeAttr("data-materials", "").removeAttr("data-quantity", "").removeAttr("data-meter", "");
          $("#nipple" + data.materiales + "measure").val("");
          $("#nipple" + data.materiales + "type").val("");
          $("#nipple" + data.materiales + "quantity").val("");
          $("#nipple" + data.materiales + "quantity").val("");
          $("#nipple" + data.materiales + "observation").val("");
          setTimeout(function() {
            $(".rf" + data.materiales).trigger('click');
          }, 100);
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
    if (count) {
      $scope.snipple = true;
      setTimeout(function() {
        $('.collapsible').collapsible();
      }, 800);
    }
  });
});
