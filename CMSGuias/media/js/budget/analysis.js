var clearEdit, delAnalysis, editAnalysis, openGroup, openUnit, saveAnalysis, searchAnalysis, searchChange;

$(function() {
  var showAnalysis;
  $("[name=name]").restrictLength($("#pres-max-length"));
  $(".showAnalysis").on("click", showAnalysis);
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
  $('.dropdown-button').dropdown();
  return;
  showAnalysis = function() {};
  $("#manalysis").modal("show");
});

openGroup = function() {
  var interval, url, win;
  url = $(this).attr("href");
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
  url = $(this).attr("href");
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

saveAnalysis = function(event) {
  $.validate({
    form: "#registration",
    errorMessagePosition: "top",
    onError: function() {
      return false;
    },
    onSuccess: function() {
      var context;
      event.preventDefault();
      context = new Object();
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
      $.post("", context, function(response) {
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
    }
  });
};

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
      template = "[[#analysis]]<tr><td>[[ index ]]</td><td>[[ code ]]</td><td>[[ name ]]</td><td>[[ unit ]]</td><td>[[ performance ]]</td><td>[[ group ]]</td><td><div class=\"dropdown\"><button class=\"btn btn-default dropdown-toggle btn-xs\" type=\"button\" data-toggle=\"dropdown\" aria-expanded=\"true\"><span class=\"caret\"></span></button><ul class=\"dropdown-menu\" role=\"menu\"><li role=\"presentation\"><a role=\"menuitem\" tabindex=\"-1\" href=\"#\">Detalle</a></li><li role=\"presentation\"><a role=\"menuitem\" tabindex=\"-1\" href=\"#\">Editar</a></li><li role=\"presentation\"><a role=\"menuitem\" tabindex=\"-1\" href=\"#\">Eliminar</a></li></ul></div></td></tr>[[/analysis]]";
      $tb = $("table > tbody");
      $tb.empty();
      Mustache.tags = new Array("[[", "]]");
      $tb.html(Mustache.render(template, response));
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
