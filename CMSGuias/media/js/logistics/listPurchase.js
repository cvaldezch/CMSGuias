var addNewMaterialPurchase, annularPurchase, calcAmount, changeSearch, changeSelect, deleCheckMaterials, getDataPurchase, getSearch, listDetails, openWindow, saveEditDetailsPurchase, savePurchase, showActions, showChoiceDeposit, showEditDetailsPurchase, showEditPurchasae, showPanelAdd, showStepOne;

$(document).ready(function() {
  $(".step-two, .panel-add").hide();
  $("input[name=star],input[name=end],input[name=transfer]").datepicker({
    dateFormat: "yy-mm-dd",
    showAnim: "slide"
  });
  $("input[name=search]").on("change", changeSearch);
  $(".btn-search").on("click", getSearch);
  $(document).on("click", ".btn-purchase", openWindow);
  $(document).on("click", ".btn-actions", showActions);
  $(".btn-edtp").on("click", showEditPurchasae);
  $(".btn-back").on("click", showStepOne);
  $("input[name=select]").on("change", changeSelect);
  $(".btn-show-add").on("mouseenter mouseleave", animateAdd).on("click", showPanelAdd);
  $("input[name=quantity],input[name=price],input[name=equantity],input[name=eprice],input[name=ediscount]").on("keypress", numberOnly);
  $("button.btn-add").on("click", addNewMaterialPurchase);
  $("button.btn-delete").on("click", deleCheckMaterials);
  $(document).on("click", ".btn-sedit", showEditDetailsPurchase);
  $(".btn-edit-details-purchase").on("click", saveEditDetailsPurchase);
  $("input.edsct").on("keyup", calcAmount);
  $(".btn-show-deposit").on("click", showChoiceDeposit);
  $("button.btn-save-purchase").on("click", savePurchase);
  $("button.btn-delp").on("click", annularPurchase);
  tinymce.init({
    selector: "[name=observation]",
    menubar: false,
    toolbar_items_size: "small"
  });
});

changeSearch = function() {
  if (this.checked) {
    if (this.value === "status") {
      $("input[name=star],input[name=end],input[name=code]").attr("disabled", true);
      $("select[name=status]").attr("disabled", false);
      return;
    } else if (this.value === "dates") {
      $("input[name=star],input[name=end]").attr("disabled", false);
      $("select[name=status],input[name=code]").attr("disabled", true);
      return;
    } else if (this.value === "code") {
      $("input[name=star],input[name=end],select[name=status]").attr("disabled", true);
      $("input[name=code]").attr("disabled", false);
      return;
    }
  }
};

