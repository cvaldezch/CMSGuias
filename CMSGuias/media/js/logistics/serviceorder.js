var addItem, calcamount, changeDsct, changeRadio, getListTmp, listDetails, loadEdit, saveServiceOrder, selectDel, selectProject, showList, showNew;

$(document).ready(function() {
  $(".btn-erase-fields,.btn-generate,.panel-new,.btn-list").hide();
  $("input[name=start],input[name=execution]").datepicker({
    changeMonth: true,
    changeYear: true,
    closeText: "Cerrar",
    dateFormat: "yy-mm-dd",
    showAnim: "slide",
    showButtonPanel: true
  });
  $("select[name=project]").on("click", selectProject);
  $("button.btn-add-item").on("click", addItem);
  $("button.btn-refresh").on("click", getListTmp);
  $("input[name=dsct]").on("change keyup", changeDsct);
  $("input[name=sel]").on("change", changeRadio);
  $("button.btn-del").on("click", selectDel);
  $(document).on("click", "button.btn-edit", loadEdit);
  $("button.btn-new").on("click", showNew);
  $("button.btn-list").on("click", showList);
  $("button.btn-generate").on("click", saveServiceOrder);
  $("textarea[name=desc]").trumbowyg();
  $(".trumbowyg-box,.trumbowyg-editor").css({
    minHeight: "250px !important"
  });
  $(".chosen-select").chosen({
    no_results_next: "Oops, nada encontrado!",
    width: "100%"
  });
});

showNew = function(event) {
  $("div.panel-list, button.btn-new").fadeOut(150);
  $("div.panel-new, button.btn-list, button.btn-generate").fadeIn(1200);
  getListTmp();
};

showList = function(event) {
  $("div.panel-new, button.btn-list, button.btn-generate").fadeOut(150);
  $("div.panel-list, button.btn-new").fadeIn(1200);
};

selectProject = function(event) {
  var $pro, data;
  $pro = $(this);
  if ($pro.val()) {
    data = new Object;
    data.pro = $pro.val();
    data.changeProject = true;
    $.getJSON("", data, function(response) {
      var $sub, tmp, x;
      if (response.status) {
        $sub = $("[name=subproject]");
        $sub.empty();
        if (response.subprojects) {
          tmp = "<option value=\"{{ id }}\">{{ x.subproject }}</option>";
          for (x in response.subprojects) {
            $sub.append(Mustache.render(tmp, response.subprojects[x]));
          }
        }
        $("input[name=arrival]").val(response.address);
      } else {
        $().toastmessage("showErrorToast", "No se a encontrado Proyectos. " + response.raise);
      }
    });
  }
};

addItem = function(event) {
  var data;
  data = new Object;
  $("div.modal-body").find("input, select, textarea").each(function(index, element) {
    if (element.value === "") {
      $().toastmessage("showWarningToast", "Campo vacio. " + element.name);
      return false;
    } else {
      data[element.name] = element.value;
    }
  });
  if (Object.keys(data).length) {
    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
    data.additem = true;
    if ($("input[name=edit-item]").val()) {
      data.pk = parseInt($("input[name=edit-item]").val());
    }
    $.post("", data, function(response) {
      if (response.status) {
        listDetails(response);
        $("input[name=edit-item]").val("");
      } else {
        $().toastmessage("showErrorToast", "No se a podido agregar el Item");
      }
    });
  }
};

listDetails = function(response) {
  var $tb, temp, x;
  if (Object.keys(response).length) {
    temp = "<tr> <td class=\"text-center\"> <input type=\"checkbox\" name=\"items\" value=\"{{ item }}\"> </td> <td class=\"text-center\">{{ item }}</td> <td>{{{ description }}}</td> <td class=\"text-right\">{{ quantity }}</td> <td class=\"text-center\">{{ unit }}</td> <td class=\"text-right\">{{ price }}</td> <td class=\"text-right\">{{ amount }}</td> <td class=\"text-center\"> <button class=\"btn btn-xs text-green btn-link btn-edit\" data-item=\"{{ item }}\" data-desc=\"{{ description }}\" data-quantity=\"{{ quantity }}\" data-unit=\"{{ unit }}\" data-price=\"{{ price }}\"> <span class=\"fa fa-edit\"></span> </button> </td> </tr>";
    $tb = $("table.table-details > tbody");
    $tb.empty();
    for (x in response.list) {
      response.list[x].description = $tb.append(Mustache.to_html(temp, response.list[x]));
    }
    calcamount();
  }
};

