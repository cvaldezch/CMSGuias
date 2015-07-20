var addTmpQuote, changeRadio, deleteAll, deleteMaterial, editMaterial, finishTmp, listTmpQuote, loadStore, loadSupplier, loadText, newQuote, saveQuote, showEdit, showMaterials, stepSecond, uploadReadFile;

$(document).ready(function() {
  $(".panel-add,input[name=read],.step-second").hide();
  $("input[name=description]").on("keyup", keyDescription);
  $("input[name=description]").on("keypress", keyUpDescription);
  $("select[name=meter]").on("click", getSummaryMaterials);
  $("input[name=code]").on("keypress", keyCode);
  $("input[name=traslado]").datepicker({
    minDate: "0",
    showAnim: "slide",
    dateFormat: "yy-mm-dd"
  });
  $(".btn-search").on("click", searchMaterial);
  $(".btn-list").on("click", listTmpQuote);
  $(".btn-add").on("click", addTmpQuote);
  $(document).on("click", "[name=btn-edit]", showEdit);
  $("button[name=esave]").on("click", editMaterial);
  $(document).on("click", "[name=btn-del]", deleteMaterial);
  $(".btn-show-materials").on("click", showMaterials);
  $(".btn-trash").on("click", deleteAll);
  $(".btn-read").on("click", function() {
    return $(".mfile").modal("show");
  });
  $(".show-input-file-temp").click(function() {
    return $("input[name=read]").click();
  });
  $("[name=btn-upload]").on("click", uploadReadFile);
  $(".btn-quote").on("click", stepSecond);
  $(".get-supplier").on("click", loadSupplier);
  $(".get-store").on("click", loadStore);
  $("textarea[name=obser]").on("focus", loadText);
  $("[name=select]").on("change", changeRadio);
  $(".btn-quotesupplier").on("click", saveQuote);
  $(".btn-newquote").on("click", newQuote);
  $(".btn-finish").on("click", finishTmp);
  $("table.table-list").floatThead({
    useAbsolutePositioning: false,
    scrollingTop: 50
  });
  listTmpQuote();
  $("[name=multiple]").checkboxpicker();
});

showMaterials = function(event) {
  var item;
  item = this;
  $(".panel-add").toggle(function() {
    if ($(this).is(":hidden")) {
      $(item).find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
    } else {
      $(item).find("span").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
    }
    return $("table.table-list").floatThead("reflow");
  });
};


/*keyDescription = (event) ->
    key = `window.Event ? event.keyCode : event.which`
    if key isnt 13 and key isnt 40 and key isnt 38 and key isnt 39 and key isnt 37
        getDescription @value.toLowerCase()
    if key is 40 or key is 38 or key is 39 or key is 37
        moveTopBottom key
    return

keyCode = (event) ->
    key = if window.Event then event.keyCode else event.which
    if key is 13
        searchMaterialCode @value

searchMaterial = (event) ->
    desc = $("input[name=description]").val()
    code = $("input[name=code]").val()
    if code.length is 15
        searchMaterialCode code
    else
        getDescription $.trim(desc).toLowerCase()
 */

addTmpQuote = function(event) {
  var code, data, quantity;
  data = new Object();
  code = $(".id-mat").html();
  quantity = $("input[name=cantidad]").val();
  if (code !== "") {
    if (quantity !== "") {
      data.materiales = code;
      data.cantidad = quantity;
      data.brand = $("select#brand").val();
      data.model = $("select#model").val();
      data.type = "add";
      data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
      $.post("", data, function(response) {
        if (response.status) {
          return listTmpQuote();
        } else {
          return $().toastmessage("showWarningToast", "El servidor no a podido agregar el material. " + response.raise);
        }
      }, "json");
    } else {
      $().toastmessage("showWarningToast", "Agregar materiales Falló. Cantidad Null.");
    }
    return;
  } else {
    $().toastmessage("showWarningToast", "Agregar materiales Falló. Código Null.");
  }
};

