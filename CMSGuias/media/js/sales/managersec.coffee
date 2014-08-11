$(document).ready ->
    $(".panel-add,input[name=read], .step-second, .body-subandsec, .body-sector, .body-materials, .ordersbedside").hide()
    $("input[name=traslado]").datepicker "dateFormat": "yy-mm-dd", changeMonth : true, changeYear : true, minDate : "0"
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
    $(document).on "click", ".btn-show-secsub", loadSecandSub
    $(document).on "click", ".btn-show-subproject_id", loadSector
    $(document).on "click", ".btn-show-sector_id", loadMaterials
    $(".btn-save-edit").on "click", editMaterials
    $(".btn-show-copy").on "click", ->
        $(".mcopy").modal "show"
        $.getJSON "/json/projects/lists/",
            "sector" : true,
            "pro" : $("input[name=pro]").val(),
            "sub" : $("input[name=sub]").val(),
            (response)->
                if response.status
                    template = "<a class=\"list-group-item\">
                                <button class=\"btn badge btn-primary btn-show-sector_id\" value=\"{{ sector_id }}\" data-sub=\"{{ subproject_id }}\" data-pro=\"{{ project_id }}\" data-body=\"projects\"><span class=\"glyphicon glyphicon-chevron-right\"></span></button>
                                {{ name }}
                                </a>"
                    $sec = $("ul.sector-local")
                    $sec.empty()
                    for x of response.sector
                        $sec.append Mustache.render template, response.sector[x]
                    return
        return
    $(".btn-back").on "click", copyBack
    $(".btn-paste").on "click", pasteMaterials
    $("input[name=rcp]").on "change", changeRadio
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
    $("input[name=proid], input[name=proname]").on "keyup", (event)->
        key = if window.Event then event.keyCode else event.which
        if key is 13
            data = new Object()
            if @name == "proid"
                data.code = $("input[name=proid]").val()
            else
                data.name = $("input[name=proname]").val()
            data.project = true
            $.getJSON "/json/projects/lists/", data, (response) ->
                if response.status
                    template = "<tr><td>{{ project_id }}</td><td>{{ name }}</td><td><button class=\"btn badge btn-primary btn-xs btn-show-secsub\" value=\"{{ project_id }}\" data-body=\"projects\"><span class=\"glyphicon glyphicon-chevron-right\"></span></button></td></tr>"
                    $tb = $(".table-projects > tbody")
                    $tb.empty()
                    for x of response.project
                        $tb.append Mustache.render template, response.project[x]
                    return
            return
    # seconded part for order to store
    $("input[name=choice]").on "change", selectChoiseOrder
    $(document).on "click", ".btn-nip-edit", show_edit_nipple
    $(".btn-show-orders").on "click", showOrders
    $(document).on "click", ".btn-append-list-nipp", showListNipp
    $(document).on "click", ".showhidenipp", showHideTbody
    $(document).on "change", "input[name=rdonipp]", changeRdoNip
    $(document).on "change", ".chknipp", chkNippChange
    $(document).on "blur", ".valquamax", valMax
    $(".btn-next-order").on "click", nextOrders
    $(".btn-back-order").on "click", backOrders
    $(".comment-mat").on "blur", updateCommentMat
    $(".btn-generate-orders").on "click", generateOrders
    $("#orderf").click ->
        $("#orderfile").click()
    tinymce.init
        selector: "textarea[name=obser]",
        theme: "modern",
        menubar: false,
        statusbar: false,
        plugins: "link contextmenu",
        fullpage_default_doctype: "<!DOCTYPE html>",
        font_size_style_values : "10px,12px,13px,14px,16px,18px,20px",
        toolbar1: "styleselect | fontsizeselect | | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent |"
        toolbar2: "undo redo | bold italic |"
    return