getSearch = function() {
  $("input[name=search]").each(function(index, element) {
    var data, end, start;
    if (element.checked) {
      data = new Object();
      if (element.value === "code") {
        if ($("input[name=code]").val() !== "") {
          data.code = $("input[name=code]").val();
          data.pass = true;
        } else {
          data.pass = false;
          $().toastmessage("showWarningToast", "campo de estado se encuntra vacio.");
        }
      } else if (element.value === "status") {
        if ($("select[name=status]").val() !== "") {
          data.status = $("select[name=status]").val();
          data.pass = true;
        } else {
          data.pass = false;
          $().toastmessage("showWarningToast", "campo de estado se encuntra vacio.");
        }
      } else if (element.value === "dates") {
        start = $("input[name=star]").val();
        if (start !== "") {
          data.dates = true;
          data.start = start;
          data.pass = true;
        } else {
          data.pass = false;
          $().toastmessage("showWarningToast", "campo de fecha inicio se encuntra vacio.");
        }
        end = $("input[name=end]").val();
        if (end !== "") {
          data.end = end;
        }
      }
      console.log(data);
      if (data.pass) {
        $.getJSON("", data, function(response) {
          var $tb, template, tmp, x;
          if (response.status) {
            template = "<tr>\n    <td>{{ item }}</td>\n    <td>{{ purchase }}</td>\n    <td>{{ document }}</td>\n    <td>{{ projects }}</td>\n    <td>{{ transfer }}</td>\n    <td>{{ currency }}</td>\n    <td>{{!replace}}</td>\n    <td><a class=\"text-black\" target=\"_blank\" href=\"/media/{{ deposito }}\"><span class=\"glyphicon glyphicon-file\"></span></a></td>\n    <td><button value=\"{{ purchase }}\" class=\"btn btn-xs btn-link text-black btn-purchase\"><span class=\"glyphicon glyphicon-list\"></span></a>\n    </td>\n    <td>\n        {{!status}}\n    </td>\n</tr>";
            $tb = $("table > tbody");
            $tb.empty();
            for (x in response.list) {
              if (response.list[x].status === 'PE') {
                tmp = template.replace("{{!status}}", "<button class=\"btn btn-xs btn-link text-black btn-actions\" value=\"{{ purchase }}\"> <span class=\"glyphicon glyphicon-ok\"></span> </button>");
              } else {
                tmp = template;
              }
              if (response.list[x].status === 'CO') {
                tmp = tmp.replace("{{!replace}}", "Recibido-Completo");
              } else if (response.list[x].status === 'IN') {
                tmp = tmp.replace("{{!replace}}", "Recibido-Incompleto");
              } else if (response.list[x].status === 'PE') {
                tmp = tmp.replace("{{!replace}}", "Pendiente");
              } else if (response.list[x].status === 'AN') {
                tmp = tmp.replace("{{!replace}}", "Anulado");
              }
              response.list[x].item = parseInt(x) + 1;
              $tb.append(Mustache.render(tmp, response.list[x]));
            }
          }
        });
      }
    }
  });
};

openWindow = function() {
  window.open("/reports/order/purchase/" + this.value + "/", "_blank");
};

showActions = function(event) {
  $(".btn-delp,.btn-edtp").val(this.value);
  $(".mactions").modal("toggle");
};

showEditPurchasae = function(event) {
  $(".mactions").modal("hide");
  $(".nrop").text(this.value);
  getDataPurchase(this.value);
  $(".step-one").fadeOut(150);
  $(".step-two").fadeIn(800);
};

showStepOne = function(event) {
  $(".nrop").text("");
  $(".step-two").fadeOut(150);
  $(".step-one").fadeIn(800);
};

getDataPurchase = function(purchase) {
  var data;
  data = new Object;
  data.purchase = purchase;
  data.getpurchase = true;
  $.getJSON("", data, function(response) {
    var $tb, template, x;
    if (response.status) {
      $("[name=rucandreason]").text(response.reason);
      $("input[name=ruc]").val(response.supplier);
      $("input[name=reason]").val(response.reason);
      $("input[name=delivery]").val(response.space);
      $("select[name=document]").val(response.document);
      $("select[name=payment]").val(response.method);
      $("select[name=currency]").val(response.currency);
      $("input[name=transfer]").val(response.transfer);
      $("input[name=contact]").val(response.contact);
      $("input[name=quotation]").val(response.quotation);
      $("#observation_ifr").contents().find('body').html(response.observation);
      console.log(response.observation);
      $("input.edsct").val(response.discount);
      $("span.eigv").text(response.igv + "%");
      $tb = $("table.table-pod > tbody");
      $tb.empty();
      template = "<tr> <td> <input type=\"checkbox\" name=\"mats\" value=\"{{ materials }}\"> </td> <td>{{ item }}</td> <td>{{ materials }}</td> <td>{{ name }}</td> <td>{{ meter }}</td> <td>{{ unit }}</td> <td>{{ brand }}</td> <td>{{ model }}</td> <td>{{ quantity }}</td> <td>{{ price }}</td> <td>{{ discount }}</td> <td>{{ amount }}</td> <td> <button class=\"btn btn-xs btn-link text-green btn-sedit\" value=\"{{ materials }}\" data-name=\"{{ name }}\" data-met=\"{{ meter }}\" data-brand=\"{{ brand }}\" data-model=\"{{ model }}\" data-quantity=\"{{ quantity }}\" data-price=\"{{ price }}\" data-discount=\"{{ discount }}\"> <span class=\"glyphicon glyphicon-edit\"></span> </button> </td> </tr>";
      for (x in response.details) {
        response.details[x].item = parseInt(x) + 1;
        $tb.append(Mustache.render(template, response.details[x]));
      }
      calcAmount();
    } else {
      return $().toastmessage("showWarningToast", "No se han conseguidos los datos. " + response.raise);
    }
  });
};

