$(document).ready ->
    # block materials
    getMaterialsAll()
    getManPowerAll()
    $(".materialsadd, .addmanpower").hide()
    $("[name=materials], [name=measure], [name=manpower]").chosen
        width: "100%"
    $("[name=materials]").on "change", getmeasure
    $("[name=measure]").on "change", getsummary
    $(".bshowaddmat").on "click", showAddMaterial
    $(".bmrefresh").on "click", refreshMaterials
    $(".btnaddmat").on "click", addMaterials
    $(document).on "dblclick", ".editm", showEditMaterials
    $(document).on "click", ".btn-edit-materials", editMaterials
    $(document).on "change", ".edit-tmp-quantity, .edit-tmp-price", calcPartitalMaterial
    $(document).on "click", ".btn-del-materials", delMaterials
    $(".bdelmatall").on "click", delMaterialsAll
    $(".bshownewmat").on "click", openNewMaterial
    # block end
    # block manpower
    $(".bshowaddmp").on "click", showAddManPower
    $(".btnaddmp").on "click", addManPower
    $(".bmprefresh").on "click", refreshManPower
    $(".bdelmp").on "click", delManPowerAll
    $(document).on "dblclick", ".editmp", showEditManPower
    $(document).on "click", ".btn-edit-mp", editManPower
    $(document).on "click", ".btn-del-mp", delManPower
    $(".bshownewmp").on "click", openNewManPower
    # end block
    return

# block Materials
getMaterialsAll = (event) ->
    context = new Object()
    context.searchName = true
    context.name = ''
    $.getJSON "/materials/", context, (response) ->
        if response.status
            $op = $("[name=materials]")
            $op.empty()
            template = "{{#names}}<option value=\"{{ name }}\">{{ name }}</option>{{/names}}"
            $op.html Mustache.render template, response
            $op.trigger "chosen:updated"
            getmeasure()
    return

getmeasure = (event) ->
    context = new Object
    context.searchMeter = true
    context.name = $("[name=materials]").val()
    $.getJSON "/materials/", context, (response) ->
        if response.status
            $se = $("[name=measure]")
            $se.empty()
            $se.append "<option></option>"
            template = "{{#meter}} <option value=\"{{code}}\">{{measure}}</option> {{/meter}}"
            $se.html Mustache.render template, response
            $se.trigger "chosen:updated"
            setTimeout ->
                getsummary()
                return
            , 200
            return
    return

getsummary = (event) ->
    context = new Object
    context.scode= $("[name=measure]").val()
    context.summary = true
    if context.scode.length is 15
        $.getJSON "/materials/", context, (response) ->
            if response.status
                template = "<table class=\"table table-condensed font-11\"><tbody><tr><th>Código</th><td class=\"matid\">{{ summary.materials }}</td></tr><tr><th>Nombre</th><td>{{ summary.name }}</td></tr><tr><th>Media</th><td>{{ summary.measure }}</td></tr><tr><th>Unidad</th><td>{{ summary.unit }}</td></tr></tbody></table>"
                $s = $("[name=summary]")
                $s.empty()
                $s.html Mustache.render template, response
                $("[name=mprice]").val response.summary.price
                return
    else
        $().toastmessage "showWarningToast", "El código del material no es valido."
    return

showAddMaterial = (event) ->
    if $(".materialsadd").is(":visible")
        $(@).removeClass "btn-warning"
        .addClass "btn-default"
        $(".materialsadd").hide 800
    else
        $(@).removeClass "btn-default"
        .addClass "btn-warning"
        $(".materialsadd").show 800
    return

addMaterials = (event) ->
    context = new Object()
    context.materials = $(".matid").text()
    context.quantity = $("[name=mquantity]").val()
    context.price = $("[name=mprice]").val()
    if context.materials.length is 15
        if context.quantity isnt ""
            if context.price isnt ""
                context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
                context.addMaterials = true
                $.post "", context, (response) ->
                    if response.status
                        getListMaterials()
                        return
                    else
                        $().toastmessage "showErrorToast", "Error al guardar los cambios. #{response.raise}"
                        return
                , "json"
            else
                $().toastmessage "showWarningToast", "Precio invalido."
        else
            $().toastmessage "showWarningToast", "Cantidad invalida."
    else
        $().toastmessage "showWarningToast", "Código de material incorrecto."
    return

