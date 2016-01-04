var LetterAnular, addDetailsPurchase, approvedProject, assignedResponsible, calAmountPurchaseOrder, changeView, closeStorage, closureProject, deleteDetailsPurchase, deleteOrderPurchase, deleteSubproject, editLetter, fileTree, genKeyConfirmationApproved, genKeyConfirmationClosureProject, genKeyConfirmationResponsible, generateLetter, getAmountLiteral, getEditPurchase, getListLetter, getListPurchaseOrder, getPercentIVA, getSectors, letterToggle, loadCloseAccounting, loadDocumentsClosure, loadsAccounts, openNewSector, openNewSubproyecto, openUpdateSector, openUpdateSubproject, openWindow, publisherCommnet, savePurchaseOrder, setSubproject, showAlertStartProject, showEditComment, showEditDetailsPurchase, showGuideByProject, showLetter, showLetterAnexosUpload, showLetterEdit, showLetterObservation, showLetterUpload, showListAnexos, showLoadPrices, toggleComment, toggleInfoClose, treeAdminaandOpera, uploadFiles, uploadLetter, uploadLetterAnexo, uploadLetterDelivery, uploadLoadPrices;

$(document).ready(function() {
  $(".panel-purchase-order-toggle").hide();
  $("input[name=podt],input[name=podf]").datepicker({
    "changeYear": true,
    "changeMonth": true,
    "showAnim": "slide",
    "dateFormat": "yy-mm-dd"
  });
  $(".new-sector").on("click", openNewSector);
  $(document).on("click", ".btn-edit-sector", openUpdateSector);
  $(".new-subproject").on("click", openNewSubproyecto);
  $(document).on("click", "#accordion > .panel-primary", setSubproject);
  $(document).on("click", ".btn-edit-sub", openUpdateSubproject);
  $(".btn-responsible").on("click", function() {
    return $(".mresponsible").modal("show");
  });
  $(".btn-files").on("click", function() {
    return $(".mfiles").modal("show");
  });
  $(".btn-cuadro").on("click", function(event) {
    return changeView(23);
  });
  $(".btn-list").on("click", function(event) {
    return changeView(100);
  });
  $(".btn-admin").on("click", function() {
    return $("[name=administrative]").click();
  });
  $(".btn-opera").on("click", function() {
    return $("[name=operation]").click();
  });
  $(".btn-upload-files").on("click", uploadFiles);
  $(".btn-show-comment").on("click", toggleComment);
  $(".btn-message-edit").on("click", showEditComment);
  $(".btn-message-del").on("click", showEditComment);
  $(".btn-assigned").on("click", assignedResponsible);
  $(".btn-approved").on("click", approvedProject);
  $(document).on("click", ".btn-del-sub", deleteSubproject);
  $(".btn-add-purchase-order-details").on("click", addDetailsPurchase);
  $("input[name=podt]").on("change", getPercentIVA);
  $(document).on("click", ".btn-edit-pod", showEditDetailsPurchase);
  $(document).on("click", ".btn-del-pod", deleteDetailsPurchase);
  $(".btn-re-purchase-order").on("click", getListPurchaseOrder);
  $(".btn-saved-purchase").on("click", savePurchaseOrder);
  $(document).on("click", ".btn-edit-purchase", getEditPurchase);
  $(document).on("click", ".btn-del-purchase", deleteOrderPurchase);
  $(".btn-details-purchare-order-toggle").click(function() {
    var $btn;
    $btn = $(this);
    $("div.panel-purchase-order-toggle").toggle(600, function() {
      if ($(".panel-purchase-order-toggle").is(":visible")) {
        $btn.find("span").eq(0).removeClass("glyphicon-plus-sign").addClass("glyphicon-minus-sign");
        $btn.find("span").eq(1).text("Cancelar");
        $btn.removeClass("text-green").addClass("text-red");
        return;
      } else {
        $btn.find("span").eq(0).removeClass("glyphicon-minus-sign").addClass("glyphicon-plus-sign");
        $btn.find("span").eq(1).text("Agregar Detalle");
        $btn.removeClass("text-red").addClass("text-green");
        return;
      }
      return $("input[name=podedit]").val("");
    });
  });
  $("button.btn-add-purchase-order").mouseover(function() {
    $(this).find("span").removeClass("glyphicon-plus-sign").addClass("glyphicon-plus");
  }).mouseout(function() {
    $(this).find("span").removeClass("glyphicon-plus").addClass("glyphicon-plus-sign");
  }).click(function() {
    $("div.mpurchase").modal("toggle");
  });
  $("#message").focus(function() {
    $(this).animate({
      "height": "102px"
    }, 500);
  }).blur(function() {
    $(this).animate({
      "height": "34px"
    }, 500);
  });
  $("input[name=poids]").blur(function(event) {
    var percent;
    percent = parseFloat(this.value);
    if (!isNaN(percent)) {
      this.value = percent.toFixed(3);
      calAmountPurchaseOrder();
    } else {
      this.value = 0;
      $().toastmessage("showWarningToast", "Solo se aceptan Números.");
    }
    $(".pods").text(this.value + "%");
  }).change(function(event) {
    $(".pods").text(this.value + "%");
    calAmountPurchaseOrder();
  });
  $("button.btn-show-letter").on("click", showLetter);
  treeAdminaandOpera();
  getListPurchaseOrder();
  getListLetter();
  tinymce.init({
    selector: "textarea#message",
    theme: "modern",
    menubar: false,
    statusbar: false,
    plugins: "link contextmenu",
    font_size_style_values: "10px,12px,13px,14px,16px,18px,20px",
    toolbar: "undo redo | styleselect | fontsizeselect |"
  });
  $(".btn-publisher").on("click", publisherCommnet);
  $("button.btn-emails").on("click", showAlertStartProject);
  $("input[name=mailer-enable]").checkboxpicker().on("change", loadsAccounts);
  $("button.btn-gen-responsible").on("click", genKeyConfirmationResponsible);
  $("button.btn-gen-approved").on("click", genKeyConfirmationApproved);
  $("button.btn-show-loadprices").on("click", showLoadPrices);
  $("button[name=upload-prices]").on("click", uploadLoadPrices);
  $("button.btn-show-guides").on("click", showGuideByProject);
  $(".generate-letter").on("click", generateLetter);
  $(document).on("click", ".btn-letter-show-up", showLetterUpload);
  $(document).on("click", ".btn-letter-show-anx", showLetterAnexosUpload);
  $(document).on("click", ".btn-letter-show-edit", showLetterEdit);
  $(document).on("click", ".btn-letter-anular", LetterAnular);
  $(".btn-letter-upload").on("click", uploadLetter);
  $(".btn-upload-anexos").on("click", uploadLetterAnexo);
  $(".edit-letter").on("click", editLetter);
  $(".btn-circle").on("click", toggleInfoClose);
  $(document).on("click", ".btn-letter-show-observation", showLetterObservation);
  $(document).on("click", ".btn-letter-show-details", showListAnexos);
  $(".btn-letter-toggle").on("click", letterToggle);
  $(".btn-open-letter-file").click(function() {
    $("input[name=letter-file]").click();
  });
  $(".btn-open-letter-anexo-file").click(function() {
    $("input[name=letter-anexos-file]").click();
  });
  $(".btn-close-storage").on("click", closeStorage);
  $(".uploadletterclosep").on("click", uploadLetterDelivery);
  $(".btn-documents-closure").on("click", loadDocumentsClosure);
  $(".btn-closure-accounting").on("click", loadCloseAccounting);
  $(".generatekeyclosure").on("click", genKeyConfirmationClosureProject);
  $(".closureProject").on("click", closureProject);
});