getListTmp = function(event) {
  var data;
  $("button > span.fa-refresh").addClass("fa-spin");
  data = new Object;
  data.list = true;
  data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
  $.post("", data, function(response) {
    if (response.status) {
      listDetails(response);
      $("button > span.fa-refresh").removeClass("fa-spin");
    } else {
      $().toastmessage("showErrorToast", "No se a realizado la lista.");
    }
  });
};

calcamount = function(event) {
  var amount, dsct, igv;
  amount = 0;
  $("table.table-details > tbody > tr").each(function(index, element) {
    var $td;
    $td = $(element).find("td");
    amount += parseFloat($td.eq(6).text());
  });
  igv = parseFloat($(".vigv").text()) / 100;
  dsct = parseFloat($(".vdsct").text() || 0) / 100;
  $(".rdsct").text((amount * dsct).toFixed(2));
  $(".ramount").text(amount.toFixed(2));
  amount = amount - (amount * dsct);
  igv = amount * igv;
  $(".rigv").text(igv.toFixed(2));
  $(".rtotal").text((amount + igv).toFixed(2));
};

changeDsct = function(event) {
  $(".vdsct").text(this.value);
  calcamount();
};

changeRadio = function(event) {
  $(this).each(function(index, element) {
    if (element.checked) {
      $("input[name=items]").each(function(index, chk) {
        chk.checked = Boolean(parseInt(element.value));
      });
    }
  });
};

selectDel = function(event) {
  var del;
  del = new Array;
  $("input[name=items]").each(function(index, chk) {
    if (chk.checked) {
      del.push(chk.value);
    }
  });
  if (del.length) {
    $().toastmessage("showToast", {
      text: "Realmente desea eliminar los items seleccionados?",
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
        var data;
        if (result === "Si") {
          data = new Object;
          data.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
          data.items = JSON.stringify(del);
          data.del = true;
          return $.post("", data, function(response) {
            if (response.status) {
              return listDetails(response);
            } else {
              return $().toastmessage("showErrorToast", "No se eliminado los Items. " + response.raise);
            }
          });
        }
      }
    });
    return;
  } else {
    $().toastmessage("showWarningToast", "Debe de seleccionar por lo menos un item.");
    return;
  }
};

loadEdit = function(event) {
  $("input[name=edit-item]").val(this.getAttribute("data-item"));
  $("textarea[name=desc]").trumbowyg('html', this.getAttribute("data-desc"));
  $("select[name=unit]").val(this.getAttribute("data-unit"));
  $("input[name=quantity]").val(this.getAttribute("data-quantity"));
  $("input[name=price]").val(this.getAttribute("data-price"));
  $("div#mdetails").modal("show");
};

saveServiceOrder = function(event) {
  var data, i, len, prm, ref, valid, x;
  data = new Object;
  data.project = $("select[name=project]").val();
  data.subproject = $("select[name=subproject]").val();
  data.supplier = $("select[name=supplier]").val();
  data.quotation = $("input[name=quotation]").val() || '';
  data.arrival = $("input[name=arrival]").val();
  data.document = $("select[name=document]").val();
  data.method = $("select[name=method]").val();
  data.currency = $("select[name=currency]").val();
  data.start = $("input[name=start]").val();
  data.term = $("input[name=execution]").val();
  data.dsct = $("input[name=dsct]").val();
  data.authorized = $("select[name=authorized]").val();
  ref = Object.keys(data);
  for (i = 0, len = ref.length; i < len; i++) {
    x = ref[i];
    if (data[x] === "" && x !== "quotation") {
      valid = false;
      break;
    } else {
      valid = true;
    }
  }
  if (valid) {
    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
    data.generateService = true;
    prm = new FormData();
    for (x in data) {
      prm.append(x, data[x]);
    }
    if ($("input[name=deposit]").get(0).files.length) {
      prm.append("deposit", $("input[name=deposit]").get(0).files[0]);
    }
    $.ajax({
      url: "",
      data: prm,
      type: "POST",
      dataType: "json",
      cache: false,
      processData: false,
      contentType: false,
      success: function(response) {
        if (response.status) {
          $().toastmessage("showSuccessToast", "Se a generado Orden de Servicio: " + response.service);
          setTimeout(function() {
            location.reload();
          }, 2600);
        } else {
          $().toastmessage("showErrorToast", "No se a generado Orden de Servicio. " + response.status);
        }
      }
    });
  } else {
    $().toastmessage("showWarningToast", "Se a encontrado un campo vacio.");
  }
};