getListMaterials = (event) ->
    context = new Object
    context.listMaterials = true
    $.getJSON "", context, (response) ->
        if response.status
            $tbl = $(".tmaterials tbody")
            $tbl.empty()
            template = "{{#materials}}<tr data-edit=\"{{pk}}\"><td>{{index}}</td><td>{{code}}</td><td>{{name}}</td><td>{{unit}}</td><td>{{quantity}}</td><td>{{price}}</td><td>{{partial}}</td><td class=\"text-center\"><button class=\"btn btn-warning btn-xs btn-edit-materials\" value=\"{{ pk }}\" data-materials=\"{{ code }}\" disabled><span class=\"fa fa-edit\"></span></button></td><td class=\"text-center\"><button class=\"btn btn-danger btn-xs btn-del-materials\" value=\"{{ pk }}\" data-materials=\"{{ code }}\"><span class=\"fa fa-trash\"></span></button></td></tr>{{/materials}}"
            counter = 1
            response.index = ->
                return counter++
            $tbl.html Mustache.render template, response
            return
        else
            $().toastmessage "showErrorToast", "Error al Obtener la lista. #{response.raise}."
            return
    return

refreshMaterials = (event) ->
    getMaterialsAll()
    getListMaterials()
    return

openNewMaterial = (event) ->
    win = window.open "/materials/", "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600"
    interval = window.setInterval ->
        if win == null or win.closed
            window.clearInterval interval
            getMaterialsAll
            return
    , 1000
    return win

showEditMaterials = (event) ->
    if $(".edit-tmp-quantity").length
        $(".edit-tmp-quantity").parent("td").html $(".edit-tmp-quantity").val()
    if $(".edit-tmp-price").length
        $(".edit-tmp-price").parent("td").html $(".edit-tmp-price").val()
    $tr = $(@)
    $td = $tr.find "td"
    quantity = $td.eq(4).text()
    $(".btn-edit-materials").attr "disabled", true
    $td.eq(7).find("button").attr "disabled", false
    ###if quantity.indexOf "," then quantity=  quantity.replace ",", "."
    quantity = parseFloat quantity###
    price = $td.eq(5).text()
    $td.eq(4).html "<input type=\"text\" value=\"#{quantity}\" class=\"form-control input-sm col-2 edit-tmp-quantity\">"
    $td.eq(5).html "<input type=\"text\" value=\"#{price}\" class=\"form-control input-sm col-2 edit-tmp-price\">"
    return

editMaterials =  (event) ->
    context = new Object
    context.quantity = $(".edit-tmp-quantity").val()
    context.price = $(".edit-tmp-price").val()
    context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
    try
        if not context.quantity.match /^[+]?[0-9]+[\.[0-9]+]?/
            $().toastmessage "showWarningToast", "No se a ingreso un número, cantidad incorrecta."
            return false
        if not context.price.match /^[+]?[0-9]+[\.[0-9]+]?/
            $().toastmessage "showWarningToast", "No se a ingreso un número, precio incorrecto."
            return false
        context.editMaterials = true
        context.materials = @getAttribute "data-materials"
        context.id = @value
        $.post "", context, (response) ->
            if response.status
                $(".edit-tmp-quantity").parent("td").parent("tr").find("td").eq(7).find("button").attr "disabled", true
                $(".edit-tmp-quantity").parent("td").html $(".edit-tmp-quantity").val()
                $(".edit-tmp-price").parent("td").html $(".edit-tmp-price").val()
                return
            else
                $().toastmessage "showErrorToast", "No se a podido editar. #{response.raise}."
                return
        , "json"
    catch e
        $().toastmessage "showWarningToast", "No se habilito la edición."
    return