loadsAccounts = function(event) {
  if ($("input[name=mailer-enable]").is(":checked")) {
    showGlobalEnvelop();
    $("iframe#globalmbody_ifr").contents().find("body").html($("#message_ifr").contents().find("body").html());
    if ($("select[name=globalmfor]").find("option").length === 0) {
      getAllCurrentAccounts();
      setTimeout(function() {
        var $item, c, items, j, k, len, len1, ref, tmp, x;
        if (globalMailerData.hasOwnProperty("fors")) {
          items = ["for", "cc", "cco"];
          for (j = 0, len = items.length; j < len; j++) {
            c = items[j];
            $item = $("select[name=globalm" + c + "]");
            tmp = "<option value=\"{{ email }}\">{{ email }}</option>";
            ref = globalMailerData.fors;
            for (k = 0, len1 = ref.length; k < len1; k++) {
              x = ref[k];
              $item.append("<option value=\"" + x + "\">" + x + "</option>");
            }
            $item.trigger("chosen:updated");
          }
        }
      }, 200);
    }
  }
};

showAlertStartProject = function(event) {
  var $pro, reason;
  $pro = $("input[name=pro]");
  reason = $("input[name=companyname]").val();
  setTimeout(function() {

    /*globalMailerData.fors = "asistente1@icrperusa.com,
                        logistica@icrperusa.com,
                        luis.martinez@icrperusa.com,
                        cvaldezchavez@gmail.com,
                        icr.luisvalencia@gmail.com,
                        almacen@icrperusa.com,
                        armando.atencio@icrperusa.com,
                        steven.paredes@icrperusa.com,
                        danilo.martinez@icrperusa.com,
                        sandra.atencio@icrperusa.com,
                        ssoma1@icrperusa.com"
     */
    globalMailerData.issue = "Apertura de Proyecto " + ($pro.attr("data-name")) + " - " + ($pro.attr("data-customers"));
    return globalMailerData.body = "<p><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\">Estimados,</span></p><p style=\"text-align: justify;\" data-mce-style=\"text-align: justify;\"><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\">Para hacerles de su conocimiento que hoy " + (new Date().toLocaleDateString()) + " se realiza la apertura del proyecto <strong>\"" + ($pro.attr("data-name")) + "\"</strong>  con código <strong>\"" + ($pro.val()) + "\"</strong> que se realizara en \"" + ($pro.attr("data-address")) + "\" para el cliente <strong>\"" + ($pro.attr("data-customers")) + "\"</strong>. El proyecto tendrá como fecha de inicio " + ($pro.attr("data-star")) + " y un fecha de termino aproximada para el " + ($pro.attr("data-end")) + ".</span></p><p><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\">" + ($(".contact-project").html().trim()) + "</span></p><p><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\"><strong>Supervisor responsable: " + ($("#superviser").text()) + "</strong>.&nbsp;</span></p><p><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\"><strong>Ejecutado por</strong> : " + reason + "</span></p><p><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\"><br data-mce-bogus=\"1\"></span></p><p><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\">Recuerden que desde la fecha rige todo lo establecido el pasado sábado 02 de Enero del 2016, por lo que les agredeceré comunicarse conmigo prontamente para agendar la reunión de apertura; y posteriormente generen su lista de ejecución solo con lo cual podra ser atendido su pedido.</span></p><p><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\">Saludos.</span></p><p><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\"><strong>Luis Martinez</strong></span><br /><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\"><strong>" + ($("input[name=companyname]").val()) + "</strong></span><br></p><p><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\"><strong>Telf:</strong> " + ($("input[name=companyname]").attr("data-phone")) + "</span></p><p><br data-mce-bogus=\"1\"></p>";
  }, 100);
  setTimeout(function() {
    $("input[name=user-email]").val("luis.martinez@icrperusa.com").attr("data-name", "Luis Martinez");
    return showGlobalEnvelop();
  }, 800);
};

approvedProject = function() {
  var data;
  data = new Object();
  data.type = "approved";
  data.passwd = $("input[name=passwd-approve]").val();
  data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
  $().toastmessage("showToast", {
    text: "Realmente desea habilitar el proyecto?",
    type: "confirm",
    sticky: true,
    buttons: [
      {
        value: 'No'
      }, {
        value: 'Si'
      }
    ],
    success: function(result) {
      if (result === "Si") {
        $.post("", data, function(response) {
          if (response.status) {
            return location.reload();
          } else {
            return $().toastmessage("showWarningToast", "Fallo Transaccion: " + response.raise);
          }
        }, "json");
      }
    }
  });
};

assignedResponsible = function() {
  var data, passwd, responsible;
  responsible = $("select[name=responsible]").val();
  passwd = $("input[name=passwd]").val();
  if ((responsible != null) && (passwd != null)) {
    data = new Object();
    data.responsible = responsible;
    data.passwd = passwd;
    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
    data.type = 'responsible';
    $.post("", data, function(response) {
      var $pro, param;
      if (response.status) {
        $pro = $("input[name=pro]");
        param = {
          'getfors': true,
          'name': $pro.attr("data-name")
        };
        $.get("/json/get/emails/starts/", param, function(rmail) {
          if (rmail.status) {
            data = new Object;
            data.forsb = rmail.fors;
            data.issue = "Responsable de Proyecto " + ($pro.attr("data-name"));
            data.body = "<p><span style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\" data-mce-style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\">Proyecto " + ($pro.val()) + " - " + ($pro.attr("data-name")) + " se asigno al responsable: <strong>" + ($("#responsible option:selected").text()) + "</strong>.&nbsp;</span></p><p>Proyecto:&nbsp; <strong>" + ($pro.attr("data-name")) + "</strong></p><p>Fecha y hora: " + (new Date().toString()) + "</p><p><span data-mce-style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\" style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\">Si no has realizado esta operación o tienes cualquier duda, puedes comunicarte con nosotros +51 1 371-0443.</span></p>";
            console.log(data);
            $.ajax({
              url: "http://190.41.246.91:3000/mailer/",
              type: "GET",
              crossDomain: true,
              data: $.param(data),
              dataType: "jsonp",
              success: function(response) {
                if (response.status) {
                  location.reload();
                } else {
                  $().toastmessage("showErrorToast", "No se podido enviar el correo.");
                }
              }
            });
          }
        });
      } else {
        $().toastmessage("showErrorToast", "El código ingresado es incorrecto: " + response.raise);
      }
    });
  }
};

