$(document).ready(function() {
  $( "ul.lst-orders" ).sortable({
      cursor: "move",
      connectWith: "ul",
      receive: function (event, ui) {
        console.log('receive');
        console.log($(this).attr('name'));
        //vecOrders.push(ui.item[0].attributes[2].value);
        if ($(this).attr('name') == "supply") {
         vecOrders.push(ui.item[0].id); 
         getlistMaterials(vecOrders);
        }else if ($(this).attr('name') == "order") {
          console.info(ui.item[0].id);
          vecOrders.splice(vecOrders.indexOf(ui.item[0].id), 1);
        };
      }
    });
    $( ".lst-orders" ).disableSelection();
});

// funtions
var vecOrders = new Array();
var getlistMaterials = function (vec) {
  if (vec.length > 0){
    console.log('enviando');
    $.getJSON("/json/get/list/orders/details/",{ 'mats': JSON.stringify(vec) }, function (response) {
      console.log(response);
    });
  }else{
    $().toastmessage("showWarningToast","No hay pedidos para suministrar");
  };
  //console.log(vec);
}