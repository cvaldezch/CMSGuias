
var mat = {}
var counter_materials_global = 0;
var getDescription = function (name) {
    $.getJSON("/json/get/materials/name/", {'nom': name }, function (response) {
        var template = "<li id='li{{ id }}' onClick=getidli(this);><a class='text-primary' onClick='selectMaterial(this);'>{{ matnom }}</a></li>";
        $opt = $(".matname-global");
        $opt.empty();
        var i = 0;
        for (var x in response.name) {
            response.name[x].id = i
            $opt.append(Mustache.render(template, response.name[x] ));
            i += 1
        };
        $(".matname-global").show();
        $("[name=description]").focus().after($(".matname-global"));
    });
}
var getidli = function (item) {
    $("[name=description]").val($("#"+item.id+" > a").text()).focus();
    $(".matname-global").hide();
    counter_materials_global = 0;
}
// selected material with click or enter
var selectMaterial = function (all) {
    $("[name=description]").val(all.innerHTML).focus();
    $(".matname-global").hide();
    counter_materials_global=0;
}
var keyUpDescription = function (event) {
    var key = (event.keyCode || event.which)
    if (key == 13) {
        if ($(".matname-global").is(':visible')) {
            $('[name=description]').val( $('.item-selected > a').text() );
            $('.matname-global').hide();
        }
        getMeters();
        counter_materials_global = 0;
    };
}
var getMeters = function () {
    var $nom = $("[name=description]");
    if ($nom.val() != "" ) {
        var template = "<option value='{{ matmed }}'>{{ matmed }}</option>";
        var data = { "matnom": $nom.val().trim() }
        $med = $("[name=meter]");
        $med.empty();
        $.getJSON("/json/get/meter/materials/", data, function (response) {
            for (var x in response.list) {
                $med.append(Mustache.render(template, response.list[x]));
            };
        });
    };
}
var getSummaryMaterials = function (event) {
    var $nom = $("[name=description]"), $med = $("[name=meter]");
    if ($nom.val().trim() != "" && $med.val() != "" ) {
        var template = "<tr><th>Codigo :</th><td class='id-mat'>{{materialesid}}</td></tr>"+
            "<tr><th>Descripción :</th><td>{{matnom}}</td></tr>"+
            "<tr><th>Medida :</th><td>{{matmed}}</td></tr>"+
            "<tr><th>Unidad :</th><td>{{unidad}}</td></tr>";
        var $tb = $(".tb-details > tbody");
        $tb.empty();
        var data = { "matnom": $nom.val(), "matmed": $med.val() }
        $.getJSON("/json/get/resumen/details/materiales/", data, function (response) {
            for (var x in response.list) {
                $tb.append(Mustache.render(template, response.list[x]));
            };
        });
    };
}
var moveTopBottom = function (key) {
    var code = key;
    var ul = document.getElementById('matname-global');
    if(code === 40){ //down
        if($('#matname-global li.item-selected').length == 0){ //Si no esta seleccionado nada
            $('#matname-global li:first').addClass('item-selected');
        }else{
            $('#matname-global li:first').addClass('item-selected');
        }
    }else if(code === 38){ //arriba
        $('#matname-global li.item-selected').removeClass('item-selected');
    }else if(code === 39){ //abajo
        var liSelected = $('#matname-global li.item-selected');
        if(liSelected.length === 1 && liSelected.next().length === 1){
            liSelected.removeClass('item-selected').next().addClass('item-selected');
            if (counter_materials_global > 9) {
                ul.scrollTop+=30;
            };
            counter_materials_global++;
        }
    }else if(code === 37){ //izquierda
        var liSelected = $('#matname-global li.item-selected');
        if(liSelected.length === 1 && liSelected.prev().length === 1){
            liSelected.removeClass('item-selected').prev().addClass ('item-selected');
            if (counter_materials_global > 9) {
                ul.scrollTop-=30;
            };
            counter_materials_global--;
        }
    }
}
// code
var searchMaterialCode = function (code) {
    var pass = false;
    if (code.length < 15 || code.length > 15) {
        $().toastmessage("showWarningToast", "Format Code Invalid!");
        pass = false;
    }else if(code.length == 15){
        pass = true;
    };
    if (pass) {
         var data = new Object();
         data['code'] = code;
         $.getJSON('/json/get/materials/code/', data, function(response) {
            mats = response;
            if (response.status) {
                //$("[name=description]").val(response.list.matnom);
                var $met = $("[name=meter]");
                $met.empty();
                $met.append(Mustache.render("<option value='{{ matmed }}'>{{ matmed }}</option>", response.list));
                $("[name=description]").val(response.list.matnom);
                var template = "<tr><th>Codigo :</th><td class='id-mat'>{{materialesid}}</td></tr>"+
                    "<tr><th>Descripción :</th><td>{{matnom}}</td></tr>"+
                    "<tr><th>Medida :</th><td>{{matmed}}</td></tr>"+
                    "<tr><th>Unidad :</th><td>{{unidad}}</td></tr>";
                var $tb = $(".tb-details > tbody");
                $tb.empty();
                $tb.append(Mustache.render(template, response.list));
            }else{
                $().toastmessage("showWarningToast","The material not found.");
            };
         });
    };
}