publisherCommnet = function() {
  var data;
  data = new Object();
  data.edit = $("input[name=edit-message]").val();
  data.message = $.trim($("#message_ifr").contents().find("body").html());
  data.status = $("select[name=message-status]").val();
  if (data.message === "<p><br data-mce-bogus=\"1\"></p>") {
    $().toastmessage("showWarningToast", "No se puede publicar el mensaje, campo vacio.");
    return false;
  }
  if (data.edit === "") {
    data.type = "add";
  } else {
    data.type = "edit";
  }
  data.proyecto = $("input[name=pro]").val();
  data.subproyecto = $("input[name=sub]").val();
  data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
  $.post("", data, function(response) {
    if (response.status) {
      return location.reload();
    }
  });
};

showEditComment = function() {
  var id;
  if (this.getAttribute("data-id") !== "") {
    id = this.getAttribute("data-id");
    $("#message_ifr").contents().find("body").html($(".comment" + id).find("div").eq(2).html());
    $("select[message-status]").val(this.getAttribute("data-status"));
    $("input[name=edit-message]").val(id);
  }
};


/*listComment = ->
    $.getJSON "", "list":"comment", (response) ->
        if response.status
            template = "
            <div class=\"alert alert-{{ status }} comment{{ id }}\">
                <div>
                    {{!editing}}
                    <small>{{ date }} {{ time }}</small>
                </div>
                <div>
                    {{ message }}
                </div>
                <div>
                    <small class=\"pull-right\">{{ charge }}</small>
                </div>
            </div>"
            edit = "<div class=\"btn-group pull-right\">
                        <button type=\"button\" data-toggle=\"dropdown\" class=\"btn btn-xs btn-link text-black dropdown-toggle\"><span class=\"glyphicon glyphicon-collapse-down\"></span></button>
                        <ul role=\"menu\" class=\"dropdown-menu\">
                            <li><a data-status=\"{{ status }}\" data-id=\"{{ id }}\" class=\"btn-message-edit\">Editar</a></li>
                            <li><a data-status=\"{{ status }}\" data-id=\"{{ id }}\" class=\"btn-message-del\">Eliminar</a></li>
                        </ul>
                    </div>"
            $panel = $("div.comment-list > .panel-body")
            $panel.empty()
            dni = $("input[name=dni]").val()
            html = ""
            for x of response.alerts
                if x.empdni == dni
                    template = template.replace "{{!editing}}", edit
                html = html.concat Mustache.to_html template, response.alerts[x]
            console.log html
            $panel.html html
            return
    return
 */

toggleComment = function() {
  $(".panel-comment").find(".panel-body").toggle(function() {
    if ($(this).is(":hidden")) {
      $(".btn-show-comment").find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
      return $(".panel-comment").css("height", "1em");
    } else {
      $(".btn-show-comment").find("span").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
      return $(".panel-comment").css("height", "23em");
    }
  });
};

treeAdminaandOpera = function() {
  var admin, opera, year;
  year = "20" + ($("input[name=pro]").val().substring(2, 4));
  if ($("input[name=sub]").val() === "") {
    admin = "/storage/projects/" + year + "/" + ($("input[name=pro]").val()) + "/administrative/";
    opera = "/storage/projects/" + year + "/" + ($("input[name=pro]").val()) + "/operation/";
  } else {
    admin = "/storage/projects/" + year + "/" + ($("input[name=pro]").val()) + "/" + ($("input[name=sub]").val()) + "/administrative/";
    opera = "/storage/projects/" + year + "/" + ($("input[name=pro]").val()) + "/" + ($("input[name=sub]").val()) + "/operation/";
  }
  fileTree('filetree_administrative', admin);
  fileTree('filetree_operation', opera);
};

fileTree = function(id, path) {
  $("#" + id).fileTree({
    root: path,
    script: "/json/get/path/",
    folderEvent: "click",
    expandSpeed: 750,
    collapseSpeed: 750,
    multiFolder: true
  }, function(file) {
    console.log(file);
    return window.open(file, "_blank");
  });
};

setSubproject = function(event) {
  $("input[name=sub]").val($(this).attr("data-sub"));
  if ($("input[name=sub]").val() !== "") {
    $(".header-project > .info-sub").remove();
    $(".header-project").append("<p class=\"info-sub\"><strong>Subproyecto :</strong> " + ($(".text-" + $(this).attr("data-sub")).html()) + " <strong> Codigo :</strong> " + ($(this).attr("data-sub")) + "</p>");
  } else {
    $("input[name=sub]").val();
    $(".header-project > .info-sub").remove();
  }
  getSectors();
};

getSectors = function() {
  var data, url;
  data = new Object();
  data.pro = $("input[name=pro]").val();
  data.sub = $("input[name=sub]").val();
  url = "/sales/projects/sectors/crud/";
  $.getJSON(url, data, function(response) {
    var $list, $sec, edit, editable, template, templist, x;
    if (response.status) {
      if (data.sub === "") {
        data.sub = "None";
      }
      template = "<article> {{!editable}} <a href=\"/sales/projects/manager/sector/" + data.pro + "/" + data.sub + "/{{ sector_id }}/\" class=\"text-black\"> {{ sector_id }} {{ nomsec }} <small>{{ planoid }}</small> </a> </article>";
      edit = "<button class=\"btn btn-xs text-black btn-link pull-left btn-edit-sector\" value=\"{{ sector_id }}\"> <span class=\"glyphicon glyphicon-pencil\"></span> </button> <button class=\"btn btn-xs text-black btn-link pull-right\" value=\"{{ sector_id }}\"> <span class=\"glyphicon glyphicon-trash\"></span> </button>";
      editable = $("input[name=status-project]").val();
      if (editable !== 'AC') {
        template = template.replace("{{!editable}}", edit);
      }
      templist = "<li><a href=\"/sales/projects/manager/sector/" + data.pro + "/" + data.sub + "/{{ sector_id }}/\" class=\"text-black\"><span class=\"glyphicon glyphicon-chevron-right\"></span> {{ nomsec }}</a></li>";
      $list = data['sub'] === "" ? $(".sectorsdefault") : $(".sectors" + data['sub']);
      $sec = $(".all-sectors");
      $sec.empty();
      $list.empty();
      for (x in response.list) {
        $sec.append(Mustache.render(template, response.list[x]));
        $list.append(Mustache.render(templist, response.list[x]));
      }
      equalheight(".all-sectors article");
    } else {
      return $().toastmessage("showErrorToast", "Error, transaction not complete. " + response.raise);
    }
  });
};

openNewSector = function(event) {
  var pro, sub, url;
  pro = $("input[name=pro]").val();
  sub = $("input[name=sub]").val();
  url = "/sales/projects/sectors/crud/?pro=" + pro + "&sub=" + sub + "&type=new";
  openWindow(url, false);
};

openUpdateSector = function(event) {
  var pro, sec, sub, url;
  pro = $("input[name=pro]").val();
  sub = $("input[name=sub]").val();
  sec = this.value;
  url = "/sales/projects/sectors/crud/?pro=" + pro + "&sub=" + sub + "&sec=" + sec + "&type=update";
  openWindow(url, false);
};

openNewSubproyecto = function(event) {
  var pro, url;
  pro = $("input[name=pro]").val();
  url = "/sales/projects/subprojects/crud/?pro=" + pro + "&type=new";
  openWindow(url, true);
};

