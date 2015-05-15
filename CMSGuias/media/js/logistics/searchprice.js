var getPricesCode, keyuppress, listDetails, searchCode, searchName;

$(function() {
  $("[name=code], [name=name]").on("keyup", keyuppress);
  return $(document).on("click", ".bdetails", getPricesCode);
});

keyuppress = function(ev) {
  var key;
  key = window.ev ? ev.keyCode : ev.which;
  if (key === 13) {
    console.log(this.name);
    if (this.name === "code") {
      searchCode();
    } else {
      searchName();
    }
  }
};

searchCode = function(ev) {
  var context;
  context = new Object;
  context.code = $("[name=code]").val();
  context.searchCode = true;
  $.getJSON("", context, function(response) {
    if (response.status) {
      listDetails(response);
    } else {
      $().toastmessage("showErrorToast", "No se han encontrado resultados.");
    }
  });
};

searchName = function(ev) {
  var context;
  context = new Object;
  context.name = $("[name=name]").val();
  context.searchName = true;
  $.getJSON("", context, function(response) {
    if (response.status) {
      listDetails(response);
    } else {
      $().toastmessage("showErrorToast", "No se han encontrado resultados.");
    }
  });
};

listDetails = function(object) {
  var $tb, count, template;
  console.info(object);
  $tb = $(".tdetails > tbody");
  count = 1;
  object.index = function() {
    return count++;
  };
  template = "{{#details}}<tr><td>{{index}}</td><td>{{code}}</td><td>{{name}}</td><td>{{metering}}</td><td><button class=\"btn btn-xs btn-danger bdetails\" value=\"{{code}}\"><span class=\"fa fa-cogs\"></span></button></td></tr>{{/details}}";
  $tb.empty();
  $tb.html(Mustache.render(template, object));
};

getPricesCode = function(ev) {
  var parameter;
  parameter = new Object;
  parameter.prices = true;
  parameter.code = this.value;
  $.getJSON("", parameter, function(response) {
    var $tb, template;
    if (response.status) {
      $tb = $(".dprices");
      template = "<dl class=\"dl-horizontal\"><dt>Codigo</dt><dd>{{data.code}}</dd><dt>Nombre</dt><dd>{{data.name}} - {{data.metering}}</dd><dt>Unidad</dt><dd>{{data.unit}}<dd></dl><table class=\"table table-condensed table-hober\"><thead><tr><th>Proveedor</th><th>O.Compra</th><th>Moneda</th><th>Fecha</th><th>Precio</th></tr></thead><tbody>{{#prices}}<tr><td>{{supplier}}</td><td>{{purchase}}</td><td>{{currency}}</td><td>{{date}}</td><td>{{price}}</td></tr>{{/prices}}</tbody></table>";
      $tb.html(Mustache.render(template, response));
      $("#mprices").modal("show");
    } else {
      $().toastmessage("showErrorToast", "No se han obtenido los precios para este material. " + response.raise);
    }
  });
};
