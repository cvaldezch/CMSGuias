var clearEdit, delAnalysis, editAnalysis, openGroup, openUnit, saveAnalysis, searchAnalysis, searchChange;

$(function() {
  $("[name=name]").restrictLength($("#pres-max-length"));
  $(".agroup").on("click", openGroup);
  $(".ounit").on("click", openUnit);
  $(".btn-saveAnalysis").on("click", saveAnalysis);
  $("[name=ssearch]").on("change", searchChange);
  $(".btn-search").on("click", searchAnalysis);
  $(document).on("click", ".bedit", editAnalysis);
  $(document).on("click", ".bdel", delAnalysis);
  $(".bedit, .bdel").css("cursor", "pointer");
  $(".analysisClose").on("click", clearEdit);
  $('select').material_select();
  $('.dropdown-button').dropdown({
    constrain_width: 200
  });
  $('.modal-trigger').leanModal();
  $(".modal.bottom-sheet").css("max-height", "60%");
});

openGroup = function() {
  var interval, url, win;
  url = $(this).attr("data-href");
  win = window.open(url, "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600");
  interval = window.setInterval(function() {
    var data;
    if ((win == null) || win.closed) {
      window.clearInterval(interval);
      data = new Object();
      data.list = true;
      $.getJSON("/sales/budget/analysis/group/list/", data, function(response) {
        var $group;
        if (response.status) {
          $group = $("[name=group]");
          $group.empty();
          Mustache.tags = new Array("[[", "]]");
          $group.html(Mustache.render("[[#list]]<option value=[[agroup_id]]\">[[ name ]]</option>[[/list]]", response));
        }
      });
    }
  }, 1000);
  return win;
};

openUnit = function() {
  var interval, url, win;
  url = $(this).attr("data-href");
  win = window.open(url, "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600");
  interval = window.setInterval(function() {
    var data;
    if ((win == null) || win.closed) {
      window.clearInterval(interval);
      data = new Object();
      data.list = true;
      $.getJSON("/unit/list/", data, function(response) {
        var $group;
        if (response.status) {
          $group = $("[name=unit]");
          $group.empty();
          Mustache.tags = new Array("[[", "]]");
          $group.html(Mustache.render("[[#unit]]<option value=\"[[unidad_id]]\">[[ uninom ]]</option>[[/unit]]", response));
        }
      });
    }
  }, 1000);
  return win;
};

saveAnalysis = function(e) {
  var context;
  context = {};
  context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
  context.group = $("[name=group]").val();
  context.name = $("[name=name]").val();
  context.unit = $("[name=unit]").val();
  context.performance = $("[name=performance]").val();
  if ($("[name=edit]").val().length === 8) {
    context.edit = true;
    context.analysis_id = $("[name=edit]").val();
  } else {
    context.analysisnew = true;
  }
  $.post('', context, function(response) {
    console.log(response);
    if (response.status) {
      swal("Felicidades!", "Se guardaron los camnbios correctamente.", "success");
      clearEdit();
      setTimeout(function() {
        location.reload();
      }, 2600);
    } else {
      swal("Error", "Error al registrar analysis", "error");
    }
  }, "json");
};

e.preventDefault();

return;

searchAnalysis = function() {
  var context, count, rdo;
  rdo = "";
  context = new Object();
  $("[name=ssearch]").each(function() {
    if (this.checked) {
      rdo = this.value;
    }
  });
  if (rdo === "0") {
    context.code = $("[name=scode]").val();
  } else if (rdo === "1") {
    context.name = $("[name=sname]").val();
  } else {
    if (rdo === "2") {
      context.group = $("[name=sgroup]").val();
    }
  }
  context.list = true;
  count = 1;
  $.getJSON("", context, function(response) {
    var $tb, template;
    if (response.status) {
      response.index = function() {
        return count++;
      };
      template = "[[#analysis]]<tr><td>[[ index ]]</td><td>[[ code ]]</td><td>[[ name ]]</td><td>[[ unit ]]</td><td>[[ group ]]</td><td class=\"center-align\">[[ performance ]]</td><td>[[ total ]]</td><td><button class=\"dropdown-button btn yellow darken-2\" type=\"button\" data-activates=\"dropdown\"><i class=\"fa fa-gears\"></i></button><ul class=\"dropdown-content\" id=\"dropdown\"><li class=\"text-left\"><a role=\"menuitem\" tabindex=\"-1\" href=\"/sales/budget/analysis/group/details/[[code]]/\"><span class=\"fa fa-list-alt\"></span> Detalle</a></li><li class=\"text-left\"><a role=\"menuitem\" tabindex=\"-1\" class=\"bedit\" data-value=\"[[code]]\" data-group=\"[[group]]\" data-name=\"[[name]]\" data-unit=\"[[unit]]\" data-performance=\"[[performance]]\"><span class=\"fa fa-edit\"></span> Editar</a></li><li class=\"text-left\"><a role=\"menuitem\" tabindex=\"-1\" class=\"bdel\" data-value=\"[[analysis_id]]\"><span class=\"fa fa-trash\"></span> Eliminar</a></li></ul></td></tr>[[/analysis]]";
      $tb = $("table > tbody");
      $tb.empty();
      Mustache.tags = new Array("[[", "]]");
      $tb.html(Mustache.render(template, response));
      $('.dropdown-button').dropdown({
        constrain_width: 200
      });
    } else {
      swal("Alerta!", "Error al buscar. " + response.raise, "warning");
    }
  });
};

searchChange = function(event) {
  if (this.value === "0") {
    $("[name=scode]").attr("disabled", false);
    $("[name=sname]").attr("disabled", true);
    $("[name=sgroup]").attr("disabled", true);
  } else if (this.value === "1") {
    $("[name=scode]").attr("disabled", true);
    $("[name=sname]").attr("disabled", false);
    $("[name=sgroup]").attr("disabled", true);
  } else if (this.value === "2") {
    $("[name=scode]").attr("disabled", true);
    $("[name=sname]").attr("disabled", true);
    $("[name=sgroup]").attr("disabled", false);
  }
};

editAnalysis = function(event) {
  $("[name=group]").val(this.getAttribute("data-group"));
  $("[name=name]").val(this.getAttribute("data-name"));
  $("[name=unit]").val(this.getAttribute("data-unit"));
  $("[name=performance]").val(this.getAttribute("data-performance"));
  $("[name=edit]").val(this.getAttribute("data-value"));
  $("#manalysis").modal("show");
};

delAnalysis = function(event) {
  var btn;
  btn = this;
  swal({
    title: "Eliminar Analisis?",
    text: "Realmente desea eliminar el Analisis de Precio Unitario?",
    type: "warning",
    showCancelButton: true,
    confirmButtonColor: "#dd6b55",
    confirmButtonText: "Si, eliminar!",
    cancelButtonText: "No, Cancelar",
    closeOnConfirm: true,
    closeOnCancel: true
  }, function(isConfirm) {
    var context;
    if (isConfirm) {
      context = new Object;
      context.delAnalysis = true;
      context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val();
      context.analysis = btn.getAttribute("data-value");
      $.post("", context, function(response) {
        if (response.status) {
          location.reload();
        } else {
          swal("Error", "Error al eliminar el Anlisis de Precio", "warning");
        }
      });
    }
  });
};

clearEdit = function(event) {
  $("[name=name]").val("");
  $("[name=performance]").val("");
  $("[name=edit]").val("");
};