openUpdateSubproject = function(event) {
  var pro, sub, url;
  pro = $("input[name=pro]").val();
  sub = this.value;
  url = "/sales/projects/subprojects/crud/?pro=" + pro + "&sub=" + sub + "&type=update";
  openWindow(url, true);
};

openWindow = function(url, reload) {
  var interval, win;
  win = window.open(url, "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600");
  interval = window.setInterval(function() {
    if (win === null || win.closed) {
      window.clearInterval(interval);
      if (reload) {
        location.reload();
      } else {
        getSectors();
      }
    }
  }, 1000);
  return win;
};

changeView = function(percent) {
  $(".all-sectors > article").css({
    "width": percent + "%"
  });
  equalheight(".all-sectors article");
};

uploadFiles = function(event) {
  var data;
  data = new FormData();
  $("input[name=administrative], input[name=operation]").each(function(index, element) {
    if (this.files[0] != null) {
      data.append(this.name, this.files[0]);
    }
  });
  data.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());
  data.append("type", "files");
  data.append("pro", $("input[name=pro]").val());
  data.append("sub", $("input[name=sub]").val());
  $.ajax({
    data: data,
    url: "",
    type: "POST",
    dataType: "json",
    cache: false,
    processData: false,
    contentType: false,
    success: function(response) {
      if (response.status) {
        return location.reload();
      } else {
        return $().toastmessage("showErrorToast", "Error al subir los archivos al servidor");
      }
    }
  });
};

deleteSubproject = function() {
  var del;
  del = this;
  $().toastmessage("showToast", {
    text: "Debe tener en cuenta que al eliminar el Subproyecto (Adicional) este eliminara todos los sectores y materiales que contenga. Desea Eliminar el subproyecto (Adicional)?",
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
        data = new Object();
        data.delsub = true;
        data.sub = del.value;
        data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
        $.post("", data, function(response) {
          if (response.status) {
            $().toastmessage("showNoticeToast", "Se a eliminado correctamente.");
            return setTimeout(function() {
              return location.reload();
            }, 2600);
          } else {
            return $().toastmessage("showErrorToast", "No se a podido eliminar el Subproyecto. " + response.raise);
          }
        }, "json");
      }
    }
  });
};

calAmountPurchaseOrder = function() {
  var amount, dsct, igv, pdsct, pigv, total;
  amount = 0;
  $(".table-details-purchase-order > tbody > tr").each(function(index, element) {
    var $td;
    $td = $(element).find("td");
    return amount += convertNumber($td.eq(6).text());
  });
  $(".pos").text(amount);
  if (isNaN(amount)) {
    amount = 0;
  }
  pdsct = parseFloat($("input[name=poids]").val());
  dsct = (amount * pdsct) / 100;
  amount = amount - dsct;
  pigv = $(".povigv").text().split("%");
  pigv = parseInt(pigv[0]);
  igv = (amount * pigv) / 100;
  total = amount + igv;
  dsct = dsct.toFixed(2);
  igv = igv.toFixed(2);
  total = total.toFixed(2);
  $(".pod").text(dsct);
  $(".poi").text(igv);
  $(".pot").text(total);
  getAmountLiteral();
};

addDetailsPurchase = function(event) {
  var $tb, $td, data, temp;
  data = new Object;
  data.desc = $.trim($("input[name=podd").val());
  data.unit = $("select[name=podu]").find("option:selected").text();
  data.date = $("input[name=podf]").val();
  data.quantity = convertNumber($("input[name=podq]").val());
  data.price = convertNumber($("input[name=podp]").val());
  data.amount = data.quantity * data.price;
  if (data.desc !== "" && !isNaN(data.price) && !isNaN(data.quantity)) {
    if ($.trim($("input[name=podedit]").val()) !== "") {
      $td = $("tr.pod" + ($.trim($("input[name=podedit]").val())) + " > td");
      $td.eq(1).text($("input[name=podd").val());
      $td.eq(2).text($("select[name=podu]").val());
      $td.eq(3).text($("input[name=podf]").val());
      $td.eq(4).text($("input[name=podq]").val());
      $td.eq(5).text($("input[name=podp]").val());
      $td.eq(6).text(parseFloat($("input[name=podq]").val()) * parseFloat($("input[name=podp]").val()));
      $("input[name=podedit]").val("");
    } else {
      $tb = $(".table-details-purchase-order > tbody");
      temp = "<tr class=\"pod{{ item }}\"> <td>{{ item }}</td> <td>{{ desc }}</td> <td>{{ unit }}</td> <td>{{ date }}</td> <td>{{ quantity }}</td> <td>{{ price }}</td> <td>{{ amount }}</td> <td class=\"text-center\"> <button class=\"btn btn-link btn-xs text-primary btn-edit-pod\" value=\"{{ item }}\"> <span class=\"glyphicon glyphicon-edit\"></span> </button> </td> <td class=\"text-center\"> <button class=\"btn btn-link btn-xs text-red btn-del-pod\" value=\"{{ item }}\"> <span class=\"glyphicon glyphicon-trash\"></span> </button> </td> </tr>";
      data.item = $tb.find("tr").length + 1;
      $tb.append(Mustache.render(temp, data));
    }
    calAmountPurchaseOrder();
    $(".btn-details-purchare-order-toggle").click();
  } else {
    $().toastmessage("showWarningToast", "Existen campos vacios!");
  }
};

getPercentIVA = function(event) {
  var data, date;
  data = new Object;
  data.percentigv = true;
  date = $.trim($("input[name=podt]").val());
  if (date !== "") {
    data.year = new Date(date + " 00:00").getFullYear();
  }
  $.getJSON("/json/general/conf/igv/", data, function(response) {
    if (response.status) {
      $(".povigv").text(response.igv + "%");
    }
  });
};

getAmountLiteral = function(event) {
  var data;
  data = new Object;
  data.number = $(".pot").text();
  $.getJSON("/json/convert/number/to/literal/", data, function(response) {
    if (response.status) {
      $(".literal-amount").text("SON: " + response.literal + " /100 " + ($("select[name=pocu]").find("option:selected").text()));
    }
  });
};

showEditDetailsPurchase = function(event) {
  var $td;
  $("input[name=podedit]").val(this.value);
  $td = $("tr.pod" + this.value + " > td");
  $("input[name=podd").val($td.eq(1).text());
  $("select[name=podu]").val($td.eq(2).text());
  $("input[name=podf]").val($td.eq(3).text());
  $("input[name=podq]").val($td.eq(4).text());
  $("input[name=podp]").val($td.eq(5).text());
  $(".btn-details-purchare-order-toggle").click();
};

deleteDetailsPurchase = function(event) {
  var $tr;
  $tr = $("tr.pod" + this.value);
  $tr.remove();
  $(".table-details-purchase-order > tbody > tr").each(function(index, element) {
    var $td;
    $td = $(element).find("td");
    $td.eq(0).text(index + 1);
    $td.eq(7).find("button").val(index + 1);
    $td.eq(8).find("button").val(index + 1);
  });
  calAmountPurchaseOrder();
};

