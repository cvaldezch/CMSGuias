$(document).ready ->
    # block search materials
    $(".panel-add,input[name=read],.step-second").hide()
    $("input[name=description]").on "keyup", keyDescription
    $("input[name=description]").on "keypress", keyUpDescription
    $("select[name=meter]").on "click", getSummaryMaterials
    $("input[name=code]").on "keypress", keyCode
    # endblock
    $("input[name=traslado]").datepicker minDate: "0", showAnim: "slide", dateFormat: "yy-mm-dd"
    $(".btn-show-materials").on "click", showMaterials
    $(".btn-search").on "click", searchMaterial
    $(".btn-list").on "click", listTmpBuy
    $(".btn-add").on "click", addTmpPurchase
    $(document).on "click", "[name=btn-edit]", showEdit
    $("button[name=esave]").on "click", editMaterial
    $(document).on "click", "[name=btn-del]", deleteMaterial
    $(".btn-trash").on "click", deleteAll
    $(".btn-read").on "click", -> $(".mfile").modal "show"
    $(".show-input-file-temp").click ->
        $("input[name=read]").click()
    $("[name=btn-upload]").on "click", uploadReadFile
    $(".show-bedside").on "click", showBedside
    $("input[name=discount],input[name=edist]").on "blur", blurRange
    listTmpBuy()
    return

showMaterials = (event) ->
    item = @
    $(".panel-add").toggle ->
        if $(@).is(":hidden")
            $(item).find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down")
        else
            $(item).find("span").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up")
    return

keyDescription = (event) ->
    key = `window.Event ? event.keyCode : event.which`
    if key isnt 13 and key isnt 40 and key isnt 38 and key isnt 39 and key isnt 37
        getDescription @value.toLowerCase()
    if key is 40 or key is 38 or key is 39 or key is 37
        moveTopBottom key
    return

keyCode = (event) ->
    key = if window.Event then event.keyCode else event.which
    if key is 13
        searchMaterialCode @value
    return

searchMaterial = (event) ->
    desc = $("input[name=description]").val()
    code = $("input[name=code]").val()
    if code.length is 15
        searchMaterialCode code
    else
        getDescription $.trim(desc).toLowerCase()

addTmpPurchase = (event) ->
    data = new Object()
    code = $(".id-mat").html()
    quantity = $("input[name=cantidad]").val()
    price = $("input[name=precio]").val()
    discount = parseInt $("input[name=discount]").val()
    if code isnt ""
        if quantity isnt ""
            if price isnt ""
                data.materiales = code
                data.cantidad = quantity
                data.precio = price
                data.discount = discount
                data.type = "add"
                data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
                $.post "", data, (response) ->
                    if response.status
                        listTmpBuy()
                    else
                        $().toastmessage "showWarningToast", "El servidor no a podido agregar el material, #{response.raise}."
                , "json"
            else
                $().toastmessage "showWarningToast", "Agregar materiales Falló. Precio Null."
        else
            $().toastmessage "showWarningToast", "Agregar materiales Falló. Cantidad Null."
        return
    else
        $().toastmessage "showWarningToast", "Agregar materiales Falló. Código Null."
    return

listTmpBuy = (event) ->
    $.getJSON "", "type":"list", (response) ->
        if response.status
            template = "<tr name=\"{{ id }}\"><td>{{ item }}</td><td>{{ materials_id }}</td><td>{{ matname }}</td><td>{{ matmeasure }}</td><td>{{ unit }}</td><td>{{ quantity }}</td><td>{{ price }}</td><td>{{ discount }}%</td><td>{{ amount }}</td><td><button class=\"btn btn-xs btn-link\" name=\"btn-edit\" value=\"{{ quantity }}\" data-price=\"{{ price }}\" data-id=\"{{ id }}\" data-mat=\"{{ materials_id }}\" data-discount=\"{{ discount }}\"><span class=\"glyphicon glyphicon-pencil\"></span></button></td><td><button class=\"btn btn-xs btn-link text-red\" name=\"btn-del\" value=\"{{ id }}\" data-mat=\"{{ materials_id }}\"><span class=\"glyphicon glyphicon-trash\"></span></button></td></tr>"
            $tb = $("table.table-list > tbody")
            $tb.empty()
            for x of response.list
                response.list[x].item = parseInt(x) + 1
                $tb.append Mustache.render template, response.list[x]
            return
        else
            $().toastmessage "showWarningToast", "No se a encontrado resultados. #{ response.raise }"
    return

showEdit = (event) ->
    event.preventDefault()
    $("input[name=ematid]").val $(@).attr "data-mat"
    $("input[name=eidtmp]").val $(@).attr "data-id"
    $("input[name=equantity]").val @value
    $("input[name=eprice]").val $(@).attr "data-price"
    $("input[name=edist]").val $(@).attr "data-discount"
    $(".medit").modal "show"
    return