listTmpQuote = function(event) {
  $.getJSON("", {
    "type": "list"
  }, function(response) {
    var $tb, template, x;
    if (response.status) {
      template = "<tr name=\"{{ id }}\"> <td>{{ item }}</td> <td>{{ materials_id }}</td> <td>{{ matname }}</td> <td>{{ matmeasure }}</td> <td>{{ unit }}</td> <td>{{ brand }}</td> <td>{{ model }}</td> <td>{{ quantity }}</td> <td> <button class=\"btn btn-xs btn-link\" name=\"btn-edit\" value=\"{{ quantity }}\" data-id=\"{{ id }}\" data-mat=\"{{ materials_id }}\" data-brand=\"{{ brand_id }}\" data-model=\"{{ model_id }}\"> <span class=\"glyphicon glyphicon-pencil\"></span> </button> </td> <td> <button class=\"btn btn-xs btn-link text-red\" name=\"btn-del\" value=\"{{ id }}\" data-mat=\"{{ materials_id }}\"> <span class=\"glyphicon glyphicon-trash\"></span> </button> </td> </tr>";
      $tb = $("table.table-list > tbody");
      $tb.empty();
      for (x in response.list) {
        response.list[x].item = parseInt(x) + 1;
        $tb.append(Mustache.render(template, response.list[x]));
      }
    } else {
      return $().toastmessage("showWarningToast", "No se a encontrado resultados. " + response.raise);
    }
  });
};

showEdit = function(event) {
  event.preventDefault();
  $("input[name=ematid]").val(this.getAttribute("data-mat"));
  $("input[name=eidtmp]").val(this.getAttribute("data-id"));
  $("input[name=equantity]").val(this.value);
  setDataBrand("select[name=ebrand]", this.getAttribute("data-brand"));
  setDataModel("select[name=emodel]", this.getAttribute("data-model"));
  $("div.medit").modal("show");
};

editMaterial = function(event) {
  var $id, $mat, $quantity, data;
  event.preventDefault();
  $id = $("input[name=eidtmp]");
  $mat = $("input[name=ematid]");
  $quantity = $("input[name=equantity]");
  if ($quantity.val() !== 0 && $quantity.val() > 0) {
    data = new Object();
    data.id = $id.val();
    data.materials_id = $mat.val();
    data.quantity = $quantity.val();
    data.brand = $("select[name=ebrand]").val();
    data.model = $("select[name=emodel]").val();
    data.type = "edit";
    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
    $.post("", data, function(response) {
      if (response.status) {

        /*$edit = $("table.table-list > tbody > tr[name=#{$id.val()}] > td")
        $edit.eq(5).html($quantity.val())
        $edit.eq(6).find("button").val($quantity.val())
        $("input[name=ematid]").val ""
        $("input[name=eidtmp]").val ""
        $("input[name=equantity]").val ""
         */
        listTmpQuote();
        $(".medit").modal("hide");
      } else {
        return $().toastmessage("showWarningToast", "No se a podido editar el material " + response.raise);
      }
    });
    return;
  } else {
    $().toastmessage("showWarningToast", "Error campo cantidad");
  }
};

deleteMaterial = function(event) {
  var item;
  event.preventDefault();
  item = this;
  return $().toastmessage("showToast", {
    sticky: true,
    text: "Desea eliminar el material " + ($(this).attr("data-mat")),
    type: "confirm",
    buttons: [
      {
        value: "Si"
      }, {
        value: "No"
      }
    ],
    success: function(result) {
      var data;
      if (result === "Si") {
        data = new Object();
        data.id = item.value;
        data.materials_id = $(item).attr("data-mat");
        data.type = "del";
        data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
        $.post("", data, function(response) {
          if (response.status) {
            return $("table.table-list > tbody > tr[name=" + item.value + "]").remove();
          } else {
            return $().toastmessage("showWarningToast", "Error al eliminar material " + response.raise);
          }
        }, "json");
      }
    }
  });
};