calcAmount = function(event) {
  var amount, dsct, igv;
  amount = 0;
  $("table.table-pod > tbody > tr").each(function(index, element) {
    var $td;
    $td = $(element).find("td");
    amount += convertNumber($td.eq(11).text());
  });
  $(".tamount").text(amount.toFixed(2));
  dsct = (amount * convertNumber($("input.edsct").val())) / 100;
  $(".tdsct").text(dsct.toFixed(2));
  amount = amount - dsct;
  igv = $("span.eigv").text().split("%")[0];
  igv = amount * convertNumber(igv) / 100;
  $(".tigv").text(igv.toFixed(2));
  $(".ttotal").text((amount + igv).toFixed(2));
};

changeSelect = function(event) {
  $("input[name=select]").each(function(ind, radio) {
    if (this.checked) {
      $("input[name=mats]").each(function(index, element) {
        element.checked = Boolean(parseInt(radio.value));
      });
    }
  });
};

showPanelAdd = function(event) {
  var btn;
  btn = this;
  $(".panel-add").fadeToggle(600, function() {
    if (this.style.display === 'block') {
      $(btn).removeClass("btn-success text-black").addClass("btn-default").find("span").eq(0).removeClass("fa-plus-square-o").addClass("fa-times-circle-o");
      $(btn).find("span").eq(1).text("Cancelar");
    } else {
      $(btn).removeClass("btn-default").addClass("btn-success").addClass("text-black").find("span").eq(0).removeClass("fa-times-circle-o").addClass("fa-plus-square-o");
      $(btn).find("span").eq(1).text("Agregar Material");
    }
  });
};

addNewMaterialPurchase = function(event) {
  var data;
  data = new Object;
  data.code = $.trim($(".id-mat").text());
  if (data.code.length !== 15) {
    $().toastmessage("showWarningToast", "Seleccione por lo menos un material para ingresar.");
    return false;
  }
  data.quantity = convertNumber($("input[name=quantity]").val());
  if (isNaN(data.quantity) || data.quantity <= 0) {
    $().toastmessage("showWarningToast", "La cantidad ingresada debe ser mayor a 0.");
    return false;
  }
  data.price = convertNumber($("input[name=price]").val());
  if (isNaN(data.price) || data.price <= 0) {
    $().toastmessage("showWarningToast", "El precio ingresado debe ser mayor a 0.");
    return false;
  }
  data.discount = convertNumber($("input[name=discount]").val());
  if (isNaN(data.discount)) {
    data.discount = 0;
  }
  data.brand = $("select[name=brand]").val();
  data.model = $("select[name=model]").val();
  if (data.brand === "" || data.model === "") {
    $().toastmessage("showWarningToast", "Debe de seleccionar una marca y modelo.");
    return false;
  }
  if ($("input[name=gincludegroup]").length && $("input[name=gincludegroup]").is(":checked")) {
    if (tmpObjectDetailsGroupMaterials.details.length) {
      data.details = JSON.stringify(tmpObjectDetailsGroupMaterials.details);
    }
  }
  data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
  data.purchase = $.trim($("span.nrop").text());
  data.addDPurchase = true;
  $.post("", data, function(response) {
    var tmpObjectDetailsGroupMaterials;
    if (response.status) {
      tmpObjectDetailsGroupMaterials = new Object;
      listDetails();
    } else {
      $().toastmessage("showErrorToast", "No se a podido añadir el/los materiales. " + response.raise);
    }
  });
};

