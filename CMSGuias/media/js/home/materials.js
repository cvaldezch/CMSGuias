var addResultTable, delMaterial, editMaterials, saveMaterials, searchCode, searchDesc, showEditMaterials, showNewMaterials;

$(document).ready(function() {
  $(".panel-new").hide();
  $("button.btn-top-page").on("click", goTopPage);
  $("input[name=searchCode]").on("keyup", searchCode);
  $("input[name=searchDesc]").on("keyup", searchDesc);
  $(document).on("click", "button[name=btnedit]", showEditMaterials);
  $("button.btn-show-new").on("click", showNewMaterials);
  $("button.btn-save-material").on("click", saveMaterials);
  $("button.btn-save-edit").on("click", editMaterials);
  $(document).on("click", "button[name=btndel]", delMaterial);
  $('table').floatThead({
    useAbsolutePositioning: false,
    scrollingTop: 50
  });
});

searchCode = function(event) {
  var data, key;
  key = event.keyCode || event.which;
  if (key === 13) {
    data = new Object;
    data.searchCode = true;
    data.code = $.trim(this.value);
    $.getJSON("", data, function(response) {
      if (response.status) {
        return addResultTable(response);
      }
    });
  }
};

searchDesc = function(event) {
  var data, key;
  key = event.keyCode || event.which;
  if (key === 13) {
    data = new Object;
    data.searchDesc = true;
    data.desc = $.trim(this.value);
    $.getJSON("", data, function(response) {
      if (response.status) {
        return addResultTable(response);
      }
    });
  }
};

addResultTable = function(response) {
  var $tb, count, template;
  template = "{{#list}}<tr>\n<td class=\"text-center\">{{ index }}</td>\n<td class=\"text-center\">{{ materials }}</td>\n<td>{{ name }}</td>\n<td>{{ measure }}</td>\n<td class=\"text-center\">{{ unit }}</td>\n<td>{{ finished }}</td>\n{{#user}}\n<td>{{ area }}</td>\n<td class=\"text-center\">\n    <button value=\"{{ materials }}\" data-des=\"{{ name }}\" data-met=\"{{ measure }}\" data-unit=\"{{ unit }}\" data-acb=\"{{ finished }}\" data-area=\"{{ area }}\" class=\"btn btn-xs btn-link text-black\" name=\"btnedit\">\n        <span class=\"fa fa-edit\"></span>\n    </button>\n</td>\n<td class=\"text-center\">\n    <button class=\"btn btn-xs btn-link text-red\" name=\"btndel\" value=\"{{ materials }}\" data-name=\"{{ name }}\" data-measure=\"{{ measure }}\" >\n        <span class=\"fa fa-trash-o\"></span>\n    </button>\n</td>\n{{/user}}\n</tr>{{/list}}";
  $tb = $("table > tbody");
  $tb.empty();
  count = 1;
  response.index = function() {
    return count++;
  };
  $tb.html(Mustache.render(template, response));
};

showNewMaterials = function(event) {
  var $btn;
  $btn = $(this);
  $(".panel-new").toggle("slow", function() {
    if (this.style.display === 'block') {
      $btn.removeClass("btn-primary").addClass("btn-default").find("span").eq(0).removeClass("fa-plus").addClass("fa-times");
      $btn.find("span").eq(1).text("Cancelar");
    } else {
      $btn.removeClass("btn-default").addClass("btn-primary").find("span").eq(0).removeClass("fa-times").addClass("fa-plus");
      $btn.find("span").eq(1).text("Numero Material");
    }
    return $('table').floatThead('reflow');
  });
};

showEditMaterials = function(event) {
  $("button.btn-save-edit").val(this.value);
  $("input[name=ematnom]").val(this.getAttribute("data-des"));
  $("input[name=ematmed]").val(this.getAttribute("data-met"));
  $("input[name=eunidad]").val(this.getAttribute("data-unit"));
  $("input[name=ematacb]").val(this.getAttribute("data-acb"));
  $("input[name=ematare]").val(this.getAttribute("data-area"));
  $(".meditmat").modal("show");
};