loadSecandSub = (event) ->
    $(".body-projects, .body-sector, .body-materials").hide()
    $(".body-subandsec").show 600
    $(".btn-back").val $(@).attr "data-body"
    $.getJSON "/json/projects/lists/",
        "pro" : @value,
        "subproject" : true,
        "sector" : true
        (response) ->
            if response.status
                template = "<a class=\"list-group-item\">
                                <button class=\"btn badge btn-primary btn-show-sector_id\" value=\"{{ sector_id }}\" data-sub=\"{{ subproject_id }}\" data-pro=\"{{ project_id }}\" data-body=\"subandsec\"><span class=\"glyphicon glyphicon-chevron-right\"></span></button>
                                {{ name }}
                                </a>"
                $item = $("ul.sectors")
                $item.empty()
                for x of response.sector
                    $item.append Mustache.render template, response.sector[x]

                $item = $("ul.subprojects")
                template = template.replace "sector_id", "subproject_id", 2
                $item.empty()
                for x of response.subproject
                    $item.append Mustache.render template, response.subproject[x]
                return
    return

loadSector = (event) ->
    $(".body-projects, .body-subandsec, .body-materials").hide()
    $(".body-sector").show 600
    $(".btn-back").val $(@).attr "data-body"
    $.getJSON "/json/projects/lists/",
        "pro" : $(@).attr("data-pro"),
        "sub" : $(@).attr("data-sub"),
        "sector" : true,
        (response) ->
            if response.status
                template = "<a class=\"list-group-item\">
                                <button class=\"btn badge btn-primary btn-show-sector_id\" value=\"{{ sector_id }}\" data-sub=\"{{ subproject_id }}\" data-pro=\"{{ project_id }}\" data-body=\"sector\"><span class=\"glyphicon glyphicon-chevron-right\"></span></button>
                                    {{ name }}
                                </a>"
                $item = $("ul.list-sector")
                $item.empty()
                for x of response.sector
                    $item.append Mustache.render template, response.sector[x]
                return
    return

loadMaterials = (event) ->
    $(".body-projects, .body-subandsec, .body-sector").hide()
    $(".body-materials").show 600
    $(".btn-back").val $(@).attr "data-body"
    $("input[name=cpro]").val $(@).attr("data-pro")
    $("input[name=csub]").val $(@).attr("data-sub")
    $("input[name=csec]").val @value
    $.getJSON "/json/projects/lists/",
        "pro" : $(@).attr("data-pro"),
        "sub" : $(@).attr("data-sub"),
        "sec" : @value,
        "materials" : true,
        (response) ->
            if response.status
                template = "<tr id=\"{{ materials_id }}-copy\"><td>{{ item }}</td><td><input type=\"checkbox\" name=\"copy\" value=\"{{ materials_id }}-copy\"></td><td>{{ materials_id }}</td><td>{{ name }}</td><td>{{ measure }}</td><td>{{ unit }}</td><td>{{ quantity }}</td><td>{{ price }}</td></tr>"
                $item = $("table.table-copy > tbody")
                $item.empty()
                for x of response.materials
                    response.materials[x].item = parseInt(x) + 1
                    $item.append Mustache.render template, response.materials[x]
                return
    return

copyBack = (event)->
    if $(".body-sector").is(":visible")
        @value = "subandsec"
    else if $(".body-sector").is(":visible")
        @value = "projects"
    else if $(".body-subandsec").is(":visible")
        @value = "projects"

    if $(".body-projects").is(":visible")
        $(".body-projects").hide()
    if $(".body-subandsec").is(":visible")
        $(".body-subandsec").hide()
    if $(".body-sector").is(":visible")
        $(".body-sector").hide()
    if $(".body-materials").is(":visible")
        $(".body-materials").hide()


    $(".body-#{@value}").show 600
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
            $(".btn-show-mat").find("span").removeClass("glyphicon-chevron-up").addClass "glyphicon-chevron-down"
        else
            $(".btn-show-mat").find("span").removeClass("glyphicon-chevron-down").addClass "glyphicon-chevron-up"
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
            $(btn).find("span").removeClass("glyphicon-chevron-up").addClass "glyphicon-chevron-down"
            return
        else
            $(btn).find("span").removeClass("glyphicon-chevron-down").addClass "glyphicon-chevron-up"
            return
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
            # valid exists exchange rate for today
            if $("[name=#{$("[name=currency]").val()}]").val() is null or $("[name=#{$("[name=currency]").val()}]").val() is undefined
                $().toastmessage "showWarningToast", "El tipo de cambio no esta registrado."
                return false
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
    btn = @value
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
                        $(".#{btn}").remove()
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
            if $("[name=#{$("[name=currency]").val()}]").val() is null or $("[name=#{$("[name=currency]").val()}]").val() is undefined
                $().toastmessage "showWarningToast", "El tipo de cambio no esta registrado."
                return false
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

