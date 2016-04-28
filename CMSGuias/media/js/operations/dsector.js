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

app.controller('DSCtrl', function($scope, $http, $cookies, $compile, $timeout) {
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  $scope.perarea = "";
  $scope.percharge = "";
  $scope.perdni = "";
  $scope.dataOrders = new Array();
  $scope.snip = [];
  $scope.nip = [];
  $scope.orders = [];
  $scope.ordersm = [];
  $scope.qon = [];
  $scope.radioO = [];
  $scope.sdnip = [];
  angular.element(document).ready(function() {
    var $table;
    $('.modal-trigger').leanModal();
    $table = $(".floatThead");
    $table.floatThead({
      position: 'absolute',
      top: 65,
      scrollContainer: function($table) {
        return $table.closest('.wrapper');
      }
    });
    if ($scope.modify > 0) {
      $scope.modifyList();
    } else {
      $scope.getListAreaMaterials();
      $scope.getProject();
      $scope.listTypeNip();
    }
    $('textarea#textarea1').characterCounter();
    $('.datepicker').pickadate({
      container: "body",
      closeOnSelect: true,
      min: new Date(),
      selectMonths: true,
      selectYears: 15,
      format: "yyyy-mm-dd"
    });
    $scope.perarea = angular.element("#perarea")[0].value;
    $scope.percharge = angular.element("#percharge")[0].value;
    $scope.perdni = angular.element("#perdni")[0].value;
  });
  $scope.getListAreaMaterials = function() {
    var data;
    $scope.dsmaterials = [];
    data = {
      dslist: true
    };
    $(".table-withoutApproved > thead").append("<tr class=\"white\"><td colspan=\"13\" class=\"center-align\"><div class=\"preloader-wrapper big active\"><div class=\"spinner-layer spinner-blue-only\"><div class=\"circle-clipper left\"><div class=\"circle\"></div></div><div class=\"gap-patch\"><div class=\"circle\"></div></div><div class=\"circle-clipper right\"><div class=\"circle\"></div></div></div></div></td></tr>");
    $http.get("", {
      params: data
    }).success(function(response) {
      if (response.status) {
        $(".table-withoutApproved > thead > tr").eq(1).remove();
        $scope.dsmaterials = response.list;
        $(".floatThead").floatThead('reflow');
        $scope.inDropdownTable(".table-withoutApproved");
        $('.dropdown-button').dropdown();
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
        $scope.inDropdownTable(table);
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
      if (Boolean($("#modify").length)) {
        delete data['savepmat'];
        data.savemmat = true;
      }
      if ($scope.mat.hasOwnProperty("obrand")) {
        if ($scope.mat.obrand) {
          data.editmat = true;
        }
      }
      $http({
        url: "",
        data: $.param(data),
        method: "post"
      }).success(function(response) {
        if (response.status) {
          Materialize.toast("Material Agregado", 2600);
          if (Boolean($("#modify").length)) {
            $scope.modifyList();
            return;
          } else {
            $scope.getListAreaMaterials();
            if ($scope.mat.hasOwnProperty("obrand")) {
              $scope.mat.obrand = null;
              $scope.mat.omodel = null;
            }
            return;
          }
        } else {
          swal("Error", " No se guardado los datos", "error");
        }
      });
    }
  };
  $scope.deleteDMaterial = function($event) {
    swal({
      title: "Eliminar material?",
      text: "realmente dese eliminar el material.",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#dd6b55",
      confirmButtonText: "Si!, eliminar",
      closeOnConfirm: true,
      closeOnCancel: true
    }, function(isConfirm) {
      var data;
      if (isConfirm) {
        data = $event.currentTarget.dataset;
        data.delmat = true;
        $http({
          url: '',
          method: 'post',
          data: $.param(data)
        }).success(function(response) {
          if (response.status) {
            $scope.getListAreaMaterials();
          }
        });
      }
    });
  };
  $scope.editDMaterial = function($event) {
    $scope.mat.code = $event.currentTarget.dataset.materials;
    $timeout((function() {
      var e;
      e = $.Event('keypress', {
        keyCode: 13
      });
      $("[name=code]").trigger(e);
    }), 100);
    $timeout((function() {
      var quantity;
      quantity = parseFloat($event.currentTarget.dataset.quantity);
      $scope.gui.smat = true;
      $("[name=brand]").val($event.currentTarget.dataset.brand);
      $("[name=model]").val($event.currentTarget.dataset.model);
      $scope.mat = {
        quantity: parseFloat(quantity),
        obrand: $event.currentTarget.dataset.brand,
        omodel: $event.currentTarget.dataset.model
      };
    }), 300);
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
      title: "Desea generar Niples para este material?",
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
        script = "{{#nip}}<tr class=\"text-12\"><td class=\"center-align\">{{index}}</td><td class=\"center-align\">{{fields.cantidad}}</td><td class=\"center-align\">{{fields.cantshop}}</td><td class=\"center-align\">{{fields.tipo}}</td><td>Niple {{#desc}}{{>fields.tipo}}{{/desc}}</td><td>{{fields.materiales.fields.matmed}}</td><td>x</td><td>{{fields.metrado}} cm</td><td>{{fields.comment}}</td><td><a href=\"#\" ng-click=\"nedit($event)\" data-pk=\"{{pk}}\" data-materials=\"{{fields.materiales.pk}}\" ng-if=\"perarea == 'administrator' || perarea == 'ventas' || perarea == 'operaciones' || percharge == 'jefe de almacen'\"><i class=\"fa fa-edit\"></i></a></td><td><a href=\"#\" ng-click=\"ndel($event)\" data-pk=\"{{pk}}\" data-materials=\"{{fields.materiales.pk}}\" class=\"red-text text-darken-1\" ng-if=\"perarea == 'administrator' || perarea == 'ventas' || perarea == 'operaciones' || percharge == 'jefe de almacen'\"><i class=\"fa fa-trash\"></i></a></td></tr>{{/nip}}";
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
      if ((nw < (meter * quantity)) || nw > (meter * quantity)) {
        dis += Math.abs((meter * quantity) - nw);
      } else if (nw === (meter * quantity)) {
        dis += meter * quantity;
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
            $(".rf" + data.materiales).trigger("click");
          }, 100);
        } else {
          swal("Error", "No se a guardado el niple.", "error");
        }
      });
    }
  };
  $scope.showModify = function() {
    var data;
    $scope.btnmodify = true;
    data = {
      modifyArea: true
    };
    $http({
      url: '',
      method: 'post',
      data: $.param(data)
    }).success(function(response) {
      if (response.status) {
        location.reload();
      } else {
        swal("Error", "No se a podido iniciar la modificación.", "error");
      }
    });
  };
  $scope.modifyList = function() {
    var data;
    data = {
      modifyList: true
    };
    $http.get('', {
      params: data
    }).success(function(response) {
      if (response.status) {
        $scope.lmodify = response.modify;
        $scope.calcMM();
      } else {
        swal('Error', 'no se a encontrado datos', 'error');
      }
    });
  };
  $scope.showEditM = function($event) {
    var elem;
    elem = this;
    $http.get('/brand/list/', {
      params: {
        'brandandmodel': true
      }
    }).success(function(response) {
      var bel, btmp, mel, mtmp;
      if (response.status) {
        $scope.brand = response;
        $scope.model = response;
        response.ifbrand = function() {
          if (this.pk === elem.$parent.x.fields.brand.pk) {
            return "selected";
          }
        };
        response.ifmodel = function() {
          if (this.pk === elem.$parent.x.fields.model.pk) {
            return "selected";
          }
        };
        btmp = "<select class=\"browser-default\" ng-blur=\"saveEditM($event)\" name=\"brand\" data-old=\"" + elem.$parent.x.fields.brand.pk + "\">{{#brand}}<option value=\"{{pk}}\" {{ifbrand}}>{{fields.brand}}</option>{{/brand}}</select>";
        mtmp = "<select class=\"browser-default\" ng-blur=\"saveEditM($event)\" name=\"model\" data-old=\"" + elem.$parent.x.fields.model.pk + "\">{{#model}}<option value=\"{{pk}}\" {{ifmodel}}>{{fields.model}}</option>{{/model}}</select>";
        bel = Mustache.render(btmp, response);
        mel = Mustache.render(mtmp, response);
        $($event.currentTarget.children[3]).html($compile(bel)($scope));
        $($event.currentTarget.children[4]).html($compile(mel)($scope));
        $($event.currentTarget.children[7]).html($compile("<input type=\"number\" ng-blur=\"saveEditM($event)\" name=\"quantity\" min=\"1\" value=\"" + elem.$parent.x.fields.quantity + "\" data-old=\"" + elem.$parent.x.fields.quantity + "\" class=\"right-align\">")($scope));
        $($event.currentTarget.children[8]).html($compile("<input type=\"number\" ng-blur=\"saveEditM($event)\" name=\"ppurchase\" min=\"0\" value=\"" + elem.$parent.x.fields.ppurchase + "\" data-old=\"" + elem.$parent.x.fields.ppurchase + "\" class=\"right-align\">")($scope));
        $($event.currentTarget.children[9]).html($compile("<input type=\"number\" ng-blur=\"saveEditM($event)\" name=\"psales\" min=\"0\" value=\"" + elem.$parent.x.fields.psales + "\" data-old=\"" + elem.$parent.x.fields.psales + "\" class=\"right-align\">")($scope));
      }
    });
  };
  $scope.saveEditM = function($event) {
    var data;
    data = {
      materials: $event.currentTarget.parentElement.parentElement.children[1].innerText,
      name: $event.currentTarget.name,
      value: $event.currentTarget.value
    };
    if (data.name === "brand") {
      data.brand = $event.currentTarget.dataset.old;
      if (data.value === data.brand) {
        return false;
      }
    } else {
      data.brand = $event.currentTarget.parentElement.parentElement.children[3].children[0].value;
    }
    if (data.name === "model") {
      data.model = $event.currentTarget.dataset.old;
      if (data.value === data.model) {
        return false;
      }
    } else {
      data.model = $event.currentTarget.parentElement.parentElement.children[4].children[0].value;
    }
    if (data.name === 'quantity' || data.name === 'ppurchase' || data.name === 'psales') {
      if (parseFloat(data.value) === parseFloat($event.currentTarget.dataset.old)) {
        return false;
      }
    }
    data.editMM = true;
    $http({
      url: '',
      method: 'post',
      data: $.param(data)
    }).success(function(response) {
      var x;
      if (response.status) {
        $scope.calcMM();
        for (x in $scope.lmodify) {
          if ($scope.lmodify[x].fields.materials.pk === $event.currentTarget.parentElement.parentElement.children[1].innerText && $scope.lmodify[x].fields.brand.pk === data.brand && $scope.lmodify[x].fields.model.pk === data.model) {
            if (data.name === "brand") {
              $scope.lmodify[x].fields.brand.pk = $event.currentTarget.parentElement.parentElement.children[3].children[0].selectedOptions[0].value;
              $scope.lmodify[x].fields.brand.fields.brand = $event.currentTarget.parentElement.parentElement.children[3].children[0].selectedOptions[0].innerText;
              $event.currentTarget.dataset.old = $scope.lmodify[x].fields.brand.pk;
            }
            if (data.name === "model") {
              $scope.lmodify[x].fields.brand.pk = $event.currentTarget.parentElement.parentElement.children[4].children[0].selectedOptions[0].value;
              $scope.lmodify[x].fields.brand.fields.brand = $event.currentTarget.parentElement.parentElement.children[4].children[0].selectedOptions[0].innerText;
              $event.currentTarget.dataset.old = $scope.lmodify[x].fields.model.pk;
            }
            if (data.name === "quantity") {
              $scope.lmodify[x].fields.quantity = data.value;
              $event.currentTarget.dataset.old = $scope.lmodify[x].fields.quantity;
            }
            if (data.name === "ppurchase") {
              $scope.lmodify[x].fields.ppurchase = data.value;
              $event.currentTarget.dataset.old = $scope.lmodify[x].fields.ppurchase;
            }
            if (data.name === "psales") {
              $scope.lmodify[x].fields.psales = data.value;
              $event.currentTarget.dataset.old = $scope.lmodify[x].fields.psales;
            }
            break;
          }
        }
        Materialize.toast('Guardado OK', 1500, 'rounded');
      } else {
        Materialize.toast("Error, no se guardo, " + response.raise, 1500);
      }
    });
  };
  $scope.closeEditM = function($event) {
    var x;
    for (x in $scope.lmodify) {
      if ($scope.lmodify[x].fields.materials.pk === $event.currentTarget.parentElement.parentElement.children[1].innerText && $scope.lmodify[x].fields.brand.pk === $event.currentTarget.parentElement.parentElement.children[3].children[0].selectedOptions[0].value && $scope.lmodify[x].fields.model.pk === $event.currentTarget.parentElement.parentElement.children[4].children[0].selectedOptions[0].value) {
        $event.currentTarget.parentElement.parentElement.children[3].innerHTML = $scope.lmodify[x].fields.brand.fields.brand;
        $event.currentTarget.parentElement.parentElement.children[4].innerHTML = $scope.lmodify[x].fields.model.fields.model;
        $event.currentTarget.parentElement.parentElement.children[7].innerHTML = $scope.lmodify[x].fields.quantity;
        $event.currentTarget.parentElement.parentElement.children[8].innerHTML = $scope.lmodify[x].fields.ppurchase;
        $event.currentTarget.parentElement.parentElement.children[9].innerHTML = $scope.lmodify[x].fields.psales;
        break;
      }
    }
  };
  $scope.delEditM = function($event) {
    swal({
      title: "Eliminar Material?",
      text: "" + $event.currentTarget.parentElement.parentElement.children[2].innerText,
      type: "warning",
      showCancelButton: true,
      confirmButtonText: "Si!, eliminar",
      confirmButtonColor: "#dd6b55",
      cancelButtonText: "No!",
      closeOnConfirm: true
    }, function(isConfirm) {
      var data;
      if (isConfirm) {
        data = {
          materials: $event.currentTarget.parentElement.parentElement.children[1].innerText,
          brand: $event.currentTarget.dataset.brand,
          model: $event.currentTarget.dataset.model,
          delMM: true
        };
        return $http({
          url: "",
          method: "post",
          data: $.param(data)
        }).success(function(response) {
          if (response.status) {
            Materialize.toast("Se elimino correctamente", 1500);
            $scope.modifyList();
          } else {
            swal("Error", "No se a podido eliminar el material, intentelo otra vez.", "error");
          }
        });
      }
    });
  };
  $scope.calcMM = function() {
    $http.get("", {
      params: {
        samountp: true
      }
    }).success(function(response) {
      $scope.amnp = response.maarea.tpurchase;
      $scope.amns = response.maarea.tsales;
      $scope.ammp = response.mmodify.apurchase;
      $scope.amms = response.mmodify.asale;
      $scope.amsecp = response.sec[0].fields.amount;
      $scope.amsecs = response.sec[0].fields.amountsales;
      $scope.amstp = response.msector.tpurchase;
      return $scope.amsts = response.msector.tsales;
    });
  };
  $scope.delAllModifyArea = function($event) {
    swal({
      title: 'Anular Modificación?',
      text: 'se eliminara cualquier modificación realizada.',
      type: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#dd6b55',
      confirmButtonText: 'Anular Modificación',
      cancelButtonText: 'No!'
    }, function(isConfirm) {
      var data;
      if (isConfirm) {
        data = {
          'annModify': true
        };
        $http({
          url: '',
          method: 'post',
          data: $.param(data)
        }).success(function(response) {
          if (response.status) {
            $timeout((function() {
              location.reload();
            }), 2600);
          } else {
            swal("Alerta!", "No se a realizado la acción. " + response.raise, "error");
          }
        });
      }
    });
  };
  $scope.approvedModify = function($event) {
    swal({
      title: "Aprobar modificación?",
      text: "Desea aprobar las modificaciones del área?",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#dd6b55",
      confirmButtonText: "Si!, Aprobar",
      closeOnConfirm: true,
      closeOnCancel: true
    }, function(isConfirm) {
      var data;
      if (isConfirm) {
        $event.currentTarget.disabled = true;
        $event.currentTarget.innerHTML = "<i class=\"fa fa-spinner fa-pulse\"></i> Procesando";
        data = {
          approvedModify: true
        };
        $http({
          url: "",
          method: "post",
          data: $.param(data)
        }).success(function(response) {
          if (response.status) {
            Materialize.toast("Se Aprobó!");
            $timeout((function() {
              location.reload();
            }), 800);
          } else {
            $event.currentTarget.className = "btn red grey-text text-darken-1";
            $event.currentTarget.innerHTML = "<i class=\"fa fa-timescircle\"></i> Error!";
          }
        });
      }
    });
  };
  $scope.showCommentMat = function() {
    $("#commentm").openModal();
    $("#mcs").val(this.$parent.x.fields.materials.pk).attr("data-brand", this.$parent.x.fields.brand.pk).attr("data-model", this.$parent.x.fields.model.pk);
    $scope.mmc = this.$parent.x.fields.comment;
    console.log(this.$parent.x.fields.comment);
    $scope.lblmcomment = this.$parent.x.fields.materials.fields.matnom + " " + this.$parent.x.fields.materials.fields.matmed;
  };
  $scope.saveComment = function($event) {
    var $d, data;
    $d = $("#mcs");
    data = {
      materials: $d.val(),
      brand: $d.attr("data-brand"),
      model: $d.attr("data-model"),
      comment: $scope.mmc,
      saveComment: true
    };
    $event.currentTarget.disabled = true;
    $event.currentTarget.innerHTML = "<i class=\"fa fa-spinner fa-pulse\"></i> Procesando";
    $http({
      url: "",
      method: "post",
      data: $.param(data)
    }).success(function(response) {
      $event.currentTarget.disabled = false;
      $event.currentTarget.innerHTML = "<i class=\"fa fa-floppy-o\"></i> GUARDAR";
      if (response.status) {
        $scope.mmc = '';
        $("#commentm").closeModal();
      }
    });
  };
  $scope.changeSelOrder = function($event) {
    $("[name=chkorders]").each(function(index, element) {
      $(element).prop("checked", Boolean(parseInt($event.currentTarget.value)));
    });
  };
  $scope.pOrders = function($event) {
    var data;
    data = new Array();
    $("[name=chkorders]").each(function(index, element) {
      var $e;
      $e = $(element);
      if ($e.is(":checked")) {
        data.push({
          "id": $e.val(),
          "name": $e.attr("data-nme"),
          "unit": $e.attr("data-unit"),
          "brandid": $e.attr("data-brandid"),
          "modelid": $e.attr("data-modelid"),
          "brand": $e.attr("data-brand"),
          "model": $e.attr("data-model"),
          "quantity": parseFloat($e.attr("data-quantity")),
          "qorders": $e.attr("data-quantity"),
          "nipple": $e.attr("data-nipple")
        });
      }
    });
    if (data.length) {
      $scope.dataOrders = data;
      $("#morders").openModal();
      return;
    }
  };
  $scope.changeQOrders = function($event) {
    var i, len, ref, x;
    if (parseFloat($event.currentTarget.value) > parseFloat($event.currentTarget.dataset.qmax)) {
      $event.currentTarget.value = $event.currentTarget.dataset.qmax;
    }
    ref = $scope.dataOrders;
    for (i = 0, len = ref.length; i < len; i++) {
      x = ref[i];
      if (x.id === $event.currentTarget.dataset.materials) {
        x.qorders = $event.currentTarget.value;
      }
    }
  };
  $scope.deleteItemOrders = function($event) {
    var count, i, len, ref, x;
    count = 0;
    ref = $scope.dataOrders;
    for (i = 0, len = ref.length; i < len; i++) {
      x = ref[i];
      if (x.id === $event.currentTarget.value) {
        $scope.dataOrders.splice(count, 1);
        console.log("item delete");
      }
      count++;
    }
  };
  $scope.getNippleMaterials = function($event) {
    var data;
    data = {
      nippleOrders: true,
      materials: $event.currentTarget.value
    };
    if (!$scope.snip["" + data.materials]) {
      $http.get("", {
        params: data
      }).success(function(response) {
        console.log(response);
        if (response.status) {
          console.log($scope.snip);
          $scope.snip["" + data.materials] = !$scope.snip["" + data.materials];
          $scope.nip["" + data.materials] = response.nipple;
        }
      });
    } else {
      $scope.snip["" + data.materials] = !$scope.snip["" + data.materials];
    }
  };
  $scope.sumNipple = function($event) {
    $timeout(function() {
      var amount;
      $scope.ordersm["" + $event.currentTarget.value] = 0;
      amount = 0;
      $("[name=selno" + $event.currentTarget.value + "]").each(function(index, element) {
        var $e, $np;
        $e = $(element);
        if ($e.is(":checked")) {
          $np = $("#n" + ($e.attr("data-nid")));
          amount += parseInt($np.val()) * parseFloat($np.attr("data-measure"));
        }
      });
      return $scope.ordersm["" + $event.currentTarget.value] = amount / 100;
    }, 200);
  };
  $scope.saveOrdersStorage = function($event) {
    console.log($scope.orders);
    console.log($scope.ordersm);
    swal({
      title: "Desea generar la orden?",
      text: '',
      type: "warning",
      showCancelButton: true,
      confirmButtonText: 'Si!, Generar!',
      confirmButtonColor: '#dd6b55',
      cancelButtonText: 'No',
      closeOnConfirm: true,
      closeOnCancel: true
    }, function(isConfirm) {
      var $file, arn, data, det, i, k, len, n, nipples, ref, ref1, v;
      if (isConfirm) {
        arn = new Array;
        nipples = new Array;
        for (n in $scope.dataOrders) {
          if (JSON.parse($scope.dataOrders[n].nipple)) {
            arn.push($scope.dataOrders[n].id);
          }
        }
        console.log(arn);
        if (arn.length) {
          for (i = 0, len = arn.length; i < len; i++) {
            n = arn[i];
            $("[name=selno" + n).each(function(index, element) {
              var $e, $np;
              $e = $(element);
              if ($e.is(":checked")) {
                $np = $("#n" + ($e.attr("data-nid")));
                nipples.push({
                  'id': $e.attr("data-nid"),
                  'm': n,
                  'quantity': $np.val(),
                  'measure': $np.attr("data-measure")
                });
              }
            });
          }
        }
        console.log(nipples);
        det = new Array();
        ref = $scope.ordersm;
        for (k in ref) {
          v = ref[k];
          console.log(k, v);
          if (v <= 0) {
            swal("", "Los materiales deben de tener una cantidad mayor a 0", "warning");
            break;
            return false;
          } else {
            det.push({
              'materials': k,
              'quantity': v
            });
          }
        }
        data = new FormData;
        if (!$scope.orders.hasOwnProperty("transfer")) {
          swal("", "Debe de seleccionar una fecha para la envio.", "warning");
          return false;
        }
        if (!$scope.orders.hasOwnProperty("storage")) {
          swal("", "Debe de seleccionar un almacén.", "warning");
          return false;
        }
        $file = $("#ordersfiles")[0];
        if ($file.files.length) {
          data.append("ordersf", $file.files[0]);
        }
        ref1 = $scope.orders;
        for (k in ref1) {
          v = ref1[k];
          data.append(k, v);
        }
        console.log(data);
        data.append("details", JSON.stringify(det));
        data.append("saveOrders", true);
        if (nipples.length) {
          data.append("nipples", JSON.stringify(nipples));
        }
        console.log($event);
        data.append("csrfmiddlewaretoken", $("[name=csrfmiddlewaretoken]").val());
        $.ajax({
          url: "",
          data: data,
          type: "post",
          dataType: "json",
          processData: false,
          contentType: false,
          cache: false,
          sendBefore: function(object, result) {
            $event.target.disabled = true;
            $event.target.innerHTML = "<i class=\"fa fa-cog fa-spin\"></i>";
          },
          success: function(response) {
            if (response.status) {
              swal("" + response.orders, "Felicidades! Orden generada.", "success");
              $timeout(function() {
                location.reload();
              }, 2600);
            } else {
              swal("Error", "al procesar. " + response.raise, "error");
              $event.target.disabled = false;
              $event.target.className = "btn red grey-text text-darken-1";
              $event.target.innerHTML = "<i class=\"fa fa-timescircle\"></i> Error!";
            }
          }
        });
      }
    });
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
  $scope.$watch('gui.smat', function() {
    $(".floatThead").floatThead('reflow');
  });
});