savePurchaseOrder = function(event) {
  var data, details;
  data = new FormData;
  data.append("savedPurchase", true);
  data.append("nropurchase", $.trim($("input[name=pond]").val()));
  data.append("issued", $.trim($("input[name=podt]").val()));
  data.append("currency", $("select[name=pocu]").val());
  data.append("document", $("select[name=podc]").val());
  data.append("method", $("select[name=popy]").val());
  if ($("input.upfile").get(0).files.length) {
    data.append("order", $("input.upfile").get(0).files[0]);
  }
  data.append("observation", $("textarea[name=obser]").val());
  data.append("dsct", parseFloat($("input[name=poids]").val()));
  data.append("igv", parseFloat($(".povigv").text().split("%")[0]));
  if ($.trim($("input[name=editpurchse]").val()) !== "") {
    data.append("editpurchse", $.trim($("input[name=editpurchse]").val()));
  }
  details = new Array;
  $(".table-details-purchase-order > tbody > tr").each(function(index, element) {
    var $td;
    $td = $(element).find("td");
    details.push({
      "description": $td.eq(1).text(),
      "unit": $td.eq(2).text(),
      "date": $td.eq(3).text(),
      "quantity": parseFloat($td.eq(4).text()),
      "price": parseFloat($td.eq(5).text())
    });
  });
  data.append("details", JSON.stringify(details));
  data.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());
  $.ajax({
    url: "",
    data: data,
    type: "POST",
    dataType: "json",
    cache: false,
    processData: false,
    contentType: false,
    success: function(response) {
      if (response.status) {
        getListPurchaseOrder();
        $("input[name=editpurchse]").val("");
        return $("div.mpurchase").modal("hide");
      } else {
        return $().toastmessage("showWarningToast", "No se a podido Guardar la Orden de compra. " + response.raise);
      }
    }
  });
};

getListPurchaseOrder = function(event) {
  var data;
  data = new Object;
  data.listPurchase = true;
  $.getJSON("", data, function(response) {
    var $tb, temp, template, x;
    if (response.status) {
      template = "<tr> <td>{{ item }}</td> <td>{{ nro }}</td> <td>{{ issued }}</td> <td>{{ document }}</td> <td class=\"text-center\">{{!file}}</td> <td class=\"text-center\"> <button class=\"btn btn-link btn-xs text-primary btn-edit-purchase\" value=\"{{ id }}\"> <span class=\"glyphicon glyphicon-edit\"></span> </button> </td> <td class=\"text-center\"> <button class=\"btn btn-link btn-xs text-red btn-del-purchase\" value=\"{{ id }}\"> <span class=\"glyphicon glyphicon-trash\"></span> </button> </td> </tr>";
      $tb = $("table.tpurchase > tbody");
      $tb.empty();
      for (x in response.list) {
        if (response.list[x].order !== "") {
          temp = template.replace("{{!file}}", "<a href=\"/media/{{ order }}\" target=\"_blank\"><span class=\"glyphicon glyphicon-file\"></span></a>");
        } else {
          temp = template;
        }
        response.item = parseInt(x) + 1;
        $tb.append(Mustache.render(temp, response.list[x]));
      }
    } else {
      return $().toastmessage("showWarningToast", "Error list ordenes de compra. " + response.raise);
    }
  });
};

getEditPurchase = function(event) {
  var data;
  $("input[name=editpurchse]").val(this.value);
  data = new Object;
  data.editPurchase = true;
  data.pk = this.value;
  $.getJSON("", data, function(response) {
    var $tb, template, x;
    if (response.status) {
      $("input[name=pond]").val(response.nropurchase);
      $("input[name=podt]").val(response.issued);
      $("select[name=pocu]").val(response.currency);
      $("select[name=podc]").val(response.document);
      $("select[name=popy]").val(response.method);
      $("textarea[name=obser]").val(response.observation);
      $("input[name=poids]").val(response.dsct);
      $(".povigv").text(response.igv + "%");
      $tb = $(".table-details-purchase-order > tbody");
      template = "<tr class=\"pod{{ item }}\"> <td>{{ item }}</td> <td>{{ description }}</td> <td>{{ unit }}</td> <td>{{ delivery }}</td> <td>{{ quantity }}</td> <td>{{ price }}</td> <td>{{ amount }}</td> <td class=\"text-center\"> <button class=\"btn btn-link btn-xs text-primary btn-edit-pod\" value=\"{{ item }}\"> <span class=\"glyphicon glyphicon-edit\"></span> </button> </td> <td class=\"text-center\"> <button class=\"btn btn-link btn-xs text-red btn-del-pod\" value=\"{{ item }}\"> <span class=\"glyphicon glyphicon-trash\"></span> </button> </td> </tr>";
      $tb.empty();
      for (x in response.details) {
        response.details[x].item = parseInt(x) + 1;
        $tb.append(Mustache.render(template, response.details[x]));
      }
      calAmountPurchaseOrder();
      $("div.mpurchase").modal("show");
    } else {
      $().toastmessage("showWarningToast", "No se recupero los datos.");
    }
  });
};

deleteOrderPurchase = function(event) {
  var val;
  val = this.value;
  $().toastmessage("showToast", {
    text: "Realmente desea eliminar la Orden de Compra?",
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
        data.deletePurchase = true;
        data.pk = val;
        data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
        $.post("", data, function(response) {
          if (response.status) {
            getListPurchaseOrder();
          } else {
            $().toastmessage("showErrorToast", "No se a eliminado la Orden de Compra");
          }
        }, "json");
      }
    }
  });
};

genKeyConfirmationResponsible = function(event) {
  var $pro, data;
  data = new Object;
  $pro = $("input[name=pro]");
  data.genKeyConf = true;
  data.email = $("input[name=user-email]").val();
  data.code = $pro.val();
  data.desc = 'responsible';
  data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
  $.post("/json/post/key/confirm/", data, function(response) {
    var reason;
    if (response.status) {
      reason = $("input[name=companyname]").val();
      data = new Object;
      data.forsb = $("input[name=user-email]").val();
      data.issue = "Código de confirmación";
      data.body = "<p><span style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\" data-mce-style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\">Tu código de confirmación para asignar al responsable es: <strong>" + response.key + "</strong>. Ingresa este código en la casilla de verificacion para continuar.</span></p><p>Generado:&nbsp; " + ($("input[name=user-email]").attr("data-name")) + "</p><p>Proyecto:&nbsp; <strong>\"" + ($pro.attr("data-name")) + "\"</strong></p><p>Ejecutado por:&nbsp; <strong>\"" + reason + "\"</strong></p><p>Fecha y hora: " + (new Date().toString()) + "</p><p><span data-mce-style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\" style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\">Si no has realizado esta operación o tienes cualquier duda respecto código, puedes comunicarte con nosotros 01 371-0443.</span></p>";
      return $.ajax({
        url: "http://190.41.246.91:3000/mailer/",
        type: "GET",
        crossDomain: true,
        data: $.param(data),
        dataType: "jsonp",
        success: function(response) {
          if (response.status) {
            return $().toastmessage("showNoticeToast", "Se a enviado el código de confirmación.");
          } else {
            return $().toastmessage("showErrorToast", "No se podido enviar el correo.");
          }
        }
      });
    } else {
      return $().toastmessage("showErrorToast", "No se generado el token.");
    }
  }, "json");
};

