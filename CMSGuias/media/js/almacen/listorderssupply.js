$(document).ready(function() {
  $( "ul.lst-orders" ).sortable({
      cursor: "move",
      connectWith: "ul",
      receive: function (event, ui) {
        name = $(this).attr('name');
        //vecOrders.push(ui.item[0].attributes[2].value);
        if (name == "supply") {
         vecOrders.push(ui.item[0].id); 
        }else if (name == "order") {
          vecOrders.splice(vecOrders.indexOf(ui.item[0].id), 1);
        };
        $("#"+ui.item[0].id).removeClass(name == "supply" ? "list-group-item-info" : "list-group-item-success").addClass(name == "supply" ? "list-group-item-success" : "list-group-item-info")
        getlistMaterials(vecOrders);
      }
    });
    $( ".lst-orders" ).disableSelection();
    $(document).on('click','.btn-addsu', showAddSupply);
    $(".btn-add-commit").on("click", saveMatSupply);
    $(".maddsupply").draggable({
      cursor: "move"
    });
});

// functions
var saveMatSupply = function (event) {
  event.preventDefault();
  // data validating
  var pass = false, data = new Object();
  $("[name=id-add],[name=cant-add]").each(function () {
    if (this.value == "") {
      $().toastmessage("showWarningToast","Se a encontrado un campo vacio.");
      pass = false;
    }else{
      data[this.name] = this.value;
      pass = true;
    };
  });
  if (pass) {
    data['csrfmiddlewaretoken'] = $("[name=csrfmiddlewaretoken]").val();
    data['add-ori'] = 'PE';
    data['orders'] = JSON.stringify(vecOrders);
    console.log(data);
    $.post("", data, function(response) {
      console.log(response);
      if (response.status) {
        $("[name="+data['id-add']+"]").attr("disabled",true);
        //110013040600003
        $(".maddsupply").modal("hide");
      };
    });
  };
}
var showAddSupply = function (event) {
  event.preventDefault();
  $("[name=id-add]").val(this.name);
  $("[name=cant-add]").val(this.value).attr("min",this.value);
  $(".maddsupply").modal("show");
}
var vecOrders = new Array();
var getlistMaterials = function (vec) {
  if (vec.length >= 0){
    $.getJSON("/json/get/list/orders/details/",{ 'orders': JSON.stringify(vec) }, function (response) {
      if (response.status) {
        var $tb = $(".data-mats > tbody");
        $tb.empty();
        var template = "<tr class='{{ status }}'><td>{{ item }}</td><td>{{ materiales_id }}</td><td>{{ matnom }}</td><td>{{ matmed }}</td><td>{{ unidad }}</td><td>{{ cantidad }}</td><td>{{ stock }}</td><td><button value='{{ cantidad }}' name='{{ materiales_id }}' class='btn btn-addsu btn-sx btn-block text-black btn-{{status}}'><span class='glyphicon glyphicon-shopping-cart'></span></button></td></tr>";
        for (var x in response.list) {
          response.list[x].item = (parseInt(x) + 1)
          response.list[x].status = response.list[x].stock <= 0 ? 'danger' : response.list[x].stock <= response.list[x].cantidad && response.list[x].stock > 0 ? 'warning' : 'success'
          $tb.append(Mustache.render(template, response.list[x]));
          response.list[x].tag ? $("button[name="+response.list[x].materiales_id+"]").attr('disabled', response.list[x].tag) : false
        };
    };
    });
  }else{
    $().toastmessage("showWarningToast","No hay pedidos para suministrar");
  };
}