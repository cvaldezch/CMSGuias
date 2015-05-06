var addManPower, addMaterials, calcPartitalMaterial, delManPower, delManPowerAll, delMaterials, delMaterialsAll, editManPower, editMaterials, getListMaterials, getManPowerAll, getMaterialsAll, getmeasure, getsummary, listManPower, openNewMaterial, refreshManPower, refreshMaterials, showAddManPower, showAddMaterial, showEditManPower, showEditMaterials;

$(document).ready(function() {
  getMaterialsAll();
  getManPowerAll();
  $(".materialsadd, .addmanpower").hide();
  $("[name=materials], [name=measure], [name=manpower]").chosen({
    width: "100%"
  });
  $("[name=materials]").on("change", getmeasure);
  $("[name=measure]").on("change", getsummary);
  $(".bshowaddmat").on("click", showAddMaterial);
  $(".bmrefresh").on("click", refreshMaterials);
  $(".btnaddmat").on("click", addMaterials);
  $(document).on("dblclick", ".editm", showEditMaterials);
  $(document).on("click", ".btn-edit-materials", editMaterials);
  $(document).on("change", ".edit-tmp-quantity, .edit-tmp-price", calcPartitalMaterial);
  $(document).on("click", ".btn-del-materials", delMaterials);
  $(".bdelmatall").on("click", delMaterialsAll);
  $(".bshownewmat").on("click", openNewMaterial);
  $(".bshowaddmp").on("click", showAddManPower);
  $(".btnaddmp").on("click", addManPower);
  $(".bmprefresh").on("click", refreshManPower);
  $(".bdelmp").on("click", delManPowerAll);
  $(document).on("dblclick", ".editmp", showEditManPower);
  $(document).on("click", ".btn-edit-mp", editManPower);
  $(document).on("click", ".btn-del-mp", delManPower);
});

getMaterialsAll = function(event) {
  var context;
  context = new Object();
  context.searchName = true;
  context.name = '';
  $.getJSON("/materials/", context, function(response) {
    var $op, template;
    if (response.status) {
      $op = $("[name=materials]");
      $op.empty();
      template = "{{#names}}<option value=\"{{ name }}\">{{ name }}</option>{{/names}}";
      $op.html(Mustache.render(template, response));
      $op.trigger("chosen:updated");
      return getmeasure();
    }
  });
};

getmeasure = function(event) {
  var context;
  context = new Object;
  context.searchMeter = true;
  context.name = $("[name=materials]").val();
  $.getJSON("/materials/", context, function(response) {
    var $se, template;
    if (response.status) {
      $se = $("[name=measure]");
      $se.empty();
      $se.append("<option></option>");
      template = "{{#meter}} <option value=\"{{code}}\">{{measure}}</option> {{/meter}}";
      $se.html(Mustache.render(template, response));
      $se.trigger("chosen:updated");
      setTimeout(function() {
        getsummary();
      }, 200);
    }
  });
};

getsummary = function(event) {
  var context;
  context = new Object;
  context.scode = $("[name=measure]").val();
  context.summary = true;
  if (context.scode.length === 15) {
    $.getJSON("/materials/", context, function(response) {
      var $s, template;
      if (response.status) {
        template = "<table class=\"table table-condensed font-11\"><tbody><tr><th>Código</th><td class=\"matid\">{{ summary.materials }}</td></tr><tr><th>Nombre</th><td>{{ summary.name }}</td></tr><tr><th>Media</th><td>{{ summary.measure }}</td></tr><tr><th>Unidad</th><td>{{ summary.unit }}</td></tr></tbody></table>";
        $s = $("[name=summary]");
        $s.empty();
        $s.html(Mustache.render(template, response));
        $("[name=mprice]").val(response.summary.price);
      }
    });
  } else {
    $().toastmessage("showWarningToast", "El código del material no es valido.");
  }
};

showAddMaterial = function(event) {
  if ($(".materialsadd").is(":visible")) {
    $(this).removeClass("btn-warning").addClass("btn-default");
    $(".materialsadd").hide(800);
  } else {
    $(this).removeClass("btn-default").addClass("btn-warning");
    $(".materialsadd").show(800);
  }
};