genKeyConfirmationApproved = function(event) {
  var $pro, data;
  data = new Object;
  $pro = $("input[name=pro]");
  data.genKeyConf = true;
  data.code = $pro.val();
  data.desc = "approved";
  data.email = $("input[name=user-email]").val();
  data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
  $.post("/json/post/key/confirm/", data, function(response) {
    var reason;
    if (response.status) {
      reason = $("input[name=companyname]").val();
      data = new Object;
      data.forsb = $("input[name=user-email]").val();
      data.issue = "Código de confirmación";
      data.body = "<p><span style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\" data-mce-style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\">Tu código de confirmación para Aprobar el Proyecto es: <strong>" + response.key + "</strong>. Ingresa este código en la casilla de verificacion para continuar.</span></p><p>Generado:&nbsp; " + ($("input[name=user-email]").attr("data-name")) + "</p><p>Proyecto:&nbsp; <strong>\"" + ($pro.attr("data-name")) + "\"</strong></p><p>Ejecutado por:&nbsp; <strong>\"" + reason + "\"</strong></p><p>Fecha y hora: " + (new Date().toString()) + "</p><p><span data-mce-style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\" style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\">Si no has realizado esta operación o tienes cualquier duda respecto código, puedes comunicarte con nosotros 01 371-0443.</span></p>";
      return $.ajax({
        url: "http://190.41.246.91:3000/mailer/",
        type: "GET",
        crossDomain: true,
        data: $.param(data),
        dataType: "jsonp",
        success: function(response) {
          if (response.status) {
            return $().toastmessage("showNoticeToast", "Se a enviado el código de confirmación.");
          } else {
            return $().toastmessage("showErrorToast", "No se podido enviar el correo.");
          }
        }
      });
    } else {
      return $().toastmessage("showErrorToast", "No se generado el token.");
    }
  }, "json");
};

showLoadPrices = function(event) {
  $("input[name=fileprices]").click();
};

uploadLoadPrices = function(event) {
  var file, form;
  file = $("input[name=fileprices]").get(0);
  if (file.files.length) {
    form = new FormData();
    form.append("prices", file.files[0]);
    form.append("loadPrices", true);
    form.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());
    $.ajax({
      url: "",
      data: form,
      type: "POST",
      dataType: "json",
      cache: false,
      contentType: false,
      processData: false,
      success: function(response) {
        if (response.status) {
          $().toastmessage("showNoticeToast", "Se a cargado el archivo correctamente.");
          return $("#mlprices").modal("hide");
        } else {
          return $().toastmessage("showWarningToast", "No se a podido subir el archivo. " + response.raise);
        }
      }
    });
  } else {
    $().toastmessage("showWarningToast", "Debe de seleccionar por lo menos un archivo.");
  }
};

showGuideByProject = function(event) {
  var href, pro, sub;
  pro = $("input[name=pro]").val();
  sub = $("input[name=sub]").val();
  if (sub === "") {
    sub = "None";
  }
  href = "/sales/projects/guide/list/" + pro + "/" + sub + "/None/";
  location.href = href;
};

showLetter = function(event) {
  $("#letter").modal("show");
};

generateLetter = function(event) {
  var $from, $observation, $status, $to, context;
  $from = $("input[name=letter-from]");
  $to = $("input[name=letter-to]");
  $status = $("select[name=letter-status]");
  $observation = $("textarea[name=letter-observation]");
  if ($.trim($from.val()) === "") {
    $from.focus();
    $().toastmessage("showWarningToast", "El campo a quién se <q>envia</q> se encuentra vacio.");
    return false;
  }
  if ($.trim($to.val()) === "") {
    $to.focus();
    $().toastmessage("showWarningToast", "El campo <q>recibe</q> se encuentra vacio.");
    return false;
  }
  context = new Object;
  context.generateletter = true;
  context.froms = $from.val();
  context.fors = $to.val();
  context.status = $status.val();
  context.observation = $observation.val();
  context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
  $.post("", context, function(response) {
    if (response.status) {
      getListLetter();
      $().toastmessage("showSuccessToast", "Se agenerado la carta Nro " + response.code);
      setTimeout(function() {
        $("#letter").modal("hide");
      }, 2600);
    } else {
      $().toastmessage("showErrorToast", "Error\r\nNo se a generado la carta. " + response.raise);
    }
  }, "json");
};

getListLetter = function(event) {
  var context;
  context = new Object;
  context.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
  context.letterlist = true;
  $.getJSON("", context, function(response) {
    var $tb, template, tmp, x;
    if (response.status) {
      template = "<tr> <td class=\"text-center\">{{ item }}</td> <td class=\"text-center\">{{ letter }}</td> <td>{{ froms }}</td> <td>{{ fors }}</td> <td class=\"text-center\">{{ status }}</td> <td class=\"text-center\"> {{!files}} </td> <td class=\"text-center\"> <div class=\"btn-group\"> <button type=\"button\" data-toggle=\"dropdown\" aria-expanded=\"false\" class=\"btn btn-xs btn-link text-black btn dropdown-toggle\"> <span class=\"fa fa-wrench\"></span> <span class=\"caret\"></span> </button> <ul class=\"dropdown-menu\" role=\"menu\"> <li class=\"text-left\"><button class=\"btn btn-link text-black btn-xs btn-letter-show-edit\" value=\"{{ letter }}\" data-from=\"{{ froms }}\" data-to=\"{{ fors }}\" data-status=\"{{ status }}\" data-observation=\"{{ observation }}\"><span class=\"fa fa-edit\"></span> Editar</button></li> <li class=\"text-left\"><button class=\"btn btn-link text-black btn-xs btn-letter-anular\" value=\"{{ letter }}\"><span class=\"fa fa-times-circle\"></span> Anular</button></li> <li class=\"divider\"></li> <li class=\"text-left\"><button class=\"btn btn-link text-black btn-xs btn-letter-show-up\" value=\"{{ letter }}\"><span class=\"glyphicon glyphicon-upload\"></span> Subir Carta</button></li> <li class=\"text-left\"><button class=\"btn btn-link text-black btn-xs btn-letter-show-anx\" value=\"{{ letter }}\"><span class=\"glyphicon glyphicon-upload\"></span> Subir Anexos</button></li> <li class=\"divider\"></li> <li class=\"text-left\"><button class=\"btn btn-link text-black btn-xs btn-letter-show-details\" value=\"{{ letter }}\"><span class=\"glyphicon glyphicon-list\"></span> Lista de anexos</button></li> <li class=\"text-left\"> <button class=\"btn btn-xs btn-link text-black btn-letter-show-observation\" value=\"{{ observation }}\"> <span class=\"fa fa-list\"></span> Observación </button> </li> </ul> </div> </td> </tr>";
      $tb = $(".table-letter > tbody");
      $tb.empty();
      for (x in response.list) {
        tmp = template;
        if (response.list[x].file.length) {
          tmp = tmp.replace("{{!files}}", "<a href=\"/media/{{ file }}\" class=\"text-black\" target=\"_blank\" rel=\"next\"> <span class=\"fa fa-file-text\"></span> </a>");
        }
        response.list[x].item = parseInt(x) + 1;
        $tb.append(Mustache.render(tmp, response.list[x]));
      }
    } else {
      $().toastmessage("showErrorToast", "No se pudo recuperar la lista de cartas. " + response.raise);
    }
  });
};

