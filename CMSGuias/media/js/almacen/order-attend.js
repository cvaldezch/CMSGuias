var app, controllers, factories;

app = angular.module('attendApp', ['ngCookies', 'angular.filter']);

app.config(function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.directive('cinmam', function($parse) {
  return {
    restrict: 'A',
    require: '?ngModel',
    scope: '@',
    link: function(scope, element, attrs, ngModel) {
      element.bind('change, blur', function(event) {
        var max, min, result, val;
        if (!isNaN(element.context.value) && element.context.value !== "") {
          val = parseFloat(element.context.value);
        } else {
          val = parseFloat(attrs.max);
        }
        max = parseFloat(attrs.max);
        min = parseFloat(attrs.min);
        result = 0;
        if (val > max) {
          result = max;
        } else if (val < min) {
          result = min;
        } else {
          result = val;
        }
        if (attrs.hasOwnProperty('ngModel')) {
          ngModel.$setViewValue(result);
          ngModel.$render();
          scope.$apply();
        } else {
          element.context.value = result;
        }
      });
    }
  };
});

factories = function($http, $cookies) {
  var obj;
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  obj = new Object;
  obj.getDetailsOrder = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get("", {
      params: options
    });
  };
  obj.getDetNiples = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get("", {
      params: options
    });
  };
  obj.getStockItem = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get("", {
      params: options
    });
  };
  obj.valNGuide = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get("", {
      params: options
    });
  };
  obj.getCarrier = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get("/json/get/carries/", {
      params: options
    });
  };
  obj.getTransport = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get("/json/get/list/transport/" + options.ruc + "/", {
      params: options
    });
  };
  obj.getConductor = function(options) {
    if (options == null) {
      options = {};
    }
    return $http.get("/json/get/list/conductor/" + options.ruc + "/", {
      params: options
    });
  };
  return obj;
};

app.factory('attendFactory', factories);