addMaterials = function(event) {
  var context;
  context = new Object();
  context.materials = $(".matid").text();
  context.quantity = $("[name=mquantity]").val();
  context.price = $("[name=mprice]").val();
  if (context.materials.length === 15) {
    if (context.quantity !== "") {
      if (context.price !== "") {
        context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
        context.addMaterials = true;
        $.post("", context, function(response) {
          if (response.status) {
            getListMaterials();
          } else {
            $().toastmessage("showErrorToast", "Error al guardar los cambios. " + response.raise);
          }
        }, "json");
      } else {
        $().toastmessage("showWarningToast", "Precio invalido.");
      }
    } else {
      $().toastmessage("showWarningToast", "Cantidad invalida.");
    }
  } else {
    $().toastmessage("showWarningToast", "Código de material incorrecto.");
  }
};

getListMaterials = function(event) {
  var context;
  context = new Object;
  context.listMaterials = true;
  $.getJSON("", context, function(response) {
    var $tbl, counter, template;
    if (response.status) {
      $tbl = $(".tmaterials tbody");
      $tbl.empty();
      template = "{{#materials}}<tr data-edit=\"{{pk}}\"><td>{{index}}</td><td>{{code}}</td><td>{{name}}</td><td>{{unit}}</td><td>{{quantity}}</td><td>{{price}}</td><td>{{partial}}</td><td class=\"text-center\"><button class=\"btn btn-warning btn-xs btn-edit-materials\" value=\"{{ pk }}\" data-materials=\"{{ code }}\" disabled><span class=\"fa fa-edit\"></span></button></td><td class=\"text-center\"><button class=\"btn btn-danger btn-xs btn-del-materials\" value=\"{{ pk }}\" data-materials=\"{{ code }}\"><span class=\"fa fa-trash\"></span></button></td></tr>{{/materials}}";
      counter = 1;
      response.index = function() {
        return counter++;
      };
      $tbl.html(Mustache.render(template, response));
    } else {
      $().toastmessage("showErrorToast", "Error al Obtener la lista. " + response.raise + ".");
    }
  });
};

refreshMaterials = function(event) {
  getMaterialsAll();
  getListMaterials();
};

openNewMaterial = function() {
  var interval, win;
  win = window.open("/materials/", "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600");
  interval = window.setInterval(function() {
    if (win === null || win.closed) {
      window.clearInterval(interval);
      getMaterialsAll;
    }
  }, 1000);
  return win;
};

showEditMaterials = function(event) {
  var $td, $tr, price, quantity;
  if ($(".edit-tmp-quantity").length) {
    $(".edit-tmp-quantity").parent("td").html($(".edit-tmp-quantity").val());
  }
  if ($(".edit-tmp-price").length) {
    $(".edit-tmp-price").parent("td").html($(".edit-tmp-price").val());
  }
  $tr = $(this);
  $td = $tr.find("td");
  quantity = $td.eq(4).text();
  $(".btn-edit-materials").attr("disabled", true);
  $td.eq(7).find("button").attr("disabled", false);

  /*if quantity.indexOf "," then quantity=  quantity.replace ",", "."
  quantity = parseFloat quantity
   */
  price = $td.eq(5).text();
  $td.eq(4).html("<input type=\"text\" value=\"" + quantity + "\" class=\"form-control input-sm col-2 edit-tmp-quantity\">");
  $td.eq(5).html("<input type=\"text\" value=\"" + price + "\" class=\"form-control input-sm col-2 edit-tmp-price\">");
};

editMaterials = function(event) {
  var context, e;
  context = new Object;
  context.quantity = $(".edit-tmp-quantity").val();
  context.price = $(".edit-tmp-price").val();
  context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
  try {
    if (!context.quantity.match(/^[+]?[0-9]+[\.[0-9]+]?/)) {
      $().toastmessage("showWarningToast", "No se a ingreso un número, cantidad incorrecta.");
      return false;
    }
    if (!context.price.match(/^[+]?[0-9]+[\.[0-9]+]?/)) {
      $().toastmessage("showWarningToast", "No se a ingreso un número, precio incorrecto.");
      return false;
    }
    context.editMaterials = true;
    context.materials = this.getAttribute("data-materials");
    context.id = this.value;
    $.post("", context, function(response) {
      if (response.status) {
        $(".edit-tmp-quantity").parent("td").parent("tr").find("td").eq(7).find("button").attr("disabled", true);
        $(".edit-tmp-quantity").parent("td").html($(".edit-tmp-quantity").val());
        $(".edit-tmp-price").parent("td").html($(".edit-tmp-price").val());
      } else {
        $().toastmessage("showErrorToast", "No se a podido editar. " + response.raise + ".");
      }
    }, "json");
  } catch (_error) {
    e = _error;
    $().toastmessage("showWarningToast", "No se habilito la edición.");
  }
};