calcPartitalMaterial = (event) ->
    $tr = $(@).parent("td").parent("tr")
    quantity = $tr.find("td").eq(4).find("input").val()
    price = $tr.find("td").eq(5).find("input").val()
    if quantity.indexOf(",") is 1
        quantity = quantity.replace ",", "."
    if price.indexOf(",") is 1
        price = price.replace ",", "."
    quantity = parseFloat quantity
    price = parseFloat price
    $tr.find("td").eq(6).text (quantity * price).toFixed(2)
    return

delMaterials = (event) ->
    btn = @
    $().toastmessage "showToast",
        text: "Realmente deseas eliminar el material?"
        type: "confirm"
        sticky: true
        buttons: [{value:"Si"}, {value:"No"}]
        success: (result) ->
            if result is "Si"
                context = new Object
                context.materials = btn.getAttribute "data-materials"
                context.id = btn.value
                context.delMaterials = true
                context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
                $.post "", context, (response) ->
                    if response.status
                        $().toastmessage "showSuccessToast", "Se a eliminado el material."
                        getListMaterials()
                        return
                    else
                        $().toastmessage "showErrorToast", "No se a podido eliminar el material. #{response.raise}"
                        return
                return
    return

delMaterialsAll = (event) ->
    $().toastmessage "showToast",
        text: "Realmente deseas eliminar todo la lista de materiales?"
        type: "confirm"
        sticky: true
        buttons: [{value:"Si"}, {value:"No"}]
        success: (result) ->
            if result is "Si"
                context = new Object
                context.delMaterialsAll = true
                context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
                $.post "", context, (response) ->
                    if response.status
                        $().toastmessage "showSuccessToast", "Se a eliminado el material."
                        getListMaterials()
                        return
                    else
                        $().toastmessage "showErrorToast", "No se a podido eliminar el material. #{response.raise}"
                        return
                return
    return

# block Man power
getManPowerAll = (event) ->
    context = new Object
    context.listcbo = true
    $.getJSON "/manpower/list/cbo/", context, (response) ->
        if response.status
            $cm = $("[name=manpower]")
            $cm.empty()
            template = "{{#list}}<option value=\"{{cargo_id}}\">{{cargos}}</option>{{/list}}"
            $cm.html Mustache.render template, response
            $cm.trigger "chosen:updated"
        else
            $().toastmessage "showErrorToast", "Error al listar combo. #{response.raise}"
            return
    return

showAddManPower = (event) ->
    if $(".addmanpower").is ":visible"
        $(@).removeClass "btn-warning"
        .addClass "btn-default"
        $(".addmanpower").hide 800
    else
        $(@).removeClass "btn-default"
        .addClass "btn-warning"
        $(".addmanpower").show 800
    return

addManPower = (event) ->
    context = new Object
    context.addMan = true
    context.performance = $(".performance").text()
    context.manpower = $("[name=manpower]").val()
    context.gang = $("[name=mpgang]").val()
    context.price = $("[name=mpprice]").val()
    if context.manpower is ""
        $().toastmessage "showWarningToast", "Codigo para Mano de obra es incorrecto."
        return false
    if not context.gang.match /^[+]?[0-9]{1,3}[\.[0-9]{0,3}]?/
        $().toastmessage "showWarningToast", "Cuadrilla invalida."
        return false
    if not context.price.match /^[+]?[0-9]+[\.[0-9]{0,4}]?/
        $().toastmessage "showWarningToast", "El precio ingresado es incorrecto."
        return false
    context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
    $.post "", context, (response) ->
        if response.status
            listManPower()
        else
            $().toastmessage  "showErrorToast", "Error al agregar mano de poder. #{response.raise}"
            return
    , "json"
    return

