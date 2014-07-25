$(document).ready ->
    # block search materials
    $(".panel-add,input[name=read],.step-second").hide()
    $("input[name=description]").on "keyup", keyDescription
    $("input[name=description]").on "keypress", keyUpDescription
    $("select[name=meter]").on "click", getSummaryMaterials
    $("input[name=code]").on "keypress", keyCode
    # endblock
    $(".panel-add-mat, .view-full").hide()
    $(".btn-show-mat").on "click", openAddMaterial
    $("input[name=plane]").on "change", uploadPlane
    $(".btn-show-planes").on "click", panelPlanes
    $("[name=show-full]").on "click", viewFull
    $("[name=plane-del]").on "click", delPlane
    $(".btn-add").on "click", addMaterial
    $("[name=show-plane]").on "click", (event) ->
        $("input[name=plane]").click()
    $(document).on "click", ".btn-del-mat", delMaterials
    $(".btn-save-edit").on "click", editMaterials
    $(document).on "click", ".btn-show-edit", ->
        $(".btn-save-edit").val @value
        $materials = $(".#{@value} > td")
        $(".text-edit").text "#{$materials.eq(2).text()} #{$materials.eq(3).text()}"
        $("input[name=edit-materials]").val $materials.eq(1).text()
        $("input[name=edit-quantity]").val $materials.eq(5).text()
        $("input[name=edit-price]").val $materials.eq(6).text()
        $(".medit").modal "toggle"
    return

# block get Materiales
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

# endBlock

openAddMaterial = (event) ->
    event.preventDefault()
    $(".panel-add-mat").toggle ->
        if $(".btn-show-mat").is(":hidden")
            $(@).find("span").removeClass "glyphicon-chevron-up"
            .addClass "glyphicon-chevron-down"
        else
            $(".btn-show-mat").find("span").removeClass "glyphicon-chevron-down"
            .addClass "glyphicon-chevron-up"
    return

uploadPlane = (event) ->
    console.log @files[0]
    if @files[0] isnt null
        data = new FormData()
        data.append("type", "plane")
        data.append("files", @files[0])
        data.append("proyecto", $("input[name=pro]").val())
        data.append("subproyecto", $("input[name=sub]").val())
        data.append("sector", $("input[name=sec]").val())
        data.append("csrfmiddlewaretoken", $("[name=csrfmiddlewaretoken]").val())
        $.ajax
            data : data,
            url : "",
            type : "POST",
            dataType : "json",
            cache : false,
            processData: false,
            contentType: false,
            success : (response) ->
                if response.status
                    location.reload()
                else
                    $().toastmessage "showErrorToast", "No se ha cargado un archivo."
    else
        $().toastmessage "showWarningToast", "No se ha cargado un archivo."
    return

panelPlanes = (event) ->
    btn = @
    $(".panel-planes > .panel-body").toggle ->
        if $(".panel-planes > .panel-body").is(":hidden")
            $(btn).find("span").removeClass "glyphicon-chevron-up"
            .addClass "glyphicon-chevron-down"
        else
            $(btn).find("span").removeClass "glyphicon-chevron-down"
            .addClass "glyphicon-chevron-up"
    return

viewFull = (event) ->
    btn = @
    $(".view-full").toggle ->
        if $(@).is(":hidden")
            $(".navbar").show "blind", 600
            return
        else
            $(".navbar").hide "blind", 600
            $("#planefull").attr "src", btn.value
            # $("#planefull").reload()
            return
    return

delPlane = (event) ->
    data = new Object()
    data.type = "delplane"
    data.files = @value
    data.pro = $("input[name=pro]").val()
    data.sub = $("input[name=sub]").val()
    data.sec = $("input[name=sec]").val()
    data.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
    $().toastmessage "showToast",
        "text" : "Desea eliminar el <q>Plano</q>?"
        "type" : "confirm"
        "sticky" : true
        buttons : [{value:'Si'},{value:'No'}]
        success : (result) ->
            if result is "Si"
                $.post "", data, (response) ->
                    if response.status
                        location.reload()
                    else
                        $().toastmessage "showWarningToast", "Error, al eliminar el plano."
    return