pasteMaterials = ->
    $cp = $("input[name=copy]")
    data = new Object()
    arr = new Array()
    counter = 0
    $cp.each (index, element) ->
        if @checked
            counter += 1
            $td = $("##{@value} > td")
            arr.push($td.eq(2).text())
    data.materials = arr
    data.paste = true
    data.pro = $("input[name=pro]").val()
    data.sub = $("input[name=sub]").val()
    data.sec = $("input[name=sec]").val()
    data.cpro = $("input[name=cpro]").val()
    data.csub = $("input[name=csub]").val()
    data.csec = $("input[name=csec]").val()
    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
    if counter > 0 and counter >= $cp.length
        $.post "/json/projects/lists/",data, (response) ->
            if response.status
                location.reload()
            else
                $().toastmessage "showErrorToast", "No found Transaction"
        , "json"
    return

changeRadio = (event) ->
    $(@).each (index, element) ->
        if @checked
            rdo = @
            $("input[name=copy]").each (index, element) ->
                @checked = if rdo.value is "all" then "checked" else ""
    return


# part two -> order to store, this include administrator, sales and store
#
#
#change choice order
selectChoiseOrder = (event) ->
    event.preventDefault()
    $(@).each ->
        if @checked
            chk = @
            $("input[name=mats]").each (index, element) ->
                @checked = Boolean parseInt chk.value
                return

    return

list_temp_nipples = (idmat)->
    data =
        "list-nip" : true
        "pro" : $("input[name=pro]").val()
        "sub" : $("input[name=sub]").val()
        "sec" : $("input[name=sec]").val()
        "mat" : idmat
    $.getJSON "", data, (response) ->
        if response.status
            template = "<tr class=\"trnip{{ id }}\">
                            <td>{{ quantity }}</td>
                            <td>{{ name }}</td>
                            <td>{{ diameter }}</td>
                            <td>x</td>
                            <td>{{ measure }}</td>
                            <td>{{ unit }}</td>
                            <td>{{ comment }}</td>
                            <td>
                                <button class=\"btn btn-xs btn-link text-green btn-nip-edit {{ view }}\" data-edit-nip=\"{{ materials }}\" value=\"{{ id }}\">
                                    <span class=\"glyphicon glyphicon-pencil\"></span>
                                </button>
                            </td>
                            <td>
                                <button class=\"btn btn-xs btn-link btn-nip-del text-red {{ view }}\" data-del-nip=\"{{ materials }}\" value=\"{{ id }}\">
                                    <span class=\"glyphicon glyphicon-trash\"></span>
                                </button>
                            </td>
                        </tr>"
            $tb = $("#des#{idmat} > div > table > tbody")
            $tb.empty()
            for x of response.list
                response.list[x].item = (parseInt(x) + 1)
                $tb.append Mustache.render template, response.list[x]

            $(".in#{idmat}").text (response.ingress)
            $(".res#{idmat}").text ($(".totr#{idmat}").val() * 100) - response.ingress
            return
    return