editMaterial = (event) ->
    event.preventDefault()
    $id = $("input[name=eidtmp]")
    $mat = $("input[name=ematid]")
    $quantity = $("input[name=equantity]")
    $price = $("input[name=eprice]")
    $discount = $("input[name=edist]").val()
    if $quantity.val() isnt 0 and $quantity.val() > 0 and $price.val() isnt 0 and $price.val() > 0
        data = new Object()
        data.id = $id.val()
        data.materials_id = $mat.val()
        data.quantity = parseFloat $quantity.val()
        data.price = parseFloat $price.val()
        data.type = "edit"
        data.discount = parseFloat $discount
        data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
        $.post "", data, (response) ->
            if response.status
                ###$edit = $("table.table-list > tbody > tr[name=#{$id.val()}] > td")
                $edit.eq(5).html $quantity.val()
                $edit.eq(6).html $price.val()
                $edit.eq(7).html "#{$discount}%"
                $edit.eq(8).html (((data.price * data.discount) / 100) * data.quantity)
                $edit.eq(9).find("button").val $quantity.val()
                $edit.eq(9).find("button").attr "data-price", $price.val()
                $("input[name=ematid],input[name=eidtmp],input[name=equantity],input[name=eprice]").val ""
                ###
                $(".medit").modal "hide"
                listTmpBuy()
                return
            else
                $().toastmessage "showWarningToast","No se a podido editar el material #{response.raise}"
        return
    else
        $().toastmessage "showWarningToast", "Error campo vacio: cantidad, precio.  "
    return

deleteMaterial = (event) ->
    event.preventDefault()
    item = @
    $().toastmessage "showToast",
        sticky: true,
        text: "Desea eliminar el material #{$(@).attr "data-mat"}",
        type: "confirm",
        buttons: [{value:"Si"},{value:"No"}],
        success: (result) ->
            if result is "Si"
                data = new Object()
                data.id = item.value
                data.materials_id = $(item).attr "data-mat"
                data.type = "del"
                data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
                $.post "", data, (response) ->
                    if response.status
                        $("table.table-list > tbody > tr[name=#{item.value}]").remove()
                    else
                        $().toastmessage "showWarningToast", "Error al eliminar material #{response.raise}"
                , "json"
                return

deleteAll = (event) ->
    event.preventDefault()
    $().toastmessage "showToast",
        sticky: true,
        text: "Desea eliminar todo el temporal?",
        type: "confirm",
        buttons: [{value:"Si"},{value:"No"}],
        success: (result) ->
            if result is "Si"
                $.post "", type: "delall", "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(), (response) ->
                    if response.status
                        $().toastmessage "showNoticeToast", "Correcto se a eliminado todo el temporal.";
                        setTimeout ->
                            location.reload()
                        , 2600
                    else
                        $().toastmessage "showWarningToast", "No se a podido eliminar todo el temporal. #{response.raise}"
                , "json"
                return
    return

uploadReadFile = (event) ->
    event.preventDefault()
    btn = @
    inputfile = document.getElementsByName("read")
    file = inputfile[0].files[0]
    if file?
        data = new FormData()
        data.append "type", "read"
        data.append "archivo", file
        data.append "csrfmiddlewaretoken", $("[name=csrfmiddlewaretoken]").val()
        $.ajax
            url : ""
            type : "POST"
            data: data
            contentType : false
            processData : false
            cache : false
            beforeSend : ->
                $(btn).button "loading"
            success : (response) ->
                if response.status
                    listTmpBuy()
                    $(btn).button "reset"
                    if response.list.length > 0
                        template = "<tr><td>{{ item }}</td><td>{{ name }}</td><td>{{ measure }}</td><td>{{ unit }}</td><td>{{ quantity }}</td><td>{{ price }}</td></tr>"
                        $tb = $("table.table-nothing > tbody")
                        $tb.empty()
                        for x of response.list
                            response.list[x].item = (parseInt(x) + 1)
                            $tb.append Mustache.render template, response.list[x]

                        $(".mlist").modal "show"
                    $(".mfile").modal "hide"
                    return
                else
                    $().toastmessage "showWarningToast", "No se ha podido completar la transacción. #{response.raise}"
    else
        $().toastmessage "showWarningToast", "Seleccione un archivo para subir y ser leido."
    return

blurRange = ->
    # event.preventDefault()
    console.info "value #{@value}"
    console.info "max #{@getAttribute("max")}"
    if parseInt(@value) > parseInt(@getAttribute("max"))
        @value = parseInt @getAttribute "max"
    else if parseInt(@value) < parseInt(@getAttribute("min"))
        @value = parseInt @getAttribute "min"
    return

showBedside = ->
    $(".mpurchase").modal "toggle"
    return

saveOrderPurchase = ->

    return