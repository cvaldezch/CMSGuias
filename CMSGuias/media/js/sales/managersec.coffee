$(document).ready ->
    $(".panel-add,input[name=read],.step-second").hide()
    $(".panel-add-mat, .view-full").hide()
    $(".btn-show-mat").on "click", openAddMaterial
    $("input[name=plane]").on "change", uploadPlane
    $(".btn-show-planes").on "click", panelPlanes
    $("[name=show-full]").on "click", viewFull
    $("[name=plane-del]").on "click", delPlane
    $(".btn-add").on "click", addMaterial
    $(".btn-show-del").on "click", dellAllMaterial
    $(".btn-new-brand").on "click", openBrand
    $(".btn-new-model").on "click", openModel
    $("[name=show-plane]").on "click", (event) ->
        $("input[name=plane]").click()
    $(document).on "click", ".btn-del-mat", delMaterials
    $(".btn-save-edit").on "click", editMaterials
    $(document).on "click", ".btn-show-edit", ->
        $(".btn-save-edit").val @value
        $materials = $(".#{@value} > td")
        editBrandandModel $materials.eq(5).text(), $materials.eq(6).text()
        $(".text-edit").text "#{$materials.eq(2).text()} #{$materials.eq(3).text()}"
        $("input[name=edit-materials]").val $materials.eq(1).text()
        $("input[name=edit-quantity]").val $materials.eq(7).text()
        $("input[name=edit-price]").val $materials.eq(8).text()
        $(".medit").modal "toggle"
    $("select[name=edit-brand]").on "change", (event) ->
        $.getJSON "/json/model/list/option/",
            "brand": $("select[name=edit-brand]").val(),
            (response) ->
                if response.status
                    template = "<option value=\"{{ model_id }}\" title>{{ model }}</option>"
                    $model = $("select[name=edit-model]")
                    $model.empty()
                    for x of response.model
                        if model is response.model[x].model
                            $model.append Mustache.render template.replace("title", "selected"), response.model[x]
                        else
                            $model.append Mustache.render template, response.model[x]
                    return
    return

editBrandandModel = (brand, model)->
    $.getJSON "/json/brand/list/option/", (response) ->
        if response.status
            template = "<option value=\"{{ brand_id }}\" title>{{ brand }}</option>"
            $brand = $("select[name=edit-brand]")
            $brand.empty()
            for x of response.brand
                if brand is response.brand[x].brand
                    $brand.append Mustache.render template.replace("title", "selected"), response.brand[x]
                else
                    $brand.append Mustache.render template, response.brand[x]

            $.getJSON "/json/model/list/option/",
                "brand": $("select[name=edit-brand]").val(),
                (response) ->
                    if response.status
                        template = "<option value=\"{{ model_id }}\" title>{{ model }}</option>"
                        $model = $("select[name=edit-model]")
                        $model.empty()
                        for x of response.model
                            if model is response.model[x].model
                                $model.append Mustache.render template.replace("title", "selected"), response.model[x]
                            else
                                $model.append Mustache.render template, response.model[x]
                        return
            return
    return

# Open window
openBrand = ->
    url = "/brand/new/"
    win = window.open url, "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600"
    interval = window.setInterval ->
        if win == null or win.closed
            window.clearInterval interval
            searchBrandOption()
            return
    , 1000
    return win;

openModel = ->
    url = "/model/new/"
    win = window.open url, "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600"
    interval = window.setInterval ->
        if win == null or win.closed
            window.clearInterval interval
            searchModelOption()
            return
    , 1000
    return win;

openAddMaterial = (event) ->
    event.preventDefault()
    $(".panel-add-mat").toggle ->
        if $(@).is(":hidden")
            $(".btn-show-mat").find("span").removeClass "glyphicon-chevron-up"
            .addClass "glyphicon-chevron-down"
        else
            $(".btn-show-mat").find("span").removeClass "glyphicon-chevron-down"
            .addClass "glyphicon-chevron-up"
    return

uploadPlane = (event) ->
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
    data.brand = $("select[name=brand]").val()
    data.model = $("select[name=model]").val()
    if data.materiales != "" and data.cantidad != "" and data.precio != ""
        # if $(".currency-name").text() is "NUEVO SOLES"
        currency = $("select[name=moneda]").val()
        if $("[name=currency]").val() isnt currency
            purchase = $("[name=#{$("[name=currency]").val()}]").val()
            data['precio'] = data['precio'] * parseFloat(purchase)

        $.post "", data, (response) ->
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
        if response.status
            template = "<tr class=\"{{ materials_id }}-{{ id }}\">
                            <td>{{ item }}</td>
                            <td>{{ materials_id }}</td>
                            <td>{{ name }}</td>
                            <td>{{ measure }}</td>
                            <td>{{ unit }}</td>
                            <td>{{ brand }}</td>
                            <td>{{ model }}</td>
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
    data.brand = $("select[name=edit-brand]").val()
    data.model = $("select[name=edit-model]").val()
    data.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
    data.type = "add"
    data.edit = true
    if data.cantidad != "" and data.precio != ""
        currency = $("select[name=moneda-e]").val()
        if $("[name=currency]").val() != currency
            purchase = $("[name=#{$("[name=currency]").val()}]").val()
            data.precio = (data.precio * purchase)

        $.post "", data, (response) ->
            if response.status
                $materials = $(".#{btn.value} > td")
                $materials.eq(5).text $("select[name=edit-brand]").text()
                $materials.eq(6).text $("select[name=edit-model]").text()
                $materials.eq(7).text data.cantidad
                $materials.eq(8).text data.precio
                $(".medit").modal "toggle"
            else
                $().toastmessage "showWarningToast", "No se edito el material."
    else
        $().toastmessage "showWarningToast", "Existen campos vacios o menores a uno."
    return

dellAllMaterial = (event) ->
    $().toastmessage "showToast",
        "text": "Desea eliminar toda la lista de materiales?"
        "sticky" : true
        "type" : "confirm"
        "buttons" : [{value:'Si'}, {value:'No'}]
        "success" : (result) ->
            if result is "Si"
                data = new Object()
                data.pro = $("input[name=pro]").val()
                data.sub = $("input[name=sub]").val()
                data.sec = $("input[name=sec]").val()
                data.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
                data.type = "killdata"
                $.post "", data, (response) ->
                    if response.status
                        location.reload()
                    else
                        $().toastmessage "showWarningToast", "No se elimino la lista de materiales."
                return
    return