uploadLetter = function(event) {
  var $file, context;
  $file = $("input[name=letter-file]");
  if ($file.get(0).files.length) {
    context = new FormData;
    context.append("id", this.value);
    context.append("letter", $file.get(0).files[0]);
    context.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());
    context.append("uploadLetter", true);
    $.ajax({
      data: context,
      url: "",
      type: "POST",
      dataType: "json",
      processData: false,
      contentType: false,
      cache: false,
      beforeSend: function(success) {
        $("#letter-upload").find(".panel").append("<div class=\"panel-body\"><span class=\"fa fa-spinner fa-pulse fa-spin\"></span> Cargando</div>");
      },
      success: function(response) {
        if (response.status) {
          $("#letter-upload").find(".panel-body").remove();
          $().toastmessage("showSuccessToast", "Se a cargado correctamente la carta.");
          getListLetter();
          $("#letter-upload").modal("hide");
        } else {
          $().toastmessage("showErrorToast", "No se a cargado la carta. " + response.raise);
        }
      }
    });
  } else {
    $().toastmessage("showWarningToast", "Debe de seleccionar un archivo para subir.");
  }
};

uploadLetterAnexo = function(event) {
  var $file, context, i, j, ref;
  $file = $("input[name=letter-anexos-file]");
  if ($file.get(0).files.length) {
    context = new FormData;
    context.append("id", this.value);
    for (i = j = 0, ref = $file.get(0).files.length; j < ref; i = j += 1) {
      context.append("anexo" + i, $file.get(0).files[i]);
    }
    context.append("csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val());
    context.append("len", $file.get(0).files.length);
    context.append("uploadLetterAnexo", true);
    $.ajax({
      data: context,
      url: "",
      type: "POST",
      dataType: "json",
      processData: false,
      contentType: false,
      cache: false,
      beforeSend: function(success) {
        $("#anexos-upload").find(".panel").append("<div class=\"panel-body\"><span class=\"fa fa-spinner fa-pulse fa-spin\"></span> Cargando</div>");
      },
      success: function(response) {
        if (response.status) {
          $("#anexos-upload").find(".panel-body").remove();
          $().toastmessage("showSuccessToast", "Se a cargado correctamente los anexos.");
          getListLetter();
          $("#anexos-upload").modal("hide");
        } else {
          $().toastmessage("showErrorToast", "No se a cargado los anexos. " + response.raise);
        }
      }
    });
  }
};

showLetterUpload = function(event) {
  $(".btn-letter-upload").val(this.value);
  $("#letter-upload").modal("show");
};

showLetterAnexosUpload = function(event) {
  $(".btn-upload-anexos").val(this.value);
  $("#anexos-upload").modal("show");
};

showLetterEdit = function(event) {
  $("[name=letter-from-edit]").val(this.getAttribute("data-from"));
  $("[name=letter-to-edit]").val(this.getAttribute("data-to"));
  $("[name=letter-status-edit]").val(this.getAttribute("data-status"));
  $("[name=letter-observation-edit]").val(this.getAttribute("data-observation"));
  $(".edit-letter").val(this.value);
  $("#letter-edit").modal("show");
};

LetterAnular = function(event) {
  var context;
  context = new Object;
  context.id = this.value;
  $().toastmessage("showToast", {
    text: "Realmente desea anular la carta " + this.value + "?",
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
      if (result === "Si") {
        context.AnnulerLetter = true;
        context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
        $.post("", context, function(response) {
          if (response.status) {
            $().toastmessage("showSuccessToast", "Se a anulado correctamente la carta " + context.id + ".");
            getListLetter();
          } else {
            $().toastmessage("showErrorToast", "Error al anular la carta. " + response.raise);
          }
        }, "json");
      }
    }
  });
};

editLetter = function(event) {
  var $from, $observation, $status, $to, context;
  $from = $("input[name=letter-from-edit]");
  $to = $("input[name=letter-to-edit]");
  $status = $("select[name=letter-status-edit]");
  $observation = $("textarea[name=letter-observation-edit]");
  if ($.trim($from.val()) === "") {
    $from.focus();
    $().toastmessage("showWarningToast", "El campo a quién se <q>envia</q> se encuentra vacio.");
    return false;
  }
  if ($.trim($to.val()) === "") {
    $to.focus();
    $().toastmessage("showWarningToast", "El campo <q>recibe</q> se encuentra vacio.");
    return false;
  }
  context = new Object;
  context.editLetter = true;
  context.letter_id = this.value;
  context.froms = $from.val();
  context.fors = $to.val();
  context.status = $status.val();
  context.observation = $observation.val();
  context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
  $.post("", context, function(response) {
    if (response.status) {
      getListLetter();
      $().toastmessage("showSuccessToast", "Se editado la carta Nro " + context.letter_id);
      setTimeout(function() {
        $("#letter-edit").modal("hide");
      }, 2600);
    } else {
      $().toastmessage("showErrorToast", "Error\r\nNo se a podido editar la carta. " + response.raise);
    }
  }, "json");
};

showLetterObservation = function(event) {
  $("#letter-observation").modal("show").find("small[name=letter-observation]").text(this.value);
};

showListAnexos = function(event) {
  var context;
  context = new Object;
  context.id = this.value;
  context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
  context.listAnexo = true;
  $.post("", context, function(response) {
    var $lt, template, x;
    if (response.status) {
      template = "<li class=\"list-group-item list-group-item-success\"> <span class=\"badge\"> <button class=\"btn btn-xs btn-link text-white\"> <span class=\"fa fa-trash\"></span> </button> </span> <a href=\"/media/{{ file }}\" class=\"text-black\" target=\"_blank\">{{ name }}</a> </li>";
      $lt = $(".list-anexo");
      $lt.empty();
      for (x in response.list) {
        $lt.append(Mustache.render(template, response.list[x]));
      }
      $("#anexo-letter-list").modal("show");
    } else {
      $().toastmessage("showErrorToast", "No se a conseguido la lista de anexos.");
    }
  }, "json");
};

letterToggle = function(event) {
  var $btn;
  $btn = $(this);
  $(".panel-letter").find(".table-letter").toggle(function() {
    if (this.style.display === "table") {
      return $btn.find("span").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
    } else {
      return $btn.find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
    }
  });
};

toggleInfoClose = function(event) {
  var $block, $btn;
  $btn = $(this);
  $block = $(".step-" + this.value);
  if ($block.is(":visible")) {
    $block.css("display", "none");
    $btn.find("span").removeClass("fa-angle-double-up").addClass("fa-angle-double-down");
  } else {
    $block.css("display", "block");
    $btn.find("span").removeClass("fa-angle-double-down").addClass("fa-angle-double-up");
  }
};

closeStorage = function(event) {
  $().toastmessage("showToast", {
    text: "Realmente desea cerrar el almacén?",
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
      var context;
      if (result === "Si") {
        context = new Object;
        context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
        context.closeStorage = true;
        $.post("", context, function(response) {
          if (response.status) {
            $().toastmessage("showSuccessToast", "Se a cerrado el almacén correctamente.");
            $(".progress-project > div.circle:nth-of-type(1)").addClass("done");
            $(".progress-project > span.bar:nth-of-type(1)").addClass("active");
            setTimeout(function() {
              location.reload();
            }, 2600);
          } else {
            $().toastmessage("showErrorToast", "Error no se a podido cerrar el almacén. " + response.raise);
          }
        }, "json");
      }
    }
  });
};