deleteAll = function(event) {
  event.preventDefault();
  $().toastmessage("showToast", {
    sticky: true,
    text: "Desea eliminar todo el temporal?",
    type: "confirm",
    buttons: [
      {
        value: "Si"
      }, {
        value: "No"
      }
    ],
    success: function(result) {
      if (result === "Si") {
        $.post("", {
          type: "delall",
          "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
        }, function(response) {
          if (response.status) {
            $().toastmessage("showNoticeToast", "Correcto se a eliminado todo el temporal.");
            return setTimeout(function() {
              return location.reload();
            }, 2600);
          } else {
            return $().toastmessage("showWarningToast", "No se a podido eliminar todo el temporal. " + response.raise);
          }
        }, "json");
      }
    }
  });
};

uploadReadFile = function(event) {
  var btn, data, file, inputfile;
  event.preventDefault();
  btn = this;
  inputfile = document.getElementsByName("read");
  file = inputfile[0].files[0];
  if (file != null) {
    data = new FormData();
    data.append("type", "read");
    data.append("archivo", file);
    data.append("csrfmiddlewaretoken", $("[name=csrfmiddlewaretoken]").val());
    $.ajax({
      url: "",
      type: "POST",
      data: data,
      contentType: false,
      processData: false,
      cache: false,
      beforeSend: function() {
        return $(btn).button("loading");
      },
      success: function(response) {
        var $tb, template, x;
        if (response.status) {
          listTmpQuote();
          $(btn).button("reset");
          if (response.list.length > 0) {
            template = "<tr><td>{{ item }}</td><td>{{ name }}</td><td>{{ measure }}</td><td>{{ unit }}</td><td>{{ quantity }}</td></tr>";
            $tb = $("table.table-nothing > tbody");
            $tb.empty();
            for (x in response.list) {
              response.list[x].item = parseInt(x) + 1;
              $tb.append(Mustache.render(template, response.list[x]));
            }
            $(".mlist").modal("show");
          }
          $(".mfile").modal("hide");
        } else {
          return $().toastmessage("showWarningToast", "No se ha podido completar la transacción. " + response.raise);
        }
      }
    });
  } else {
    $().toastmessage("showWarningToast", "Seleccione un archivo para subir y ser leido.");
  }
};

stepSecond = function() {
  $.getJSON("", {
    "type": "list"
  }, function(response) {
    var $tb, template, x;
    if (response.status) {
      template = "<tr name=\"{{ id }}\"> <td> <input type=\"checkbox\" name=\"chk\" value=\"{{ id }}\" data-materials=\"{{ materials_id }}\" data-brand=\"{{ brand }}\" data-model=\"{{ model }}\" data-quantity=\"{{ quantity }}\"> </td> <td>{{ item }}</td> <td>{{ materials_id }}</td> <td>{{ matname }}</td> <td>{{ matmeasure }}</td> <td>{{ unit }}</td> <td>{{ brand }}</td> <td>{{ model }}</td> <td class=\"text-right\">{{ quantity }}</td> </tr>";
      $tb = $("table.table-quote > tbody");
      $tb.empty();
      for (x in response.list) {
        response.list[x].item = parseInt(x) + 1;
        $tb.append(Mustache.render(template, response.list[x]));
      }
    } else {
      $().toastmessage("showWarningToast", "No se a encontrado resultados. " + response.raise);
    }
  });
  loadSupplier();
  loadStore();
  $(".step-first").hide("blind", 600);
  $(".step-second").show("blind", 400);
};

loadSupplier = function() {
  return $.getJSON("/json/supplier/get/list/all/", function(response) {
    var $sel, template, x;
    if (response.status) {
      template = "<option value=\"{{ supplier_id }}\">{{ company }}</option>";
      $sel = $("select#proveedor");
      $sel.empty();
      for (x in response.supplier) {
        $sel.append(Mustache.render(template, response.supplier[x]));
      }
      return;
    }
  });
};