listDetails = function(event) {
  var data;
  data = new Object;
  data.listDetails = true;
  data.purchase = $.trim($("span.nrop").text());
  $.getJSON("", data, function(response) {
    var $tb, template, x;
    if (response.status) {
      $tb = $("table.table-pod > tbody");
      $tb.empty();
      template = "<tr> <td> <input type=\"checkbox\" name=\"mats\" value=\"{{ materials }}\"> </td> <td>{{ item }}</td> <td>{{ materials }}</td> <td>{{ name }}</td> <td>{{ meter }}</td> <td>{{ unit }}</td> <td>{{ brand }}</td> <td>{{ model }}</td> <td>{{ quantity }}</td> <td>{{ price }}</td> <td>{{ discount }}</td> <td>{{ amount }}</td> <td> <button class=\"btn btn-xs btn-link text-green btn-sedit\" value=\"{{ materials }}\" data-name=\"{{ name }}\" data-met=\"{{ meter }}\" data-brand=\"{{ brand }}\" data-model=\"{{ model }}\" data-quantity=\"{{ quantity }}\" data-price=\"{{ price }}\" data-discount=\"{{ discount }}\"> <span class=\"glyphicon glyphicon-edit\"></span> </button> </td> </tr>";
      for (x in response.details) {
        response.details[x].item = parseInt(x) + 1;
        $tb.append(Mustache.render(template, response.details[x]));
      }
      return calcAmount();
    }
  });
};

deleCheckMaterials = function(event) {
  var $chk, codes, counter, size;
  $chk = $("input[name=mats]");
  size = $chk.length;
  counter = 0;
  codes = new Array;
  $chk.each(function(index, element) {
    if (element.checked) {
      codes.push(element.value);
      counter++;
    }
  });
  if (counter > 0 && counter <= size) {
    $().toastmessage("showToast", {
      text: "Seguro(a) que desea eliminar el/los material(es) seleccionado(s).",
      sticky: true,
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
          data = new Object;
          data.purchase = $.trim($("span.nrop").text());
          data.materials = JSON.stringify(codes);
          data.delDPurchase = true;
          data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
          $.post("", data, function(response) {
            if (response.status) {
              listDetails();
            } else {
              $().toastmessage("showErrorToast", "No se a podido eliminar el/los material(es).");
            }
          });
        }
      }
    });
  } else {
    $().toastmessage("showWarningToast", "Seleccione por lo menos un material para eliminar.");
  }
};

showEditDetailsPurchase = function(event) {
  var $btn, brand, model;
  $btn = this;
  $(".nmaterial").text((this.getAttribute("data-name")) + "  -  " + (this.getAttribute("data-met")));
  $("input[name=ecmaterial]").val(this.value);
  brand = '';
  model = '';
  $.getJSON("/json/brand/list/option/", function(response) {
    brand = response;
  });
  $.getJSON("/json/model/list/option/", function(response) {
    model = response;
  });
  setTimeout(function() {
    var $ob, $om, objectDataBrand, objectDataModel, opb, opm, tob, tom, x;
    opb = "<option value=\"{{ brand_id }}\" {{!se}}>{{ brand }}</option>";
    opm = "<option value=\"{{ model_id }}\" {{!se}}>{{ model }}</option>";
    $ob = $("select[name=ebrand]");
    $ob.empty();
    for (x in brand.brand) {
      tob = opb;
      if (brand.brand[x].brand === $btn.getAttribute("data-brand")) {
        tob = tob.replace("{{!se}}", "selected");
      }
      $ob.append(Mustache.render(tob, brand.brand[x]));
    }
    $om = $("select[name=emodel]");
    $om.empty();
    for (x in model.model) {
      tom = opm;
      if (model.model[x].model === $btn.getAttribute("data-model")) {
        tom = tom.replace("{{!se}}", "selected");
      }
      $om.append(Mustache.render(tom, model.model[x]));
    }
    $("input[name=equantity]").val($btn.getAttribute("data-quantity"));
    $("input[name=eprice]").val($btn.getAttribute("data-price"));
    $("input[name=ediscount]").val($btn.getAttribute("data-discount"));
    $(".mdpurchase").modal("show");
    objectDataBrand = new Object;
    return objectDataModel = new Object;
  }, 1000);
};