uploadLetterDelivery = function(event) {
  var $file, context;
  context = new FormData;
  context.append("csrfmiddlewaretoken", $("[name=csrfmiddlewaretoken]").val());
  $file = $("[name=letterdelivery]").get(0);
  if ($file.files.length) {
    context.append("letter", $file.files[0]);
    context.append("letterdelivery", true);
  } else {
    $().toastmessage("showWarningToast", "No se a encontrado un archivo para subir al proyecto");
    return false;
  }
  $.ajax({
    data: context,
    type: "POST",
    dataType: "json",
    contentType: false,
    processData: false,
    cache: false,
    success: function(response) {
      if (response.status) {
        $().toastmessage("showSuccessToast", "Se subio la carta de entrega correctamente.");
        $(".progress-project > div.circle:nth-of-type(2)").addClass("done");
        $(".progress-project > span.bar:nth-of-type(2)").addClass("active");
        setTimeout(function() {
          location.reload();
        }, 2600);
      } else {
        $().toastmessage("showErrorToast", "Error al subir Carta de entrega. " + response.raise);
      }
    }
  });
};

loadDocumentsClosure = function(event) {
  var $doc, data, i, j, ref;
  $doc = $("[name=documentsclosure]").get(0).files;
  if ($doc.length) {
    data = new FormData;
    if ($doc.length > 1) {
      for (i = j = 0, ref = $doc.length; j < ref; i = j += 1) {
        data.append("documents" + i, $doc[i]);
      }
      data.append("totalFiles", $doc.length);
    } else {
      data.append("documents", $doc[0]);
    }
    data.append("csrfmiddlewaretoken", $("[name=csrfmiddlewaretoken]").val());
    data.append("documentsCloser", true);
    $.ajax({
      data: data,
      dataType: "json",
      type: "POST",
      url: "",
      contentType: false,
      processData: false,
      cache: false,
      success: function(response) {
        if (response.status) {
          $().toastmessage("showSuccessToast", "Se subio los documentos correctamente.");
          $(".progress-project > div.circle:nth-of-type(3)").addClass("done");
          $(".progress-project > span.bar:nth-of-type(3)").addClass("active");
          return setTimeout(function() {
            location.reload();
          }, 2600);
        } else {
          $().toastmessage("showErrorToast", "No se a podido cargar el/los archivo(s). " + response.raise);
        }
      }
    });
  } else {
    $().toastmessage("showWarningToast", "No se han encontrado archivos para subir.");
  }
};

loadCloseAccounting = function(event) {
  var $file, data, invoice, iva, otherin, otherout, retention;
  data = new FormData;
  invoice = $("[name=closureamount]").val();
  iva = $("[name=closureiva]").val();
  otherin = $("[name=closureother]").val();
  otherout = $("[name=closureout]").val();
  retention = $("[name=closureretention]").val();
  if ((invoice == null) || parseInt(invoice) < 0) {
    invoice = 0;
  }
  if ((iva == null) || parseInt(iva) < 0) {
    iva = 0;
  }
  if ((otherin == null) || parseInt(otherin) < 0) {
    otherin = 0;
  }
  if ((otherout == null) || parseInt(otherout) < 0) {
    otherout = 0;
  }
  if ((retention == null) || parseInt(retention) < 0) {
    retention = 0;
  }
  data.append("tinvoice", invoice);
  data.append("tiva", iva);
  data.append("otherin", otherin);
  data.append("otherout", otherout);
  data.append("retention", retention);
  $file = $("[name=accountingfiles").get(0).files;
  data.append("csrfmiddlewaretoken", $("[name=csrfmiddlewaretoken]").val());
  if ($file.length) {
    data.append("fileaccounting", $file[0]);
  }
  data.append("saveAccounting", true);
  $.ajax({
    url: "",
    type: "POST",
    data: data,
    dataType: "json",
    cache: false,
    contentType: false,
    processData: false,
    success: function(response) {
      if (response.status) {
        $().toastmessage("showSuccessToast", "Se subio los documentos correctamente.");
        $(".progress-project > div.circle:nth-of-type(4)").addClass("done");
        $(".progress-project > span.bar:nth-of-type(4)").addClass("active");
        setTimeout(function() {
          location.reload();
        }, 2600);
      } else {
        $().toastmessage("showErrorToast", "Error al guardar los cambios de contabilidad. " + response.raise);
      }
    }
  });
};

genKeyConfirmationClosureProject = function(event) {
  var $pro, data;
  data = new Object;
  $pro = $("input[name=pro]");
  data.genKeyConfClose = true;
  data.code = $pro.val();
  data.desc = "approved";
  data.email = $("input[name=user-email]").val();
  data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
  $.post("", data, function(response) {
    var reason;
    if (response.status) {
      reason = $("input[name=companyname]").val();
      data = new Object;
      data.forsb = $("input[name=user-email]").val();
      data.issue = "Código de confirmación";
      data.body = "<p><span style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\" data-mce-style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\">Tu código de confirmación para Aprobar el cierre de; Proyecto es: <strong>" + response.key + "</strong>. Ingresa este código en la casilla de verificacion para continuar.</span></p><p>Generado:&nbsp; " + ($("input[name=user-email]").attr("data-name")) + "</p><p>Proyecto:&nbsp; <strong>\"" + ($pro.attr("data-name")) + "\"</strong></p><p>Ejecutado por:&nbsp; <strong>\"" + reason + "\"</strong></p><p>Fecha y hora: " + (new Date().toString()) + "</p><p><span data-mce-style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\" style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\">Si no has realizado esta operación o tienes cualquier duda respecto código, puedes comunicarte con nosotros 01 371-0443.</span></p>";
      return $.ajax({
        url: "http://190.41.246.91:3000/mailer/",
        type: "GET",
        crossDomain: true,
        data: $.param(data),
        dataType: "jsonp",
        success: function(response) {
          if (response.status) {
            return $().toastmessage("showNoticeToast", "Se a enviado el código de confirmación.");
          } else {
            return $().toastmessage("showErrorToast", "No se podido enviar el correo.");
          }
        }
      });
    } else {
      return $().toastmessage("showErrorToast", "No se generado el token.");
    }
  }, "json");
};

closureProject = function(event) {
  $().toastmessage("showToast", {
    text: "Realmente desea Cerrar el Proyecto?",
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
        data.closureproject = true;
        data.keycon = $("[name=keyclosure]").val();
        $.post("", data, function(response) {
          if (response.status) {
            $(".progress-project > div.circle:nth-of-type(5)").addClass("done");
            $().toastmessage("showSuccessToast", "El Proyecto se a cerrado correctamente.");
            setTimeout(function() {
              return location.href = "/sales/projects/";
            }, 3000);
          } else {
            $().toastmessage("showErrorToast", "No se a podido cerrar el prouyecto. " + response.raise);
          }
        });
      }
    }
  });
};