loadStore = function() {
  return $.getJSON("/json/store/get/list/all/", function(response) {
    var $sel, template, x;
    if (response.status) {
      template = "<option value=\"{{ store_id }}\">{{ name }}</option>";
      $sel = $("select#almacen");
      $sel.empty();
      for (x in response.store) {
        $sel.append(Mustache.render(template, response.store[x]));
      }
      return;
    }
  });
};

loadText = function() {
  tinymce.init({
    selector: "textarea[name=obser]",
    theme: "modern",
    menubar: false,
    statusbar: false,
    toolbar_items_size: "small",
    schema: "html5",
    toolbar: "undo redo | styleselect | bold italic"
  });
};

changeRadio = function(event) {
  $("input[name=select]").each(function() {
    var radio;
    radio = Boolean(parseInt(this.value));
    if (this.checked) {
      $("[name=chk]").each(function() {
        this.checked = radio;
      });
    }
  });
};

saveQuote = function(event) {
  var check, data, mats, obser, store, supplier, transfer;
  check = $("input[name=multiple]");
  supplier = $("select[name=proveedor]");
  store = $("select[name=almacen]");
  transfer = $("input[name=traslado]");
  obser = $("#obser_ifr").contents().find("body").html();
  data = new Object();
  mats = new Array();
  if (supplier.val() !== "" && store.val() !== "" && transfer.val() !== "") {
    if (check.is(":checked")) {
      console.log("check");
      data.proveedor = supplier.val();
      data.quote = check.val();
      data.check = "old";
    } else {
      console.log("not checked");
      data.proveedor = supplier.val();
      data.almacen = store.val();
      data.traslado = transfer.val();
      data.obser = obser;
      data.check = "new";
    }
    data.type = "addQuote";
    data.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
    $("[name=chk]").each(function() {
      if (this.checked) {
        mats.push({
          "materials_id": this.getAttribute("data-materials"),
          "brand": this.getAttribute("data-brand"),
          "model": this.getAttribute("data-model"),
          "quantity": this.getAttribute("data-quantity")
        });
      }
    });
    data.details = JSON.stringify(mats);
    if (mats.length <= 0) {
      $().toastmessage("showWarningToast", "Formato incorrecto, Materiales no seleccionados.");
      return false;
    }
    $.post("", data, function(response) {
      if (response.status) {
        $().toastmessage("showNoticeToast", "Cotización generada " + response.quote);
        check.val(response.quote);
        return newQuote(event);
      } else {
        return $().toastmessage("showWarningToast", "Guardar Cotización fallo. " + response.raise);
      }
    }, "json");
    console.log(data);
    return;
  } else {
    $().toastmessage("showWarningToast", "Formato incorrecto, Campos vacios.");
  }
};

newQuote = function(event) {
  var span, value;
  event.preventDefault();
  span = $(".btn-newquote").find("span");
  if (span.eq(1).html() === "Nuevo") {
    value = false;
    span.eq(0).removeClass("glyphicon-file").addClass("glyphicon-remove");
    span.eq(1).html("Cancelar");
  } else {
    value = true;
    span.eq(0).removeClass("glyphicon-remove").addClass("glyphicon-file");
    span.eq(1).html("Nuevo");
  }
  $(".form-quote").find("select, input, button").each(function() {
    this.disabled = value;
  });
  $(".btn-quotesupplier").attr("disabled", value);
};

finishTmp = function(event) {
  event.preventDefault();
  $().toastmessage("showToast", {
    sticky: true,
    text: "Desea Terminar con el temporal de la Cotización?",
    type: "confirm",
    buttons: [
      {
        value: "Si"
      }, {
        value: "No"
      }
    ],
    success: function(result) {
      if (result === "Si") {
        $.post("", {
          type: "delall",
          "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
        }, function(response) {
          if (response.status) {
            $().toastmessage("showNoticeToast", "Felicidades, la(s) cotizacion(es) se han generado.");
            return setTimeout(function() {
              return location.reload();
            }, 2600);
          } else {
            return $().toastmessage("showWarningToast", "No se a ponido finalizar el temportal. " + response.raise);
          }
        }, "json");
      }
    }
  });
};