saveEditDetailsPurchase = function(event) {
  var data;
  data = new Object;
  data.materials = $("input[name=ecmaterial]").val();
  if (data.materials.length !== 15) {
    $().toastmessage("showWarningToast", "Seleccione por lo menos un material para modificar.");
    return false;
  }
  data.quantity = convertNumber($("input[name=equantity]").val());
  if (isNaN(data.quantity) || data.quantity <= 0) {
    $().toastmessage("showWarningToast", "La cantidad ingresada debe ser mayor que 0.");
    return false;
  }
  data.price = convertNumber($("input[name=eprice]").val());
  if (isNaN(data.price) || data.price <= 0) {
    $().toastmessage("showWarningToast", "El precio ingresado debe ser mayor que 0.");
    return false;
  }
  data.discount = convertNumber($("input[name=ediscount]").val());
  if (isNaN(data.discount)) {
    data.discount = 0;
  }
  data.brand = $("select[name=ebrand]").val();
  data.model = $("select[name=emodel]").val();
  if (data.brand === "" || data.model === "") {
    $().toastmessage("showWarningToast", "Debe de seleccionar una marca y modelo.");
    return false;
  }
  data.editDPurchase = true;
  data.purchase = $.trim($("span.nrop").text());
  data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
  console.log(data);
  $.post("", data, function(response) {
    if (response.status) {
      $("input[name=equantity]").val("");
      $("input[name=eprice]").val("");
      $("input[name=ediscount]").val("");
      $(".mdpurchase").modal("hide");
      listDetails();
    } else {
      $().toastmessage("showErrorToast", "No se a actualizado el material.");
    }
  }, "json");
};

showChoiceDeposit = function(event) {
  $("input[name=deposit]").click();
};

savePurchase = function(event) {
  var $files, data;
  data = new FormData;
  data.append("delivery", $("input[name=delivery]").val());
  data.append("document", $("select[name=document]").val());
  data.append("payment", $("select[name=payment]").val());
  data.append("currency", $("select[name=currency]").val());
  data.append("transfer", $("input[name=transfer]").val());
  data.append("contact", $("input[name=contact]").val());
  data.append("purchase", $.trim($("span.nrop").text()));
  data.append("discount", convertNumber($("input.edsct").val()));
  data.append("purchaseSave", true);
  data.append("quotation", $("[name=quotation]").val());
  data.append("observation", $("#observation_ifr").contents().find("body").html());
  data.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());
  $files = $("input[name=deposit]");
  if ($files.get(0).files.length) {
    data.append("deposit", $files.get(0).files[0]);
  }
  $.ajax({
    data: data,
    url: "",
    type: "POST",
    dataType: "json",
    cache: false,
    processData: false,
    contentType: false,
    success: function(response) {
      console.log(response);
      if (response.status) {
        location.reload();
      } else {
        $().toastmessage("showErrorToast", "No se han realizado los cambios en la Orden de Compra. " + response.raise);
      }
    }
  });
};

annularPurchase = function(event) {
  var btn;
  btn = this;
  $().toastmessage("showToast", {
    text: "Realmente desea anular la Orden de compra Nro " + this.value,
    sticky: true,
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
        data = new Object;
        data.annularPurchase = true;
        data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
        data.purchase = btn.value;
        $.post("", data, function(response) {
          if (response.status) {
            return location.reload();
          } else {
            return $().toastmessage("showErrorToast", "No se a anulado la Orden de Compra. " + response.raise);
          }
        });
      }
    }
  });
};
