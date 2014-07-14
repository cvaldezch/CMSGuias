$(document).ready ->
    # block search materials
    $(".panel-add,input[name=read],.step-second").hide()
    $("input[name=description]").on "keyup", keyDescription
    $("input[name=description]").on "keypress", keyUpDescription
    $("select[name=meter]").on "click", getSummaryMaterials
    $("input[name=code]").on "keypress", keyCode
    # endblock
    $("input[name=traslado]").datepicker minDate: "0", showAnim: "slide", dateFormat: "yy-mm-dd"
    $(".btn-search").on "click", searchMaterial
    $(".btn-list").on "click", listTmpQuote
    $(".btn-add").on "click", addTmpQuote
    $(document).on "click", "[name=btn-edit]", showEdit
    $("button[name=esave]").on "click", editMaterial
    $(document).on "click", "[name=btn-del]", deleteMaterial
    $(".btn-show-materials").on "click", showMaterials
    $(".btn-trash").on "click", deleteAll
    $(".btn-read").on "click", -> $(".mfile").modal "show"
    $(".show-input-file-temp").click ->
        $("input[name=read]").click()
    $("[name=btn-upload]").on "click", uploadReadFile
    $(".btn-quote").on "click", stepSecond
    $(".get-supplier").on "click", loadSupplier
    $(".get-store").on "click", loadStore
    $("textarea[name=obser]").on "focus", loadText
    $("[name=select]").on "change", changeRadio
    $(".btn-quotesupplier").on "click", saveQuote
    $(".btn-newquote").on "click", newQuote
    $(".btn-finish").on "click", finishTmp
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

searchMaterial = (event) ->
    desc = $("input[name=description]").val()
    code = $("input[name=code]").val()
    if code.length is 15
        searchMaterialCode code
    else
        getDescription $.trim(desc).toLowerCase()

addTmpQuote = (event) ->
    data = new Object()
    code = $(".id-mat").html()
    quantity = $("input[name=cantidad]").val()
    if code isnt ""
        if quantity isnt ""
            data.materiales = code
            data.cantidad = quantity
            data.type = "add"
            data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
            $.post "", data, (response) ->
                if response.status
                    listTmpQuote()
                else
                    $().toastmessage "showWarningToast", "El servidor no a podido agregar el material. #{response.raise}"
            , "json"
        else
            $().toastmessage "showWarningToast", "Agregar materiales Falló. Cantidad Null."
        return
    else
        $().toastmessage "showWarningToast", "Agregar materiales Falló. Código Null."
    return

listTmpQuote = (event) ->
    $.getJSON "", "type":"list", (response) ->
        if response.status
            template = "<tr name=\"{{ id }}\"><td>{{ item }}</td><td>{{ materials_id }}</td><td>{{ matname }}</td><td>{{ matmeasure }}</td><td>{{ unit }}</td><td>{{ quantity }}</td><td><button class=\"btn btn-xs btn-link\" name=\"btn-edit\" value=\"{{ quantity }}\" data-id=\"{{ id }}\" data-mat=\"{{ materials_id }}\"><span class=\"glyphicon glyphicon-pencil\"></span></button></td><td><button class=\"btn btn-xs btn-link text-red\" name=\"btn-del\" value=\"{{ id }}\" data-mat=\"{{ materials_id }}\"><span class=\"glyphicon glyphicon-trash\"></span></button></td></tr>"
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
    $(".medit").modal "show"
    return

editMaterial = (event) ->
    event.preventDefault()
    $id = $("input[name=eidtmp]")
    $mat = $("input[name=ematid]")
    $quantity = $("input[name=equantity]")
    if $quantity.val() isnt 0 and $quantity.val() > 0
        data = new Object()
        data.id = $id.val()
        data.materials_id = $mat.val()
        data.quantity = $quantity.val()
        data.type = "edit"
        data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
        $.post "", data, (response) ->
            if response.status
                $edit = $("table.table-list > tbody > tr[name=#{$id.val()}] > td")
                $edit.eq(5).html($quantity.val())
                $edit.eq(6).find("button").val($quantity.val())
                $("input[name=ematid]").val ""
                $("input[name=eidtmp]").val ""
                $("input[name=equantity]").val ""
                $(".medit").modal "hide"
                return
            else
                $().toastmessage "showWarningToast","No se a podido editar el material #{response.raise}"
        return
    else
        $().toastmessage "showWarningToast", "Error campo cantidad"
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
    inputfile = docu("read")
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
                    listTmpQuote()
                    $(btn).button "reset"
                    if response.list.length > 0
                        template = "<tr><td>{{ item }}</td><td>{{ name }}</td><td>{{ measure }}</td><td>{{ unit }}</td><td>{{ quantity }}</td></tr>"
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