aggregate_nipples = (idmat) ->
    $(".nv#{idmat}").val ""
    $(".mt#{idmat}").val ""
    $(".tn#{idmat}").val ""
    $(".nc#{idmat}").text ""
    $(".update-quantity-#{idmat}").val ""
    $(".update-id-#{idmat}").val ""
    $(".tn#{idmat},.mt#{idmat},.nv#{idmat},.nc#{idmat},.bn#{idmat}").attr "disabled", false
    return

saved_or_update_nipples = (idmat) ->
    if idmat.length == 15
        data = new Object()
        pass = false
        data.addnip = true
        data.proyecto = $("input[name=pro]").val()
        data.subproyecto = $("input[name=sub]").val()
        data.sector = $("input[name=sec]").val()
        data.materiales = idmat
        data.metrado = parseFloat parseInt $(".mt#{idmat}").val()
        data.tipo = $(".tn#{idmat}").val()
        data.cantidad = parseFloat parseInt $(".nv#{idmat}").val()
        data.cantshop = parseFloat parseInt $(".nv#{idmat}").val()
        data.comment = $($(".nc#{idmat}")).val()
        data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
        if $("input.update-id-#{idmat}").val() isnt ""
            data.id = $("input.update-id-#{idmat}").val()
            pass = if (data.metrado * data.cantidad) <= (parseFloat parseInt($(".res#{idmat}").text()) + parseFloat parseInt($(".update-quantity-#{idmat}").val())) then true else false
        else
            pass = if (data.metrado * data.cantidad) <= parseFloat parseInt $(".res#{idmat}").text() then true else false
        if pass
            $.post "", data, (response) ->
                if response.status
                    $(".tn#{idmat},.mt#{idmat},.nv#{idmat},.nc#{idmat},.bn#{idmat}").attr "disabled", true
                    $(".update-quantity-#{idmat}").val ""
                    $(".update-id-#{idmat}").val ""
                    list_temp_nipples idmat

            return
        else
            $().toastmessage "showWarningToast", "Cantidad es mayor a la establecida."
    else
        $().toastmessage "showWarningToast", "Código incorrecto"
    return

show_edit_nipple = ->
    idmat = $(@).attr "data-edit-nip"
    tipo = new Object()
    $(".tn#{idmat}").find("option").each (index, element) ->
        text = $.trim element.innerHTML
        text = text.split "-"
        if text.length == 2
            text = text[1]
        else if text.length == 3
            text = text[1] + "-" + text[2]
        tipo[text] = element.value
        return

    $(".update-id-#{idmat}").val @value
    $td = $(".trnip#{@value} > td")
    $(".nv#{idmat}").val $td.eq(0).text()
    $(".mt#{idmat}").val $td.eq(4).html()
    $(".tn#{idmat}").val tipo[$td.eq(1).text()]
    $(".nc#{idmat}").text $td.eq(6).text()
    $(".update-quantity-#{idmat}").val(parseFloat($td.eq(0).text()) * parseFloat($td.eq(4).text()))
    $(".tn#{idmat},.mt#{idmat},.nv#{idmat},.nc#{idmat},.bn#{idmat}").attr "disabled", false
    return

delete_all_temp_nipples = (idmat)->
    if idmat isnt ""
        $().toastmessage "showToast",
            text : "Desea eliminar todo los niples de la tuberia?"
            type : "confirm"
            sticky : true
            buttons : [{value:'Si'},{value:'No'}]
            success : (result) ->
                if result is "Si"
                    data = new Object()
                    data.addnip = true
                    data.proyecto = $("input[name=pro]").val()
                    data.subproyecto = $("input[name=sub]").val()
                    data.sector = $("input[name=sec]").val()
                    data.materiales = idmat
                    $.post "", data, (response) ->
                        if response.status
                            list_temp_nipples idmat
                    , "json"
                    return
        return
    else
        $().toastmessage "showWarningToast", "Código de material incorrecto."
    return

deleteallnipmat = ->

    return