addMaterial = (event) ->
    data = new Object()
    data.proyecto = $("input[name=pro]").val()
    data.subproyecto = $("input[name=sub]").val()
    data.sector = $("input[name=sec]").val()
    data.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
    data.type = "add"
    data.materiales = $(".id-mat").text()
    data.cantidad = $("input[name=cantidad]").val()
    data.precio = $("input[name=precio]").val()
    if data.materiales != "" and data.cantidad != "" and data.precio != ""
        # if $(".currency-name").text() is "NUEVO SOLES"
        currency = $("select[name=moneda]").val()
        console.log currency
        if $("[name=currency]").val() isnt currency
            purchase = $("[name=#{$("[name=currency]").val()}]").val()
            data['precio'] = data['precio'] * parseFloat(purchase)

        $.post "", data, (response) ->
            console.info response
            if response.status
                listMaterials()
            else
                $().toastmessage "showErrorToast", "No found Transaction #{response.raise }"
        , "json"
        return
    else
        $().toastmessage "showWarningToast", "Existe campos vacio."
    return

listMaterials = ->
    data = new Object()
    data.pro = $("input[name=pro]").val()
    data.sub = $("input[name=sub]").val()
    data.sec = $("input[name=sec]").val()
    data.type = "list"
    $.getJSON "", data, (response) ->
        console.info response
        if response.status
            template = "<tr class=\"{{ materials_id }}-{{ id }}\">
                            <td>{{ item }}</td>
                            <td>{{ materials_id }}</td>
                            <td>{{ name }}</td>
                            <td>{{ measure }}</td>
                            <td>{{ unit }}</td>
                            <td>{{ quantity }}</td>
                            <td>{{ price }}</td>
                            <td>
                                <button class=\"btn btn-xs btn-link text-green btn-show-edit\" value=\"{{ materials_id }}-{{ id }}\">
                                    <span class=\"glyphicon glyphicon-pencil\"></span>
                                </button>
                            </td>
                            <td>
                                <button class=\"btn btn-xs btn-link text-red btn-del-mat\" value=\"{{ materials_id }}-{{ id }}\">
                                    <span class=\"glyphicon glyphicon-trash\"></span>
                                </button>
                            </td>
                        </tr>"
            $tb = $(".table-details > tbody")
            $tb.empty()
            for x of response.list
                response.list[x].item = parseInt(x) + 1
                $tb.append Mustache.render template, response.list[x]
    return

delMaterials = (event)->
    console.log @value
    $materials = $(".#{@value} > td")
    $().toastmessage "showToast",
        "text": "Desea eliminar #{$materials.eq(2).text()} #{$materials.eq(3).text()}?"
        "sticky" : true
        "type" : "confirm"
        "buttons" : [{value:'Si'}, {value:'No'}]
        "success" : (result) ->
            if result is "Si"
                data = new Object()
                data.pro = $("input[name=pro]").val()
                data.sub = $("input[name=sub]").val()
                data.sec = $("input[name=sec]").val()
                data.materials = $materials.eq(1).text()
                data.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
                data.type = "del"
                $.post "", data, (response) ->
                    if response.status
                        $(".#{@value}").remove()
                        $(".table-details > tbody > tr").each (index, element) ->
                            element.find "td"
                            .eq 0
                            .text index + 1
                        return
                    else
                        $().toastmessage "showWarningToast", "No se elimino el material."
                return
    return

editMaterials = (event) ->
    btn = @
    data = new Object()
    data.proyecto = $("input[name=pro]").val()
    data.subproyecto = $("input[name=sub]").val()
    data.sector = $("input[name=sec]").val()
    data.materiales = $("input[name=edit-materials]").val()
    data.cantidad = $("input[name=edit-quantity]").val()
    data.precio = $("input[name=edit-price]").val()
    data.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
    data.type = "add"
    data.edit = true
    if data.cantidad != "" and data.precio != ""
        currency = $("select[name=moneda-e]").val()
        console.log currency
        console.info $("[name=currency]").val()
        if $("[name=currency]").val() != currency
            console.warn $("[name=#{$("[name=currency]").val()}]").val()
            purchase = $("[name=#{$("[name=currency]").val()}]").val()
            data.precio = (data.precio * purchase)

        $.post "", data, (response) ->
            if response.status
                $materials = $(".#{btn.value} > td")
                $materials.eq(5).text data.cantidad
                $materials.eq(6).text data.precio
                $(".medit").modal "toggle"
            else
                $().toastmessage "showWarningToast", "No se edito el material."
    else
        $().toastmessage "showWarningToast", "Existen campos vacios o menores a uno."
    return