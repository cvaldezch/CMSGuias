var addTmpPurchase, blurRange, calcTotal, deleteAll, deleteMaterial, editMaterial, listTmpBuy, openBrand, openModel, openUnit, saveComment, saveOrderPurchase, showBedside, showEdit, showMaterials, showObservation, toggleDeposito, uploadReadFile;

$(document).ready(function() {
  $(".panel-add,input[name=read],.step-second").hide();

  /*$("input[name=description]").on "keyup", keyDescription
  $("input[name=description]").on "keypress", keyUpDescription
  $("select[name=meter]").on "click", getSummaryMaterials
  $("input[name=code]").on "keypress", keyCode
   */
  $("input[name=traslado]").datepicker({
    minDate: "0",
    showAnim: "slide",
    dateFormat: "yy-mm-dd"
  });
  $(".btn-show-materials").on("click", showMaterials);
  $(".btn-search").on("click", searchMaterial);
  $(".btn-list").on("click", listTmpBuy);
  $(".btn-add").on("click", addTmpPurchase);
  $(document).on("click", "[name=btn-edit]", showEdit);
  $("button[name=esave]").on("click", editMaterial);
  $(document).on("click", "[name=btn-del]", deleteMaterial);
  $(".btn-trash").on("click", deleteAll);
  $(".btn-read").on("click", function() {
    return $(".mfile").modal("show");
  });
  $(".show-input-file-temp").click(function() {
    return $("input[name=read]").click();
  });
  $("[name=btn-upload]").on("click", uploadReadFile);
  $(".show-bedside").on("click", showBedside);
  $("input[name=discount],input[name=edist]").on("blur", blurRange);
  $(".btn-deposito").on("click", toggleDeposito);
  $(".btn-purchase").on("click", saveOrderPurchase);
  $("input[name=pdiscount]").on("keyup", calcTotal).on("keypress", numberOnly);
  $("[name=selproject]").chosen({
    width: "100%"
  });
  $("#saveComment").on("click", saveComment);
  $(document).on("click", "[name=btn-comment]", showObservation);
  listTmpBuy();
  $.get("/unit/list/?list=true", function(response) {
    var $unit, template;
    if (response.status) {
      template = "{{#lunit}}<option value=\"{{ unidad_id }}\">{{ uninom }}</option>{{/lunit}}";
      $unit = $("select[name=eunit]");
      $unit.empty();
      console.log(response);
      $unit.html(Mustache.render(template, response));
    }
  });
  $("table.table-list").floatThead({
    useAbsolutePositioning: true,
    scrollingTop: 50
  });
  tinymce.init({
    selector: "textarea[name=observation]",
    menubar: false,
    toolbar: "undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify",
    toolbar_items_size: 'small'
  });
});