stepSecond = ->
    $.getJSON "", "type":"list", (response) ->
        if response.status
            template = "<tr name=\"{{ id }}\"><td>{{ item }}</td><td><input type=\"checkbox\" name=\"chk\" value=\"{{ id }}\"></td><td>{{ materials_id }}</td><td>{{ matname }}</td><td>{{ matmeasure }}</td><td>{{ unit }}</td><td>{{ quantity }}</td></tr>"
            $tb = $("table.table-quote > tbody")
            $tb.empty()
            for x of response.list
                response.list[x].item = parseInt(x) + 1
                $tb.append Mustache.render template, response.list[x]
            return
        else
            $().toastmessage "showWarningToast", "No se a encontrado resultados. #{ response.raise }"
            return
    loadSupplier()
    loadStore()
    $(".step-first").hide "blind", 600
    $(".step-second").show "blind", 400
    return

loadSupplier = ->
    $.getJSON "/json/supplier/get/list/all/", (response) ->
        if response.status
            template = "<option value=\"{{ supplier_id }}\">{{ company }}</option>"
            $sel = $("select#proveedor")
            $sel.empty()
            for x of response.supplier
                $sel.append Mustache.render template, response.supplier[x]
            return
        return

loadStore = ->
    $.getJSON "/json/store/get/list/all/", (response) ->
        if response.status
            template = "<option value=\"{{ store_id }}\">{{ name }}</option>"
            $sel = $("select#almacen")
            $sel.empty()
            for x of response.store
                $sel.append Mustache.render template, response.store[x]
            return
        return

loadText = ->
    tinymce.init
        selector: "textarea[name=obser]"
        theme: "modern"
        menubar: false
        statusbar: false
        toolbar_items_size: "small"
        schema: "html5"
        toolbar: "undo redo | styleselect | bold italic"
    return

changeRadio = (event) ->
    $("input[name=select]").each ->
        radio = Boolean parseInt @.value
        if @checked
            $("[name=chk]").each ->
                @.checked = radio
                return
            return
    return

saveQuote = (event) ->
    check = $("input[name=multiple]")
    supplier = $("select[name=proveedor]")
    store = $("select[name=almacen]")
    transfer = $("input[name=traslado]")
    obser = $("#obser_ifr").contents().find("body").html()
    data = new Object()
    mats = new Array()
    if supplier.val() isnt "" and store.val() isnt "" and transfer.val() isnt ""
        if check.is(":checked")
            console.log "check"
            data.proveedor = supplier.val()
            data.quote = check.val()
            data.check = "old"
        else
            console.log "not checked"
            data.proveedor = supplier.val()
            data.almacen = store.val()
            data.traslado = transfer.val()
            data.obser = obser
            data.check = "new"
        data.type = "addQuote"
        data.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
        $("[name=chk]").each ->
            if @checked
                mats.push
                    "materials_id" : $(".table-quote > tbody > tr[name=#{@value}]").find("td").eq(2).html()
                    "quantity" : $(".table-quote > tbody > tr[name=#{@value}]").find("td").eq(6).html()
                return
        data.details = JSON.stringify mats
        if mats.length <= 0
            $().toastmessage "showWarningToast", "Formato incorrecto, Materiales no seleccionados."
            return false

        $.post "", data, (response) ->
            if response.status
                $().toastmessage "showNoticeToast", "Cotización generada #{response.quote}"
                check.val response.quote
                newQuote event
            else
                $().toastmessage "showWarningToast", "Guardar Cotización fallo. #{response.raise}"
        , "json"
        console.log data
        return
    else
        $().toastmessage "showWarningToast", "Formato incorrecto, Campos vacios."
    return

newQuote = (event) ->
    event.preventDefault()
    span = $(".btn-newquote").find "span"
    if span.eq(1).html() is "Nuevo"
        value = false
        span.eq(0).removeClass("glyphicon-file").addClass "glyphicon-remove"
        span.eq(1).html("Cancelar")
    else
        value = true
        span.eq(0).removeClass("glyphicon-remove").addClass "glyphicon-file"
        span.eq(1).html("Nuevo")
    $(".form-quote").find("select, input, button").each ->
        @disabled = value
        return
    $(".btn-quotesupplier").attr "disabled", value
    return

finishTmp = (event) ->
    event.preventDefault()
    $().toastmessage "showToast",
        sticky: true,
        text: "Desea Terminar con el temporal de la Cotización?",
        type: "confirm",
        buttons: [{value:"Si"},{value:"No"}],
        success: (result) ->
            if result is "Si"
                $.post "", type: "delall", "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(), (response) ->
                    if response.status
                        $().toastmessage "showNoticeToast", "Felicidades, la(s) cotizacion(es) se han generado.";
                        setTimeout ->
                            location.reload()
                        , 2600
                    else
                        $().toastmessage "showWarningToast", "No se a ponido finalizar el temportal. #{response.raise}"
                , "json"
                return
    return