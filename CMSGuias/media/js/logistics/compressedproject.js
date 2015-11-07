var changeSelect, createTmpPurchase, createTmpQuatation, getListCheck;

$(document).ready(function() {
  $("input[name=select]").on("change", changeSelect);
  $("button.btn-quotation").on("click", createTmpQuatation);
  $("button.btn-purchase").on("click", createTmpPurchase);
  $("table.table-float").floatThead({
    useAbsolutePositioning: false,
    scrollingTop: 50
  });
});

changeSelect = function(event) {
  var radio;
  radio = this;
  if (this.checked) {
    $("input[name=materials]").each(function(index, element) {
      element.checked = Boolean(parseInt(radio.value));
    });
  }
};

getListCheck = function(event) {
  var data;
  data = new Array;
  $("input[name=materials]").each(function(index, element) {
    if (element.checked) {
      data.push({
        "materials": element.getAttribute("data-materials"),
        "quantity": element.value,
        "remainder": element.getAttribute("data-remainder"),
        "brand": element.getAttribute("data-brand"),
        "model": element.getAttribute("data-model")
      });
    }
  });
  return data;
};

createTmpQuatation = function(event) {
  var data;
  data = new Object;
  data.details = getListCheck();
  setTimeout(function() {
    if (data.details.length) {
      $().toastmessage("showToast", {
        text: "Desea generar el temporal para la cotización?",
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
            data.quote = true;
            data.details = JSON.stringify(data.details);
            data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
            $.post("", data, function(response) {
              if (response.status) {
                $().toastmessage("showNoticeToast", "se a generado el tmp de cotización.");
                setTimeout(function() {
                  var href;
                  href = "/logistics/quote/single/";
                }, 2600);
              } else {
                $().toastmessage("showErrorToast", "No se podido crear temp para la cotización.");
              }
            });
          }
        }
      });
    } else {
      $().toastmessage("showWarningToast", "No se han encontrado materiales para cotizar.");
    }
  }, 300);
};

createTmpPurchase = function(event) {
  var data;
  data = new Object;
  data.details = getListCheck();
  setTimeout(function() {
    if (data.details.length) {
      $().toastmessage("showToast", {
        text: "Desea generar el temporal para la orden de compra?",
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
            data.purchase = true;
            data.details = JSON.stringify(data.details);
            data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
            $.post("", data, function(response) {
              if (response.status) {
                $().toastmessage("showNoticeToast", "se a generado el tmp de la orden de compra.");
                setTimeout(function() {
                  var href;
                  href = "/logistics/purchase/single/";
                }, 2600);
              } else {
                $().toastmessage("showErrorToast", "No se podido crear temp para la compra.");
              }
            });
          }
        }
      });
    } else {
      $().toastmessage("showWarningToast", "No se han encontrado materiales para Comprar.");
    }
  }, 300);
};