listManPower = (event) ->
    context = new Object
    context.listManPower = true
    $.getJSON "", context, (response) ->
        if response.status
            $tb = $(".tmanpower > tbody")
            template = "{{#manpower}}<tr class=\"editmp\"><td>{{index}}</td><td>{{code}}</td><td>{{name}}</td><td>{{unit}}</td><td>{{gang}}</td><td>{{quantity}}</td><td>{{price}}</td><td>{{partial}}</td><td class=\"text-center\"><button class=\"btn btn-xs btn-warning btn-edit-mp\" value=\"{{ id }}\" data-mp=\"{{code}}\" disabled><span class=\"fa fa-edit\"></span></button></td><td class=\"text-center\"><button class=\"btn btn-danger btn-xs btn-del-mp\" value=\"{{ id }}\" data-mp=\"{{code}}\"><span class=\"fa fa-trash\"></span></button></td></tr>{{/manpower}}"
            $tb.empty()
            counter = 1
            response.index = ->
                return counter++
            $tb.html Mustache.render template, response
            return
        else
            $().toastmessage "showErrorToast", "No se obtenido resultados. #{response.raise}"
            return
    return

delManPowerAll = (event) ->
    $().toastmessage "showToast",
        text: "Realmente desea eliminar todo la lista de Mano de Obra?"
        type: "confirm",
        sticky: true,
        buttons: [{value:"Si"}, {value:"No"}],
        success: (result) ->
            if result is "Si"
                context = new Object
                context.delManPowerAll = true
                context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
                $.post "", context, (response) ->
                    if response.status
                        listManPower()
                        return
                    else
                        $().toastmessage "showErrorToast", "Error al eliminar toda la lista. #{response.raise}"
                        return
                , "json"
                return
    return

refreshManPower = (event) ->
    getManPowerAll()
    listManPower()
    return
# end block

showEditManPower = (event) ->
    if $(".edit-mp-gang").length
        $(".edit-mp-gang").parent("td").html $(".edit-mp-gang").val()
    if $(".edit-mp-price").length
        $(".edit-mp-price").parent("td").html $(".edit-mp-price").val()
    $tr = $(@)
    $td = $tr.find "td"
    gang = $td.eq(4).text()
    #$(".btn-edit-materials").attr "disabled", true
    $td.eq(8).find("button").attr "disabled", false
    price = $td.eq(6).text()
    $td.eq(4).html "<input type=\"text\" value=\"#{gang}\" class=\"form-control input-sm col-2 edit-mp-gang\">"
    $td.eq(6).html "<input type=\"text\" value=\"#{price}\" class=\"form-control input-sm col-2 edit-mp-price\">"
    return

editManPower = (event) ->
    context = new Object
    context.addMan = true
    context.gang = $(".edit-mp-gang").val()
    context.price = $(".edit-mp-price").val()
    context.performance = $(".performance").text()
    context.manpower = @getAttribute "data-mp"
    if not context.gang.match /^[+]?[0-9]{1,3}[\.[0-9]{0,3}]?/
        $().toastmessage "showWarningToast", "Cuadrilla invalida."
        return false
    if not context.price.match /^[+]?[0-9]+[\.[0-9]{0,4}]?/
        $().toastmessage "showWarningToast", "El precio ingresado es incorrecto."
        return false
    context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
    $.post "", context, (response) ->
        if response.status
            listManPower()
            return
        else
            $().toastmessage "showErrorToast", "Error al editar los campos. #{response.raise}"
            return
    , "json"
    return

delManPower = (event) ->
  btn = @
  $().toastmessage "showToast",
    text: "Realmente deseas eliminar la mano de Obra?"
    type: "confirm"
    sticky: true
    buttons: [{value:"Si"},{value:"No"}]
    success: (result) ->
      if result is "Si"
        context = new Object
        context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
        context.delMan = true
        context.manpower = btn.getAttribute "data-mp"
        $.post "", context, (response) ->
          if response.status
            listManPower()
            return
          else
            $().toastmessage "showErrorToast", "Error al eliminar la mano de obra. #{response.raise}"
            return
        , "json"
  return

openNewManPower = ->
    win = window.open "/manpower/add", "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600"
    interval = window.setInterval ->
        if win == null or win.closed
            window.clearInterval interval
            getManPowerAll()
            return
    , 1000
    return win

# block tools
getlistTools = (event) ->
  return