showMaterials = function(event) {
  var item;
  item = this;
  $(".panel-add").toggle(function() {
    if ($(this).is(":hidden")) {
      return $(item).find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
    } else {
      return $(item).find("span").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
    }
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
    return
 */


/*searchMaterial = (event) ->
    desc = $("input[name=description]").val()
    code = $("input[name=code]").val()
    if code.length is 15
        searchMaterialCode code
    else
        getDescription $.trim(desc).toLowerCase()
 */

addTmpPurchase = function(event) {
  var code, data, discount, price, quantity;
  data = new Object();
  code = $(".id-mat").html();
  quantity = $("input[name=cantidad]").val();
  price = $("input[name=precio]").val();
  discount = parseInt($("input[name=discount]").val());
  if (code !== "") {
    if (quantity !== "") {
      if (price !== "") {
        data.materiales = code;
        data.cantidad = quantity;
        data.precio = price;
        data.brand = $("select[name=brand]").val();
        data.model = $("select[name=model]").val();
        data.unit = $("select[name=unit]").val();
        data.perception = $("[name=perception]").is(":checked") ? 1 : 0;
        data.discount = discount;
        data.type = "add";
        data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
        $.post("", data, function(response) {
          if (response.status) {
            return listTmpBuy();
          } else {
            return $().toastmessage("showWarningToast", "El servidor no a podido agregar el material, " + response.raise + ".");
          }
        }, "json");
      } else {
        $().toastmessage("showWarningToast", "Agregar materiales Falló. Precio Null.");
      }
    } else {
      $().toastmessage("showWarningToast", "Agregar materiales Falló. Cantidad Null.");
    }
    return;
  } else {
    $().toastmessage("showWarningToast", "Agregar materiales Falló. Código Null.");
  }
};

listTmpBuy = function(event) {
  $.getJSON("", {
    "type": "list"
  }, function(response) {
    var $tb, template, x;
    if (response.status) {
      template = "<tr name=\"{{id}}\">\n<td style=\"width: 20px;\" class=\"text-center\">{{item}}</td><td>{{materials_id}}</td>\n<td>{{matname}} - {{matmeasure}}</td>\n<td>{{unit}}</td>\n<td>{{brand}}</td>\n<td>{{model}}</td>\n<td class=\"text-right\">{{quantity}}</td>\n<td class=\"text-right\">{{price}}</td>\n<td class=\"text-right\">{{discount}}%</td>\n<td class=\"text-right\">{{perception}}%</td>\n<td class=\"text-right\">{{amount}}</td>\n<td class=\"text-center\"><button class=\"btn btn-xs btn-link\" name=\"btn-edit\" value=\"{{quantity}}\" data-price=\"{{price}}\" data-brand=\"{{brand}}\" data-model=\"{{model}}\" data-nombre=\"{{matname}} {{matmeasure}}\" data-id=\"{{id}}\" data-mat=\"{{materials_id}}\" data-discount=\"{{discount}}\" data-unit=\"{{unit}}\" data-perception=\"{{perception}}\"><span class=\"glyphicon glyphicon-pencil\"></span></button></td>\n<td class=\"text-center\"><button class=\"btn btn-xs btn-link text-red\" name=\"btn-del\" value=\"{{id}}\" data-mat=\"{{materials_id}}\"><span class=\"glyphicon glyphicon-trash\"></span></button></td>\n<td class=\"text-center\">\n    <button type=\"button\" class=\"btn btn-sm btn-link black-text\" name=\"btn-comment\" value=\"{{id}}\" data-materrials=\"{{materials_id}}\" data-desc=\"{{matname}} - {{matmeasure}}\" data-brand=\"{{brand}}\" data-model=\"{{model}}\" data-unit=\"{{unit}}\" data-obs=\"{{observation}}\">\n        <i class=\"fa fa-font fa-lg text-black\"></i>\n    </button>\n</td>\n</tr>";
      $tb = $("table.table-list > tbody");
      $tb.empty();
      for (x in response.list) {
        response.list[x].item = parseInt(x) + 1;
        $tb.append(Mustache.render(template, response.list[x]));
      }
      $(".discount").html(response.discount.toFixed(2));
      $(".sub").html(response.subtotal.toFixed(2));
      if ($("[name=sigv]").is(":checked")) {
        $(".igv").html(response.igv.toFixed(2));
        $(".total").html(response.total.toFixed(2));
      } else {
        $(".igv").html(0);
        $(".total").html((response.total - response.igv).toFixed(2));
      }
    } else {
      return $().toastmessage("showWarningToast", "No se a encontrado resultados. " + response.raise);
    }
  });
};

showObservation = function() {
  console.log($(this).a);
  $(".odesc").text(($(this).attr("data-desc")) + " " + ($(this).attr("data-brand")) + " " + ($(this).attr("data-model")));
  $("#obs").html("" + ($(this).attr("data-obs")));
  $("#saveComment").val($(this).val());
  $("#mobservation").modal("show");
};

showEdit = function(event) {
  var btn, opb, opm;
  btn = this;
  getDataBrand();
  getDataModel();
  opb = "<option value=\"{{brand_id}}\" {{!se}}>{{ brand }}</option>";
  opm = "<option value=\"{{ model_id }}\" {{!se}}>{{ model }}</option>";
  $("input[name=ematid]").val($(this).attr("data-mat"));
  $("input[name=eidtmp]").val($(this).attr("data-id"));
  $("input[name=equantity]").val(this.value);
  $("input[name=eprice]").val($(this).attr("data-price"));
  $("input[name=edist]").val($(this).attr("data-discount"));
  setTimeout(function() {
    var $bra, $mo, tb, tm, x;
    $bra = $("select[name=ebrand]");
    $bra.empty();
    for (x in globalDataBrand) {
      tb = opb;
      if (globalDataBrand[x].brand === btn.getAttribute("data-brand")) {
        tb = tb.replace("{{!se}}", "selected");
      }
      $bra.append(Mustache.render(tb, globalDataBrand[x]));
    }
    $mo = $("select[name=emodel]");
    $mo.empty();
    for (x in globalDataModel) {
      tm = opm;
      if (globalDataModel[x].model === btn.getAttribute("data-model")) {
        tm = tm.replace("{{!se}}", "selected");
      }
      $mo.append(Mustache.render(tm, globalDataModel[x]));
    }
    $("[name=eunit]").val(btn.getAttribute("data-unit"));
    $("[name=eperception]").prop("checked", Boolean(parseInt(btn.getAttribute("data-perception"))));
    $("#descedit").html(btn.getAttribute("data-nombre"));
    return $(".medit").modal("show");
  }, 1000);
};

editMaterial = function(event) {
  var $discount, $id, $mat, $price, $quantity, data;
  event.preventDefault();
  $id = $("input[name=eidtmp]");
  $mat = $("input[name=ematid]");
  $quantity = $("input[name=equantity]");
  $price = $("input[name=eprice]");
  $discount = $("input[name=edist]").val();
  if ($quantity.val() !== 0 && $quantity.val() > 0 && $price.val() !== 0 && $price.val() > 0) {
    data = new Object();
    data.id = $id.val();
    data.materials_id = $mat.val();
    data.quantity = parseFloat($quantity.val());
    data.price = parseFloat($price.val());
    data.brand = $("select[name=ebrand]").val();
    data.model = $("select[name=emodel]").val();
    data.type = "edit";
    data.unit = $("select[name=eunit]").val();
    data.perception = $("[name=eperception]").is(":checked") ? 1 : 0;
    data.discount = parseFloat($discount);
    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
    $.post("", data, function(response) {
      if (response.status) {

        /*$edit = $("table.table-list > tbody > tr[name=#{$id.val()}] > td")
        $edit.eq(5).html $quantity.val()
        $edit.eq(6).html $price.val()
        $edit.eq(7).html "#{$discount}%"
        $edit.eq(8).html (((data.price * data.discount) / 100) * data.quantity)
        $edit.eq(9).find("button").val $quantity.val()
        $edit.eq(9).find("button").attr "data-price", $price.val()
        $("input[name=ematid],input[name=eidtmp],input[name=equantity],input[name=eprice]").val ""
         */
        $(".medit").modal("hide");
        listTmpBuy();
      } else {
        return $().toastmessage("showWarningToast", "No se a podido editar el material " + response.raise);
      }
    });
    return;
  } else {
    $().toastmessage("showWarningToast", "Error campo vacio: cantidad, precio.  ");
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
          listTmpBuy();
          $(btn).button("reset");
          if (response.list.length > 0) {
            template = "<tr><td>{{ item }}</td><td>{{ name }}</td><td>{{ measure }}</td><td>{{ unit }}</td><td>{{ quantity }}</td><td>{{ price }}</td></tr>";
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

blurRange = function() {
  console.info("value " + this.value);
  console.info("max " + (this.getAttribute("max")));
  if (parseInt(this.value) > parseInt(this.getAttribute("max"))) {
    this.value = parseInt(this.getAttribute("max"));
  } else if (parseInt(this.value) < parseInt(this.getAttribute("min"))) {
    this.value = parseInt(this.getAttribute("min"));
  }
};

toggleDeposito = function() {
  $("input[name=deposito]").click();
};

showBedside = function() {
  var $tb;
  $tb = $("table.table-list > tbody > tr");
  if ($tb.length) {
    $(".mpurchase").modal("toggle");
    calcTotal();
  } else {
    $().toastmessage("showWarningToast", "Debe de ingresar por lo menos un material.");
  }
};

saveOrderPurchase = function() {
  var data, valid;
  valid = false;
  data = new Object();
  $("div.mpurchase > .modal-dialog > .modal-content > .modal-body > .row").find("select,input").each(function(index, elements) {
    if (elements.type === "file" || elements.type === "select" || elements.type === "text") {
      data[elements.name] = elements.value;
      return true;
    }
    if (elements.value !== "") {
      valid = true;
      return data[elements.name] = elements.value;
    } else {
      valid = false;
      data.element = elements.name;
      return valid;
    }
  });
  if (valid) {
    $().toastmessage("showToast", {
      text: "Desea generar la <q>Orden de Compra</q>?",
      type: "confirm",
      sticky: true,
      buttons: [
        {
          value: 'Si'
        }, {
          value: 'No'
        }
      ],
      success: function(result) {
        var discount, prm;
        if (result === "Si") {
          discount = $("input[name=pdiscount]").val();
          if (discount === "") {
            discount = 0;
          }
          prm = new FormData();
          prm.append("proveedor", data.proveedor);
          prm.append("lugent", data.lugent);
          prm.append("documento", data.documento);
          prm.append("pagos", data.pagos);
          prm.append("moneda", data.moneda);
          prm.append("traslado", data.traslado);
          prm.append("contacto", data.contacto);
          prm.append("discount", discount);
          prm.append("sigv", $("[name=sigv]").is(":checked") ? 1 : 0);
          prm.append("projects", $("select[name=selproject]").val().toString());
          prm.append("savePurchase", true);
          prm.append('quotation', $("[name=quotation]").val());
          prm.append('observation', $("#observation_ifr").contents().find('body').html());
          if ($("input[name=deposito]").get(0).files.length) {
            prm.append("deposito", $("input[name=deposito]").get(0).files[1]);
          }
          prm.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());
          $.ajax({
            url: "",
            type: "POST",
            data: prm,
            dataType: "json",
            contentType: false,
            processData: false,
            cache: false,
            success: function(response) {
              if (response.status) {
                $().toastmessage("showNoticeToast", "Correco se a generar <q>Orden de Compra Nro " + response.nro + "</q>");
                setTimeout(function() {
                  return location.reload();
                }, 2600);
              } else {
                $().toastmessage("showWarningToast", "No se a podido generar la <q>Orden de Compra</q>. " + response.raise);
              }
            }
          });
        }
      }
    });
  } else {
    $().toastmessage("showWarningToast", "Alerta!<br>Campo vacio, " + data.element);
  }
};

saveComment = function() {
  var data;
  data = {
    comment: $("#obs").val(),
    saveComment: true,
    id: $(this).val(),
    'csrfmiddlewaretoken': $("[name=csrfmiddlewaretoken]").val()
  };
  $.post("", data, function(response) {
    console.log(response);
    if (response.status) {
      $("#obs").val();
      listTmpBuy();
      $("#mobservation").modal("hide");
    } else {
      $().toastmessage("showWarningToast", "No se a podido guardar los datos temporales. " + response.raise);
    }
  }, "json");
};

calcTotal = function(event) {
  var discount, igv, sub, total;
  sub = convertNumber($(".sub").text());
  igv = convertNumber($(".igv").text());
  igv = (igv * 100) / sub;
  discount = convertNumber($("input[name=pdiscount]").val());
  $("label[name=vamount]").text(sub);
  discount = (sub * discount) / 100;
  $("label[name=vdsct]").text(discount);
  if ($("[name=sigv]").is(":checked")) {
    igv = ((sub - discount) * igv) / 100;
    $("[name=vigv]").val(igv.toFixed(2));
    total = sub - discount + igv;
  } else {
    $("[name=vigv]").val(0);
    total = sub - discount;
  }
  $("label[name=vtotal]").text(total.toFixed(2));
};

openBrand = function() {
  var interval, url, win;
  url = "/brand/new/";
  win = window.open(url, "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600");
  interval = window.setInterval(function() {
    var $brand, template;
    if (win === null || win.closed) {
      window.clearInterval(interval);
      $.getJSON("/json/brand/list/option/", function(response) {});
      if (response.status) {
        template = "{{#brand}}<option value=\"{{ brand_id }}\">{{ brand }}</option>{{/brand}}";
        $brand = $("select[name=ebrand]");
        $brand.empty();
        $brand.html(Mustache.render(template, response));
      }
    }
  }, 1000);
  return win;
};

openModel = function() {
  var interval, url, win;
  url = "/model/new/";
  win = window.open(url, "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600");
  interval = window.setInterval(function() {
    var brand, data;
    if (win === null || win.closed) {
      window.clearInterval(interval);
      brand = $("select[name=brand]").val();
      data = {
        brand: brand
      };
      $.getJSON("/json/model/list/option/", data, function(response) {
        var $model, template;
        if (response.status) {
          template = "{{#model}}<option value=\"{{ model_id }}\">{{ model }}</option>{{/model}}";
          $model = $("select[name=emodel]");
          $model.empty();
          return $model.html(Mustache.render(template, response));
        }
      });
    }
  }, 1000);
  return win;
};

openUnit = function() {
  var interval, url, win;
  url = "/unit/add";
  win = window.open(url, "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600");
  interval = window.setInterval(function() {
    if (win === null || win.closed) {
      window.clearInterval(interval);
      $.get("/unit/list/?list=true", function(response) {
        var $unit, template;
        if (response.status) {
          template = "{{#lunit}}<option value=\"{{ unidad_id }}\">{{ uninom }}</option>{{/lunit}}";
          $unit = $("select[name=unit],select[name=eunit]");
          $unit.empty();
          return $unit.html(Mustache.render(template, response));
        }
      });
    }
  }, 1000);
  return win;
};
