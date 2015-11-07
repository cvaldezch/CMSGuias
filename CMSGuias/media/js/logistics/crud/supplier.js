var getDataRUC;

$(document).ready(function() {
  $("input,select").attr("class", "form-control input-sm");
  $("select[name=pais]").on("click", getDepartamentOption);
  $("select[name=departamento]").on("click", getProvinceOption);
  $("select[name=provincia]").on("click", getDistrictOption);
  $("button.btn-search").on("click", getDataRUC);
  setTimeout(function() {
    return $("input[name=proveedor_id]").keyup(function(event) {
      if (this.value.length === 11) {
        getDataRUC();
      }
    });
  }, 1500);
  if ($(".alert-success").is(":visible")) {
    setTimeout(function() {
      window.close();
    }, 2600);
  }
});

getDataRUC = function() {
  var data, ruc;
  ruc = $("input[name=proveedor_id]").val();
  if (ruc.length === 11) {
    data = new Object();
    data.ruc = ruc;
    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
    $.post("/json/restful/data/ruc/", data, function(response) {
      console.log(response);
      if (response.status) {
        $("input[name=razonsocial]").val(response.reason);
        $("input[name=direccion]").val(response.address);
        return $("input[name=telefono]").val(response.phone);
      } else {
        return $().toastmessage("showWarningToast", "No se a encontrado el Proveedor.");
      }
    }, "json");
    return;
  } else {
    $().toastmessage("showWarningToast", "El numero de ruc es invalido!");
  }
};
