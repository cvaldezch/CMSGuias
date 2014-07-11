// Generated by CoffeeScript 1.7.1
(function() {
  var addTmpQuote, deleteAll, deleteMaterial, editMaterial, keyCode, keyDescription, listTmpQuote, searchMaterial, showEdit, showMaterials, stepSecond, uploadReadFile;

  $(document).ready(function() {
    $(".panel-add,input[name=read],.step-second").hide();
    $("input[name=description]").on("keyup", keyDescription);
    $("input[name=description]").on("keypress", keyUpDescription);
    $("select[name=meter]").on("click", getSummaryMaterials);
    $("input[name=code]").on("keypress", keyCode);
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

  keyDescription = function(event) {
    var key;
    key = window.Event ? event.keyCode : event.which;
    if (key !== 13 && key !== 40 && key !== 38 && key !== 39 && key !== 37) {
      getDescription(this.value.toLowerCase());
    }
    if (key === 40 || key === 38 || key === 39 || key === 37) {
      moveTopBottom(key);
    }
  };

  keyCode = function(event) {
    var key;
    key = window.Event ? event.keyCode : event.which;
    if (key === 13) {
      return searchMaterialCode(this.value);
    }
  };

  searchMaterial = function(event) {
    var code, desc;
    desc = $("input[name=description]").val();
    code = $("input[name=code]").val();
    if (code.length === 15) {
      return searchMaterialCode(code);
    } else {
      return getDescription($.trim(desc).toLowerCase());
    }
  };

  addTmpQuote = function(event) {
    var code, data, quantity;
    data = new Object();
    code = $(".id-mat").html();
    quantity = $("input[name=cantidad]").val();
    if (code !== "") {
      if (quantity !== "") {
        data.materiales = code;
        data.cantidad = quantity;
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
        template = "<tr name=\"{{ id }}\"><td>{{ item }}</td><td>{{ materials_id }}</td><td>{{ matname }}</td><td>{{ matmeasure }}</td><td>{{ unit }}</td><td>{{ quantity }}</td><td><button class=\"btn btn-xs btn-link\" name=\"btn-edit\" value=\"{{ quantity }}\" data-id=\"{{ id }}\" data-mat=\"{{ materials_id }}\"><span class=\"glyphicon glyphicon-pencil\"></span></button></td><td><button class=\"btn btn-xs btn-link text-red\" name=\"btn-del\" value=\"{{ id }}\" data-mat=\"{{ materials_id }}\"><span class=\"glyphicon glyphicon-trash\"></span></button></td></tr>";
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
    $("input[name=ematid]").val($(this).attr("data-mat"));
    $("input[name=eidtmp]").val($(this).attr("data-id"));
    $("input[name=equantity]").val(this.value);
    $(".medit").modal("show");
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
      data.type = "edit";
      data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
      $.post("", data, function(response) {
        var $edit;
        if (response.status) {
          $edit = $("table.table-list > tbody > tr[name=" + ($id.val()) + "] > td");
          $edit.eq(5).html($quantity.val());
          $edit.eq(6).find("button").val($quantity.val());
          $("input[name=ematid]").val("");
          $("input[name=eidtmp]").val("");
          $("input[name=equantity]").val("");
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
        template = "<tr name=\"{{ id }}\"><td>{{ item }}</td><td><input type=\"checkbox\"></td><td>{{ materials_id }}</td><td>{{ matname }}</td><td>{{ matmeasure }}</td><td>{{ unit }}</td><td>{{ quantity }}</td></tr>";
        $tb = $("table.table-quote > tbody");
        $tb.empty();
        for (x in response.list) {
          response.list[x].item = parseInt(x) + 1;
          $tb.append(Mustache.render(template, response.list[x]));
        }
      } else {
        return $().toastmessage("showWarningToast", "No se a encontrado resultados. " + response.raise);
      }
    });
    $(".step-first").hide("blind", 600);
    $(".step-second").show("blind", 400);
  };

}).call(this);