calcPartitalMaterial = function(event) {
  var $tr, price, quantity;
  $tr = $(this).parent("td").parent("tr");
  quantity = $tr.find("td").eq(4).find("input").val();
  price = $tr.find("td").eq(5).find("input").val();
  if (quantity.indexOf(",") === 1) {
    quantity = quantity.replace(",", ".");
  }
  if (price.indexOf(",") === 1) {
    price = price.replace(",", ".");
  }
  quantity = parseFloat(quantity);
  price = parseFloat(price);
  $tr.find("td").eq(6).text((quantity * price).toFixed(2));
};

delMaterials = function(event) {
  var btn;
  btn = this;
  $().toastmessage("showToast", {
    text: "Realmente deseas eliminar el material?",
    type: "confirm",
    sticky: true,
    buttons: [
      {
        value: "Si"
      }, {
        value: "No"
      }
    ],
    success: function(result) {
      var context;
      if (result === "Si") {
        context = new Object;
        context.materials = btn.getAttribute("data-materials");
        context.id = btn.value;
        context.delMaterials = true;
        context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
        $.post("", context, function(response) {
          if (response.status) {
            $().toastmessage("showSuccessToast", "Se a eliminado el material.");
            getListMaterials();
          } else {
            $().toastmessage("showErrorToast", "No se a podido eliminar el material. " + response.raise);
          }
        });
      }
    }
  });
};

delMaterialsAll = function(event) {
  $().toastmessage("showToast", {
    text: "Realmente deseas eliminar todo la lista de materiales?",
    type: "confirm",
    sticky: true,
    buttons: [
      {
        value: "Si"
      }, {
        value: "No"
      }
    ],
    success: function(result) {
      var context;
      if (result === "Si") {
        context = new Object;
        context.delMaterialsAll = true;
        context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
        $.post("", context, function(response) {
          if (response.status) {
            $().toastmessage("showSuccessToast", "Se a eliminado el material.");
            getListMaterials();
          } else {
            $().toastmessage("showErrorToast", "No se a podido eliminar el material. " + response.raise);
          }
        });
      }
    }
  });
};

getManPowerAll = function(event) {
  var context;
  context = new Object;
  context.listcbo = true;
  $.getJSON("/manpower/list/cbo/", context, function(response) {
    var $cm, template;
    if (response.status) {
      $cm = $("[name=manpower]");
      $cm.empty();
      template = "{{#list}}<option value=\"{{cargo_id}}\">{{cargos}}</option>{{/list}}";
      $cm.html(Mustache.render(template, response));
      return $cm.trigger("chosen:updated");
    } else {
      $().toastmessage("showErrorToast", "Error al listar combo. " + response.raise);
    }
  });
};

showAddManPower = function(event) {
  if ($(".addmanpower").is(":visible")) {
    $(this).removeClass("btn-warning").addClass("btn-default");
    $(".addmanpower").hide(800);
  } else {
    $(this).removeClass("btn-default").addClass("btn-warning");
    $(".addmanpower").show(800);
  }
};

addManPower = function(event) {
  var context;
  context = new Object;
  context.addMan = true;
  context.performance = $(".performance").text();
  context.manpower = $("[name=manpower]").val();
  context.gang = $("[name=mpgang]").val();
  context.price = $("[name=mpprice]").val();
  if (context.manpower === "") {
    $().toastmessage("showWarningToast", "Codigo para Mano de obra es incorrecto.");
    return false;
  }
  if (!context.gang.match(/^[+]?[0-9]{1,3}[\.[0-9]{0,3}]?/)) {
    $().toastmessage("showWarningToast", "Cuadrilla invalida.");
    return false;
  }
  if (!context.price.match(/^[+]?[0-9]+[\.[0-9]{0,4}]?/)) {
    $().toastmessage("showWarningToast", "El precio ingresado es incorrecto.");
    return false;
  }
  context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
  $.post("", context, function(response) {
    if (response.status) {
      return listManPower();
    } else {
      $().toastmessage("showErrorToast", "Error al agregar mano de poder. " + response.raise);
    }
  }, "json");
};