saveMaterials = function(event) {
  var data;
  data = new Object;
  data.materiales_id = $("input[name=materials]").val();
  data.matnom = $("input[name=matnom]").val();
  data.matmed = $("input[name=matmed]").val();
  data.unidad = $("select[name=unidad]").val();
  data.matacb = $("input[name=matacb]").val();
  data.matare = $("input[name=matare]").val();
  if (data.materiales_id === "" && data.materiales_id.length < 15) {
    $().toastmessage("showWarningToast", "El Código de material no es correcto.");
    return false;
  }
  if (data.matnom === "") {
    $().toastmessage("showWarningToast", "Debe de ingresar una descripcion para el material.");
    return false;
  }
  if (data.matmed === "") {
    $().toastmessage("showWarningToast", "Debe de ingresar un diametro para el material.");
    return false;
  }
  if (data.unidad === "") {
    $().toastmessage("showWarningToast", "Debe de ingresar una unidad para el material.");
    return false;
  }
  data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
  data.exists = true;
  $.post("", data, function(exists) {
    if (!exists.status) {
      delete data.exists;
      data.saveMaterial = true;
      $.post("", data, function(response) {
        if (response.status) {
          $("input[name=searchCode]").val(data.materiales_id).trigger(jQuery.Event("keyup", {
            which: 13
          }));
          $("button.btn-show-new").trigger("click");
          $("input[name=materials]").val("");
          $("input[name=matnom]").val("");
          $("input[name=matmed]").val("");
          $("input[name=matacb]").val("");
          $("input[name=matare]").val("");
        }
      }, "json");
    } else {
      return $().toastmessage("showWarningToast", "El codigo de material que esta intentando ingresar ya existe!.");
    }
  }, "json");
};

editMaterials = function(event) {
  var data;
  data = new Object;
  data.materiales_id = this.value;
  data.matnom = $("input[name=ematnom]").val();
  data.matmed = $("input[name=ematmed]").val();
  data.unidad = $("select[name=eunidad]").val();
  data.matacb = $("input[name=ematacb]").val();
  data.matare = $("input[name=ematare]").val();
  if (data.materiales_id === "" && data.materiales_id.length < 15) {
    $().toastmessage("showWarningToast", "El Código de material no es correcto.");
    return false;
  }
  if (data.matnom === "") {
    $().toastmessage("showWarningToast", "Debe de ingresar una descripcion para el material.");
    return false;
  }
  if (data.matmed === "") {
    $().toastmessage("showWarningToast", "Debe de ingresar un diametro para el material.");
    return false;
  }
  if (data.unidad === "") {
    $().toastmessage("showWarningToast", "Debe de ingresar una unidad para el material.");
    return false;
  }
  data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
  data.saveMaterial = true;
  data.edit = true;
  $.post("", data, function(response) {
    if (response.status) {
      $("input[name=searchCode]").val(data.materiales_id).trigger(jQuery.Event("keyup", {
        which: 13
      }));
      $("input[name=ematnom]").val("");
      $("input[name=ematmed]").val("");
      $("input[name=ematacb]").val("");
      $("input[name=ematare]").val("");
      $(".meditmat").modal("hide");
    }
  }, "json");
};

delMaterial = function(event) {
  var btn;
  btn = this;
  $().toastmessage("showToast", {
    text: "Realmente desea Eliminar el material: " + (this.getAttribute("data-name")) + " " + (this.getAttribute("data-measure")),
    sticky: true,
    type: "confirm",
    buttons: [
      {
        value: 'Si'
      }, {
        value: 'No'
      }
    ],
    success: function(result) {
      var data;
      if (result === "Si") {
        data = new Object;
        data.materials = btn.value;
        data["delete"] = true;
        data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
        $.post("", data, function(response) {
          if (response.status) {
            return location.reload();
          }
        }, "json");
      }
    }
  });
};