showOrders = ->
    counter = 0
    data = new Object()
    arr = new Array()
    $("input[name=mats]").each (index, element) ->
        if @checked
            counter += 1
            $td = $(".#{@value} > td")
            arr.push {"item": counter, "materials":$td.eq(2).text(), 'name': $td.eq(3).text(), 'measure':$td.eq(4).text(), 'unit':$td.eq(5).text(),'brand':$td.eq(6).text(), 'model':$td.eq(7).text(),'quantity':$td.eq(8).text()}
    data.list = arr
    if counter > 0
        $tb = $(".torders > tbody.materials")
        $tb.empty()
        for x of data.list
            template = "<tr>
                    <td>{{ item }}</td>
                    <td>{{ materials }}</td>
                    <td>{{ name }}</td>
                    <td>{{ measure }}</td>
                    <td>{{ unit }}</td>
                    <td>{{ brand }}</td>
                    <td>{{ model }}</td>
                    <td>{{ quantity }}</td>
                    <td>
                        {{! input }}
                    </td>
                    </tr>"
            if $.trim(data.list[x].materials.substring(0, 3)) == "115"
                template = template.replace("{{! input }}", "
                        <div class=\"input-group\">
                            <input type=\"number\" class=\"form-control input-sm meter{{ materials }} quantityOrders\" data-mat=\"{{ materials }}\" readonly=\"readonly\">
                            <span class=\"input-group-btn\">
                                <button class=\"btn btn-default btn-sm btn-append-list-nipp\" value=\"{{ materials }}\" type=\"button\">
                                    <span class=\"glyphicon glyphicon-list\"></span>
                                </button>
                            </span>
                        </div>")
            else
                template = template.replace("{{! input }}","
                        <input type=\"number\" min=\"1\" max=\"{{ quantity }}\" value=\"{{ quantity }}\" data-mat=\"{{ materials }}\" class=\"form-control input-sm valquamax quantityOrders\">")
            $tb.append Mustache.render template, data.list[x]
        $("#morders").modal "toggle"
    else
        $().toastmessage "showWarningToast", "Tienes que seleccionar por lo menos un material."
    return

showListNipp = ->
    idmat = @value
    data = new Object()
    arr =  new Array()
    counter = 0
    # console.log $("table.torders > tbody.nipples > tr.prenip#{idmat}").length
    if $("table.torders > tbody.nipples > tr.prenip#{idmat}").length is 0
        $tr = $("div#des#{@value} > div > table > tbody.tb > tr")
        if $tr.length is 0
            list_temp_nipples @value
        $tr.each ()->
            $td = $(@).find("td")
            counter += 1
            arr.push {"item":counter, "quantity":$td.eq(0).text(), "name": $td.eq(1).text(), "diameter":$td.eq(2).text(),"measure":$td.eq(4).text(), "unit":"cm", "comment":$td.eq(6).text(),"id":$td.eq(7).find("button").val()}
            return
    else
        console.log "row exists"
        counter = 1
    if counter > 0
        if arr.length > 0
            data.nip = arr
            $tb = $(".torders > tbody.nipples")
            template = "<tr class=\"#{idmat}nip{{ id }}\"><td><input type=\"checkbox\" class=\"chknipp chknipp#{idmat}\" value=\"#{idmat}nip{{ id }}\" value=\"{{ id }}\"></td><td><input type=\"number\" class=\"form-control input-sm valquamax\" style=\"width:90px;\" data-id=\"{{ id }}\" min=\"1\" max=\"{{ quantity }}\" value=\"{{ quantity }}\" data-mat=\"#{idmat}\" disabled></td><td>{{ quantity }}</td><td>{{ name }}</td><td>{{ diameter }}</td><td>x</td><td>{{ measure }}</td><td>{{ unit }}</td><td>{{ comment }}</td></tr>"
            dat = ""
            for x of data.nip
                dat = dat.concat Mustache.render template, data.nip[x]

            $mat = $(".#{idmat} > td")
            template = "<tr class=\"prenip#{idmat}\"><td colspan=\"9\">
                        <table class=\"table table-condensed table#{idmat}\">
                            <thead>
                                <tr>
                                    <td colspan=\"8\">#{ $mat.eq(3).text()} - #{$mat.eq(4).text()} <div class=\"form-group\">seleccionar :
                                            <label class=\"radio-inline\"><input type=\"radio\" data-mat=\"#{idmat}\" value=\"1\" name=\"rdonipp\"> todo</label>
                                            <label class=\"radio-inline\"><input type=\"radio\" data-mat=\"#{idmat}\" value=\"0\" name=\"rdonipp\"> ninguno.</label>
                                        </div></td>
                                </tr>
                                <tr><th><button value=\"#{idmat}\" class=\"btn btn-xs btn-link showhidenipp\"><span class=\"glyphicon glyphicon-chevron-up\"></span></button></th><th>Pedido</th><th>Cantidad</th><th>Tipo</th><th>Diametro</th><th></th><th>Medida</th><th>Unidad</th></tr>
                            </thead>
                            <tbody>{rows}</tbody>
                        </table>
                        </td></tr>"
            template = template.replace "{rows}", dat
            $tb.append template
        else
            console.log "mostramos row old "
    return

showHideTbody = ->
    btn = @
    if @value.length is 15
        $(".table#{@value} > tbody").toggle ->
            if $(@).is(":hidden")
                $(btn).find("span").removeClass "glyphicon-chevron-up"
                .addClass "glyphicon-chevron-down"
            else
                $(btn).find("span").removeClass "glyphicon-chevron-down"
                .addClass "glyphicon-chevron-up"
    else
        $("#{@value}").toggle ->
            if $(@).is(":hidden")
                $(btn).find("span").removeClass "glyphicon-chevron-up"
                .addClass "glyphicon-chevron-down"
            else
                $(btn).find("span").removeClass "glyphicon-chevron-down"
                .addClass "glyphicon-chevron-up"
    return

changeRdoNip = ->
    chk = false
    $(@).each ->
        if @.checked
            chk = Boolean parseInt @value
            $(".chknipp#{$(@).attr "data-mat"}").each ->
                @.checked = chk
                $(@).change()
                return
            return
    return

chkNippChange = ->
    if @value isnt ""
        $td = $("tr.#{@value} > td")
        $td.eq(1).find("input").attr "disabled", not @checked
        calMeter @value.substring 0, 15
    return

calMeter = (matid)->
    input = $(".meter#{matid}")
    m = 0
    $(".table#{matid} > tbody > tr").each (index, element) ->
        $td = $(element).find("td")
        if $td.eq(0).find("input").is(":checked")
            quantity = parseFloat $td.eq(1).find("input").val()
            meter = parseFloat $td.eq(6).text()
            m += ((quantity * meter) / 100)
    input.val m
    return

valMax = ->
    $input = $(@)
    max = parseFloat $input.attr "max"
    val = parseFloat $input.val()
    mat = $input.attr "data-mat"
    if val > max
        $input.val max
    else if val < 1
        $input.val 1
        id = $input.attr "data-id"
        #$input.val max
        $("tr.#{mat}nip#{id} > td").eq(0).find("input").attr "checked", false
        .change()
    calMeter mat
    return

nextOrders = ->
    pass = valQuantityPreOrders()
    if pass
        $(".torders").fadeOut 400
        $(".ordersbedside").fadeIn 800
    else
        $().toastmessage "showWarningToast", "Existe campos vacios o con valor cero, esto es incorrecto."
    return

backOrders = ->
    $(".ordersbedside").fadeOut 400
    $(".torders").fadeIn 800
    return

valQuantityPreOrders = ->
    pass = false
    $(".quantityOrders").each (index, element) ->
        if element.value is "" or element.value is 0 or element.value is "0"
            pass = false
            return
        else
            pass = true
            return
    return pass

updateCommentMat = ->
    data = new Object()
    data.pro = $("input[name=pro]").val()
    data.sub = $("input[name=sub]").val()
    data.sec = $("input[name=sec]").val()
    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
    data.comment = @value
    data.mat = $(@).attr "data-mat"
    data.upcomment = true
    $.post "", data
    return

validOrders = ->
    data = new Object()
    detail = new Array()
    nipp = new Array()
    pipe = new Array()
    pass = false
    $(".ordersbedside > .row").find("select,input").each ->
        #console.warn "#{@name} and #{@value} length #{@value.length}"
        if @value is ""
            if @name isnt "orderfile"
                pass = false
                data.elemet = @name
                return pass
            return
        else
            if @name isnt "orderfile" and @name isnt ""
                data[@name] = @value #$(element).value
                pass = true
            return
    if pass
        $(".quantityOrders").each (index, element) ->
            if element.value isnt "" or element.value isnt 0 or element.value isnt "0"
                detail.push {"idmat": element.getAttribute("data-mat"), "quantity": parseFloat(element.value), "comment":$("tr.#{element.getAttribute("data-mat")}").find("td").eq(11).find("input").val()}
                if element.getAttribute("data-mat").substring(0,3) is "115"
                    pipe.push element.getAttribute("data-mat")
                    return
        if pipe.length > 0
            tipo = new Object()
            $(".tn#{detail[0].idmat}").find("option").each (index, element) ->
                text = $.trim element.innerHTML
                text = text.split "-"
                if text.length == 2
                    text = text[1]
                else if text.length == 3
                    text = text[1] + "-" + text[2]
                tipo[text] = element.value
                return
            for x of pipe
                $(".table#{pipe[x]} > tbody > tr").each (index, element) ->
                    $td = $(element).find("td")
                    if $td.eq(0).find("input").is(":checked")
                        ar = $("tr.trnip#{$td.eq(1).find("input").attr("data-id")}").find("td").eq(1).text().split(",")
                        met = $("tr.trnip#{$td.eq(1).find("input").attr("data-id")}").find("td").eq(4).text()
                        nipp.push({"quantity":parseFloat($td.eq(1).find("input").val()), "idnip":$td.eq(1).find("input").attr("data-id"), "idmat": $td.eq(1).find("input").attr("data-mat"), "comment": $("tr.trnip#{$td.eq(1).find("input").attr("data-id")}").find("td").eq(6).text(), "type": ar[1], "meter" : met})
                        return
    data.detail = JSON.stringify detail
    data.nipples = JSON.stringify nipp
    data.pass = pass
    return data

generateOrders = ->
    val = validOrders()
    if val.pass
        btn = @
        data = new FormData()
        if $("input[name=orderfile]").get(0).files.length > 0
            data.append "orderfile", $("input[name=orderfile]").get(0).files[0]
        data.append "obser", $("#obser_ifr").contents().find("body").html()
        data.append "proyecto", $("input[name=pro]").val()
        data.append "subproyecto", $("input[name=sub]").val()
        data.append "sector", $("input[name=sec]").val()
        data.append "csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val()
        data.append "almacen", val.almacen
        data.append "asunto", val.asunto
        data.append "empdni", val.empdni
        data.append "traslado", val.traslado
        data.append "details", val.detail
        data.append "nipples", val.nipples
        data.append "saveorders", true
        $.ajax
            data : data
            url : ""
            type : "POST"
            dataType : "json"
            cache: false
            contentType : false
            processData : false
            beforeSend : ->
                $(btn).button("loading");
            success : (response) ->
                if response.status
                    $(btn).button('loading');
                    $().toastmessage "showNoticeToast", "Correcto! se a generado el pedido a almacén nro #{response.nro}"
                    setTimeout ->
                        location.reload()
                    , 2600
                else
                    $().toastmessage "showWarningToast", "No se a generado el pedido almacén, #{response.raise}"
        return
    else
        $().toastmessage "showWarningToast", "existe un error de formatado, revise los campos del formulario"
    return