controllers = function($scope, $timeout, $q, attendFactory) {
  var validStock;
  $scope.dorders = [];
  $scope.vstock = false;
  $scope.cstock = new Array();
  $scope.qmax = 0;
  $scope.stks = [];
  $scope.dguide = new Array();
  $scope.fchk = new Array();
  $scope.nipdetails = new Array();
  $scope.ngvalid = false;
  angular.element(document).ready(function() {
    angular.element(".modal-trigger").leanModal();
    if ($scope.init === true) {
      angular.element(".datepicker").pickadate({
        container: 'body',
        format: 'yyyy-mm-dd',
        min: new Date(),
        selectMonths: true,
        selectYears: 15
      });
      $scope.sDetailsOrders();
      $timeout(function() {
        $scope.getCarrier();
      }, 2000);
    }
  });
  $scope.getCarrier = function() {
    console.log("REQUEST DATA CARRIER");
    attendFactory.getCarrier().success(function(response) {
      console.log("DATOS DE CARRIER EXTRACT ", response);
      if (response.status) {
        $scope.carriers = response.carrier;
      } else {
        Materialize.toast("Transportista sin datos!", 3600);
      }
    });
  };
  $scope.getTransport = function() {
    var prms;
    console.log("EXECUTE JSON TRANSPORT");
    prms = {
      'ruc': $scope.carrier
    };
    attendFactory.getTransport(prms).success(function(response) {
      if (response.status) {
        $scope.transports = response.list;
        console.log($scope.transports);
      } else {
        Materialize.toast("Transporte sin datos!", 3600);
      }
    });
  };
  $scope.getConductor = function() {
    var prms;
    console.log("EXECUTE JSON CONDUCTOR");
    prms = {
      'ruc': $scope.carrier
    };
    attendFactory.getConductor(prms).success(function(response) {
      if (response.status) {
        $scope.conductors = response.list;
        console.log($scope.conductors);
      } else {
        Materialize.toast("Conductor sin datos!", 3600);
      }
    });
  };
  $scope.changeAttend = function($index) {
    var b, k, m, o, obj, ref;
    if (!$scope.fchk[$index].status) {
      $scope.fchk[$index].quantity = 0;
      angular.forEach($scope.dguide, function(obj, index) {
        var b, m, o;
        m = $scope.fchk[$index].materials === obj.materials;
        b = $scope.fchk[$index].brand === obj.brand;
        o = ($scope.fchk[$index].model = obj.model);
        if (m && b && o) {
          console.log(obj);
          console.warn($scope.fchk[$index]);
          $scope.dguide.splice(index, 1);
          console.info($scope.dguide);
        }
      });
      ref = $scope.nipdetails;
      for (k in ref) {
        obj = ref[k];
        m = $scope.fchk[$index].materials === obj.materials;
        b = $scope.fchk[$index].brand === obj.brand;
        o = ($scope.fchk[$index].model = obj.model);
        if (m && b && o) {
          $scope.nipdetails.splice(k, 1);
        }
      }
      $scope.enableGuide();
    }
  };
  $scope.sDetailsOrders = function() {
    attendFactory.getDetailsOrder({
      'details': true
    }).success(function(response) {
      if (response.status) {
        $timeout(function() {
          $scope.dorders = response.details;
          $scope.getNiple();
          return console.log("is execute!!");
        }, 80);
      } else {
        console.log("error in data " + response.raise);
      }
    });
  };
  $scope.getDetailsOrder = function() {
    attendFactory.getDetailsOrder({
      'details': true
    }).success(function(response) {
      if (response.status) {
        $scope.sdetails = response.details;
        angular.element("#midetails").openModal();
      } else {
        Materialize.toast('No hay datos para mostrar', 3600, 'rounded');
      }
    });
  };
  $scope.getNiple = function() {
    attendFactory.getDetNiples({
      'detailsnip': true
    }).success(function(response) {
      var tmp;
      if (response.status) {
        tmp = new Array();
        angular.forEach(response.nip, function(value) {
          tmp.push({
            'id': value.pk,
            'materials': value.fields.materiales.pk,
            'name': value.fields.materiales.fields.matnom + " " + value.fields.materiales.fields.matmed + " " + value.fields.materiales.fields.unidad,
            'description': "Niple " + response.types[value.fields.tipo] + " ",
            'brand': value.fields.brand.pk,
            'bname': value.fields.brand.fields.brand,
            'model': value.fields.model.pk,
            'mname': value.fields.model.fields.model,
            'tipo': value.fields.tipo,
            'meter': value.fields.metrado,
            'quantity': value.fields.cantidad,
            'send': value.fields.cantshop,
            'guide': value.fields.cantguide,
            'tag': value.fields.tag
          });
        });
        $scope.nTypes = response.types;
        $scope.dnip = tmp;
      } else {
        Materialize.toast("Error " + response.raise, 3000, 'rounded');
      }
    });
  };
  $scope.chkAll = function() {
    var selected;
    selected = function() {
      var deferred, promises;
      deferred = $q.defer();
      promises = new Array();
      angular.forEach($scope.fchk, function(obj, index) {
        obj.status = $scope.chk;
        if (!$scope.chk) {
          $scope.changeAttend(index);
          promises.push(index);
        }
      });
      $q.all(promises).then(function(result) {
        deferred.resolve(result);
        return returns;
      });
      return deferred.promise;
    };
    selected().then(function(response) {
      $scope.enableGuide();
    });
  };
  validStock = function() {
    var defer, promises;
    defer = $q.defer();
    promises = [];
    angular.forEach(angular.element("[name=chk]"), function(el) {
      if (angular.element(el).is(":checked")) {
        promises.push({
          materials: el.attributes["data-materials"].value,
          name: el.attributes["data-mname"].value,
          brand: el.attributes["data-brand"].value,
          model: el.attributes["data-model"].value,
          nbrand: el.attributes["data-nbrand"].value,
          nmodel: el.attributes["data-nmodel"].value,
          quantity: el.attributes['data-quantity'].value
        });
      }
    });
    $q.all(promises).then(function(response) {
      defer.resolve(response);
    });
    return defer.promise;
  };
  $scope.getStock = function() {
    validStock().then(function(result) {
      $scope.cstock = result;
      $scope.dguide = new Array();
      $scope.stock();
    });
  };
  $scope.stock = function() {
    var deferred, nextStep;
    deferred = $q.defer();
    nextStep = function() {
      var prm;
      if ($scope.cstock.length > 0) {
        prm = $scope.cstock[0];
        prm['gstock'] = true;
        attendFactory.getStockItem(prm).success(function(response) {
          if (response.status) {
            $scope.stks = new Array();
            $scope.istock = response.stock;
            $scope.qmax = parseFloat(prm.quantity);
            $scope.gbrand = prm.brand;
            $scope.gmodel = prm.model;
            $scope.gmaterials = prm.materials;
            $scope.gname = prm.name;
            $scope.gnbrand = prm.nbrand;
            $scope.gnmodel = prm.nmodel;
            angular.element("#sd").text(prm.name + " " + prm.nbrand + " " + prm.nmodel);
            $scope.dstock = {
              'materials': prm.materials,
              'brand': prm.brand,
              'model': prm.model
            };
            angular.element("#mstock").openModal({
              dismissible: false
            });
            console.info(prm);
            $scope.cstock.splice(0, 1);
            console.log($scope.cstock);
            deferred.resolve(false);
          } else {
            console.log(response.raise);
            deferred.resolve(false);
          }
        });
      } else {
        deferred.resolve(true);
      }
    };
    nextStep();
    return deferred.promise;
  };
  $scope.showNip = function(indexsnip) {
    var consulting, verify;
    consulting = function() {
      var deferred, promises;
      deferred = $q.defer();
      promises = new Array();
      angular.forEach($scope.dnip, function(obj, index) {
        var brand, mat, model;
        mat = $scope.gmaterials === obj.materials;
        brand = $scope.gbrand === obj.brand;
        model = $scope.gmodel === obj.model;
        if (mat && brand && model) {
          promises.push(obj);
        }
      });
      $q.all(promises).then(function(response) {
        deferred.resolve(response);
      });
      return deferred.promise;
    };
    verify = function() {
      var defer, ver;
      defer = $q.defer();
      ver = false;
      console.error($scope.nipdetails);
      angular.forEach($scope.nipdetails, function(obj, index) {
        var brand, mat, model, ref;
        console.warn(obj);
        mat = $scope.gmaterials === obj.materials;
        brand = $scope.gbrand === obj.brand;
        model = $scope.gmodel === obj.model;
        console.info(mat, brand, model);
        if (mat && brand && model) {
          ver = (ref = obj.details.length > 0) != null ? ref : {
            "true": false
          };
        }
        defer.resolve(ver);
      });
      defer.resolve(ver);
      return defer.promise;
    };
    verify().then(function(response) {
      $scope.indexshownip = indexsnip;
      if (response === true) {
        return angular.forEach($scope.nipdetails, function(obj, index) {
          var brand, mat, model;
          mat = $scope.gmaterials === obj.materials;
          brand = $scope.gbrand === obj.brand;
          model = $scope.gmodel === obj.model;
          if (mat && brand && model) {
            $scope.snip = obj.details;
            angular.element("#snip").openModal({
              dismissible: false
            });
          }
        });
      } else {
        consulting().then(function(result) {
          if (result.length > 0) {
            $scope.snip = result;
            angular.element("#snip").openModal({
              dismissible: false
            });
          }
        });
      }
    });
  };
  $scope.validSelectStock = function() {
    var amount, tmp;
    tmp = new Array();
    amount = 0;
    angular.forEach($scope.stks, function(obj, index) {
      amount += obj['quantity'];
    });
    if (amount > $scope.qmax) {
      Materialize.toast("<i class='fa fa-times fa-3x red-text'></i>&nbsp;Cantidad mayor a la requerida.", 6000);
    } else if (amount <= 0) {
      Materialize.toast("<i class='fa fa-times fa-3x red-text'></i>&nbsp;Cantidad menor que 0.", 6000);
    } else {
      $scope.dguide.push({
        'materials': $scope.gmaterials,
        'brand': $scope.gbrand,
        'model': $scope.gmodel,
        'name': $scope.gname,
        'nbrand': $scope.gnbrand,
        'nmodel': $scope.gnmodel,
        'amount': amount,
        'details': new Array()
      });
      angular.forEach($scope.dguide, function(obj, index) {
        var b, m, o;
        m = obj.materials === $scope.gmaterials;
        b = obj.brand === $scope.gbrand;
        o = obj.model === $scope.gmodel;
        if (m && b && o) {
          angular.forEach($scope.stks, function(stk, i) {
            if (stk.chk === true) {
              obj.details.push({
                'materials': $scope.gmaterials,
                'brand': stk.brand,
                'model': stk.model,
                'quantity': stk.quantity
              });
            }
          });
        }
      });
      angular.forEach($scope.fchk, function(obj, index) {
        var b, m, o;
        m = obj.materials === $scope.gmaterials;
        b = obj.brand === $scope.gbrand;
        o = obj.model === $scope.gmodel;
        if (m && b && o) {
          $scope.fchk[index].quantity = amount;
        }
      });
      console.info("Nothing generate guide");
      $scope.stock().then(function(result) {
        if (result) {
          $scope.enableGuide();
          angular.element("#mstock").closeModal();
          Materialize.toast("Completo!", 3000);
        } else {
          console.log("Falta");
        }
      });
    }
  };
  $scope.enableGuide = function() {
    var sd;
    sd = function() {
      var count, defered, promises;
      defered = $q.defer();
      promises = new Array();
      count = 0;
      angular.forEach($scope.dguide, function(obj) {
        if (obj.amount > 0) {
          count++;
          promises.push(count);
        }
      });
      $q.all(promises).then(function(response) {
        defered.resolve(response.length);
      });
      return defered.promise;
    };
    sd().then(function(result) {
      if (result > 0) {
        $scope.vstock = true;
      } else {
        $scope.vstock = false;
      }
    });
  };
  $scope.verifyNip = function() {
    var brand, defer, key, mat, model, obj, promises, ref, ver;
    console.log("star verify");
    defer = $q.defer();
    promises = new Array();
    ref = $scope.nipdetails;
    for (key in ref) {
      obj = ref[key];
      console.log("check nip obj", key);
      console.log(obj);
      ver = -1;
      mat = $scope.gmaterials === obj.materials;
      brand = $scope.gbrand === obj.brand;
      model = $scope.gmodel === obj.model;
      if (mat && brand && model) {
        ver = parseInt(key);
        promises.push(ver);
      } else {
        promises.push(ver);
      }
    }
    $q.all(promises).then(function(response) {
      var count;
      console.info(response);
      count = Array.from(new Set(response));
      if (count.length >= 1) {
        if (count[0] !== -1) {
          defer.resolve(count[0]);
        } else {
          defer.resolve(count[1]);
        }
      } else {
        defer.resolve(-1);
      }
    });
    return defer.promise;
  };
  $scope.selectNip = function() {
    $scope.verifyNip().then(function(response) {
      var amount, i, ref, x;
      console.warn(response);
      amount = 0;
      ref = $scope.snip;
      for (i in ref) {
        x = ref[i];
        amount += (x.meter * x.guide) / 100;
      }
      $scope.stks[$scope.indexshownip].quantity = amount;
      if (response >= 0) {
        $scope.nipdetails[response].details = $scope.snip;
        $scope.snip = new Array();
        angular.element("#snip").closeModal();
      } else {
        $scope.nipdetails.push({
          'materials': $scope.gmaterials,
          'brand': $scope.gbrand,
          'model': $scope.gmodel,
          'details': $scope.snip
        });
        $scope.snip = new Array();
        angular.element("#snip").closeModal();
      }
    });
  };
  $scope.setZeroNip = function() {
    var amount, i, ref, x;
    amount = 0;
    ref = $scope.snip;
    for (i in ref) {
      x = ref[i];
      x.guide = 0;
      x.status = false;
    }
    $scope.stks[$scope.indexshownip].quantity = amount;
    angular.element("#snip").closeModal();
    $scope.snip = new Array();
  };
  $scope.SetSezoItemSelected = function() {
    var brand, el, k, mat, model, o, ref;
    ref = $scope.dorders;
    for (k in ref) {
      o = ref[k];
      console.warn(o);
      console.info("INDEX OBJECT ", k);
      mat = $scope.gmaterials === o.fields.materiales.pk;
      brand = $scope.gbrand === o.fields.brand.pk;
      model = $scope.gmodel === o.fields.model.pk;
      if (mat && brand && model) {
        console.log("change zero", k);
        el = angular.element("#chk" + $scope.gmaterials + $scope.gbrand + $scope.gmodel);
        el[0].checked = false;
        $scope.fchk[k].status = false;
        $scope.changeAttend(k);
        $scope.stock().then(function(result) {
          if (result) {
            $scope.enableGuide();
            angular.element("#mstock").closeModal();
            Materialize.toast("Completo!", 3000);
          } else {
            console.log("Falta");
          }
        });
      }
    }
  };
  $scope.selectOrderNip = function(idx) {
    if (idx == null) {
      idx = -1;
    }
    if (idx === -1) {
      angular.forEach($scope.snip, function(obj, index) {
        obj.status = $scope.ns;
        if (!obj.status) {
          $scope.snip[index].guide = 0;
        }
      });
    }
    if (idx >= 0) {
      if (!$scope.snip[idx].status) {
        $scope.snip[idx].guide = 0;
      }
    }
  };
  $scope.validNroGuide = function() {
    var prms;
    if ($scope.guide.nro === null) {
      return;
    }
    if ($scope.guide.nro.match("[0-9]{3}\-[0-9]{1, 8}")) {
      prms = {
        'validNumber': true,
        'guia': $scope.guide.nro
      };
      attendFactory.valNGuide(prms).success(function(response) {
        if (response.status) {
          $scope.ngvalid = true;
        } else {
          Materialize.toast("<span>Nro de Guia Invalido!<br>" + response.raise + "</span>", 2000);
        }
      });
    } else {
      Materialize.toast("Nro de Guia Invalido!", 3600);
    }
  };
  return $scope.test = function() {
    console.log($scope.snip, $scope.nipdetails);
    console.info($scope.dguide);
  };
};

app.controller('attendCtrl', controllers);