listManPower = function(event) {
  var context;
  context = new Object;
  context.listManPower = true;
  $.getJSON("", context, function(response) {
    var $tb, counter, template;
    if (response.status) {
      $tb = $(".tmanpower > tbody");
      template = "{{#manpower}}<tr class=\"editmp\"><td>{{index}}</td><td>{{code}}</td><td>{{name}}</td><td>{{unit}}</td><td>{{gang}}</td><td>{{quantity}}</td><td>{{price}}</td><td>{{partial}}</td><td class=\"text-center\"><button class=\"btn btn-xs btn-warning\" value=\"{{ id }}\" data-mp=\"{{code}}\" disabled><span class=\"fa fa-edit\"></span></button></td><td class=\"text-center\"><button class=\"btn btn-danger btn-xs\" value=\"{{ id }}\" data-mp=\"{{code}}\"><span class=\"fa fa-trash\"></span></button></td></tr>{{/manpower}}";
      $tb.empty();
      counter = 1;
      response.index = function() {
        return counter++;
      };
      $tb.html(Mustache.render(template, response));
    } else {
      $().toastmessage("showErrorToast", "No se obtenido resultados. " + response.raise);
    }
  });
};

delManPowerAll = function(event) {
  $().toastmessage("showToast", {
    text: "Realmente desea eliminar todo la lista de Mano de Obra?",
    type: "confirm",
    sticky: true,
    buttons: [
      {
        value: "Si"
      }, {
        value: "No"
      }
    ],
    success: function(result) {
      var context;
      if (result === "Si") {
        context = new Object;
        context.delManPowerAll = true;
        $.post("", context, function(response) {
          if (response.status) {
            listManPower();
          } else {
            $().toastmessage("showErrorToast", "Error al eliminar toda la lista. " + response.raise);
          }
        }, "json");
      }
    }
  });
};

refreshManPower = function(event) {
  getManPowerAll();
  listManPower();
};

showEditManPower = function(event) {
  var $td, $tr, gang, price;
  if ($(".edit-mp-gang").length) {
    $(".edit-mp-gang").parent("td").html($(".edit-mp-gang").val());
  }
  if ($(".edit-mp-price").length) {
    $(".edit-mp-price").parent("td").html($(".edit-mp-price").val());
  }
  $tr = $(this);
  $td = $tr.find("td");
  gang = $td.eq(4).text();
  $td.eq(8).find("button").attr("disabled", false);
  price = $td.eq(6).text();
  $td.eq(4).html("<input type=\"text\" value=\"" + gang + "\" class=\"form-control input-sm col-2 edit-mp-gang\">");
  $td.eq(6).html("<input type=\"text\" value=\"" + price + "\" class=\"form-control input-sm col-2 edit-mp-price\">");
};

editManPower = function(event) {
  var context;
  context = new Object;
  context.addMan = true;
  context.gang = $(".edit-mp-gang").val();
  context.price = $(".edit-mp-price").val();
  context.performance = $(".performance").text();
  context.manpower = this.getAttribute("data-mp");
  if (!context.gang.match(/^[+]?[0-9]{1,3}[\.[0-9]{0,3}]?/)) {
    $().toastmessage("showWarningToast", "Cuadrilla invalida.");
    return false;
  }
  if (!context.price.match(/^[+]?[0-9]+[\.[0-9]{0,4}]?/)) {
    $().toastmessage("showWarningToast", "El precio ingresado es incorrecto.");
    return false;
  }
  context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
  $.post("", context, function(response) {
    if (response.status) {
      listManPower();
    } else {
      $().toastmessage("showErrorToast", "Error al editar los campos. " + response.raise);
    }
  }, "json");
};

delManPower = function(event) {
  var btn;
  btn = this;
  $().toastmessage("showToast", {
    text: "Realmente deseas eliminar la mano de Obra?",
    type: "confirm",
    sticky: true,
    buttons: [
      {
        value: "Si"
      }, {
        value: "No"
      }
    ],
    success: function(result) {
      var context;
      if (result === "Si") {
        context = new Object;
        context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
        context.delMan = true;
        context.manpower = btn.getAttribute("data-mp");
        return $.post("", context, function(response) {
          if (response.status) {
            listManPower();
          } else {
            $().toastmessage("showErrorToast", "Error al eliminar la mano de obra. " + response.raise);
          }
        }, "json");
      }
    }
  });
};
