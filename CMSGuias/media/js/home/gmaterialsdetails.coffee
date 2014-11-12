$(document).ready ->
    # Elements loading hidden
    $(".panel-add-materials, .body-two").hide()
    $(".btn-add-show").on "click", showPanelAdd
    $(".btn-add").on "mouseenter mouseleave",  btnAddChangeIcon
    $("input[name=cantidad],input[name=equantity]").on "keydown", numberOnly
    $("button.btn-add").on "click", addMaterials
    $("button.btn-save-e").on "click", saveEditQuantity
    $("button.btn-del-all").on "click", delAllDetails
    $(document).on "click", "button.btn-edit", showeQuantity
    $(document).on "click", "button.btn-del", delMaterial
    $("button.btn-cp").on "click", showCopy
    $("input[name=gdesc],input[name=gcode]").on "keyup", searchGroup
    $("button.btn-back-copy").on "click", backSearch
    $(document).on "click", "button.btn-details", getDetailsGroup
    $("button.btn-save-clipboard").on "click", copyClipboard
    return

showPanelAdd = (event) ->
    $btn = $(@)
    $(".panel-add-materials").fadeToggle 800, ->
        if $(@).is(":visible")
            $btn.removeClass "btn-success"
            .removeClass "text-black"
            .addClass "btn-default"
            .find "span"
            .eq 0
            .removeClass "glyphicon-plus-sign"
            .addClass "glyphicon-remove-sign"
            $btn.find "span"
            .eq 1
            .text "Cancelar"
            return
        else
            $btn.removeClass "btn-default"
            .addClass "btn-success"
            .addClass "text-black"
            .find "span"
            .eq 0
            .removeClass "glyphicon-remove-sign"
            .addClass "glyphicon-plus-sign"
            $btn.find "span"
            .eq 1
            .text "Agregar"
            return
    return

btnAddChangeIcon = (event) ->
    $(@).hover ->
        $(@).find "span"
        .eq 0
        .removeClass "glyphicon-plus-sign"
        .addClass "glyphicon-plus"
        return
    , ->
        $(@).find "span"
        .eq 0
        .removeClass "glyphicon-plus"
        .addClass "glyphicon-plus-sign"
        return
    return

listMaterials = (event) ->
    data = new Object
    data.listMaterials = true
    $.getJSON "", data, (response) ->
        if response.status
            $tb = $("table.table-details > tbody")
            $tb.empty()
            template = "<tr class=\"tr-{{ code }}\">
                        <td>{{ item }}</td>
                        <td>{{ code }}</td>
                        <td>{{ name }}</td>
                        <td>{{ meter }}</td>
                        <td>{{ unit }}</td>
                        <td>{{ quantity }}</td>
                        <td class=\"text-center\">
                            <button class=\"btn btn-xs btn-link text-green btn-edit\" value=\"{{ code }}\">
                                <span class=\"glyphicon glyphicon-edit\"></span>
                            </button>
                        </td>
                        <td class=\"text-center\">
                            <button class=\"btn btn-xs btn-link text-red btn-del\" value=\"{{ code }}\">
                                <span class=\"glyphicon glyphicon-trash\"></span>
                            </button>
                        </td>
                        </tr>"
            for x of response.details
                response.details[x].item = parseInt(x) + 1
                $tb.append Mustache.render template, response.details[x]
            return
    return

addMaterials = (event) ->
    data = new Object
    data.code = $(".id-mat").text()
    if data.code is ""
        $().toastmessage "showWarningToast", "Ingrese un material."
        return false
    data.quantity = parseFloat($("input[name=cantidad]").val())
    if ($("input[name=cantidad]").val() is "")
        return false
        $().toastmessage "showWarningToast", "Ingrese una cantidad."
    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
    data.addMaterials = true
    $.post "", data, (response) ->
        if response.status
            listMaterials()
        else
            $().toastmessage "showErrorToast", "No se a podido agregar el material. #{raise}"
    , "json"
    return

showeQuantity = (event) ->
    code = @value
    $td = $("tr.tr-#{code}").find("td")
    $("span.emname").text "#{$td.eq(2).text()} - #{$td.eq(3).text()}"
    $("input[name=equantity]").val $td.eq(5).text()
    $("input[name=ematerials]").val $td.eq(1).text()
    $(".mequantity").modal "show"
    return

saveEditQuantity = (event) ->
    data = new Object
    data.code = $("input[name=ematerials]").val()
    if data.code is ""
        $().toastmessage "showWarningToast", "Ingrese un material."
        return false
    data.quantity = parseFloat($("input[name=equantity]").val())
    if ($("input[name=equantity]").val() is "")
        return false
        $().toastmessage "showWarningToast", "Ingrese una cantidad."
    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
    data.eMaterials = true
    $.post "", data, (response) ->
        if response.status
            listMaterials()
            $("input[name=equantity]").val ""
            $("input[name=ematerials]").val ""
            $(".mequantity").modal "hide"
        else
            $().toastmessage "showErrorToast", "No se a podido agregar el material. #{raise}"
    , "json"
    return

delAllDetails = (event) ->
    $().toastmessage "showToast",
        text: "Realmente desea eliminar todo la lista de materiales?"
        type: "confirm"
        sticky: true
        buttons: [{value:"Si"}, {value:"No"}]
        success: (result) ->
            if result is "Si"
                data = new Object
                data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
                data.delall = true
                $.post "", data, (response) ->
                    if response.status
                        location.reload()
                    else
                        $().toastmessage "showErrorToast", "No se a podido eliminar la lista."
                        return
                return
    return

delMaterial = (event) ->
    $btn = @
    $().toastmessage "showToast",
        text: "Realmente desea eliminar el materiale?"
        type: "confirm"
        sticky: true
        buttons: [{value:"Si"}, {value:"No"}]
        success: (result) ->
            if result is "Si"
                data = new Object
                data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
                data.materials = $btn.value
                data.delMaterial = true
                $.post "", data, (response) ->
                    if response.status
                        listMaterials()
                    else
                        $().toastmessage "showErrorToast", "No se a podido eliminar la lista."
                        return
                return
    return

showCopy = (event) ->
    $(".mcopy").modal "show"
    return

searchGroup = (event) ->
    data = new Object
    data.name = @name
    if data.name is "gcode" and @value.length < 10
        return false

    data.val = @value
    data.searchGruop = true
    $.getJSON "", data, (response) ->
        $tb = $("table.tgroup > tbody")
        $tb.empty()
        if response.status
            template = "<tr>
                        <td>{{ item }}</td>
                        <td>{{ desc }}</td>
                        <td>{{ materials }}</td>
                        <td>{{ parent }}</td>
                        <td>{{ tgroup }}</td>
                        <td class=\"text-center\">
                            <button class=\"btn btn-xs btn-link btn-details\" value=\"{{ mgroup_id }}\" data-mat=\"{{ materials }}\" data-desc=\"{{ desc }}\">
                                <span class=\"glyphicon glyphicon-list-alt\"></span>
                            </button>
                        </td>
                        </tr>"
            for x of response.details
                response.details[x].item = parseInt(x) + 1
                $tb.append Mustache.render template, response.details[x]
            return
        #else
           #$().toastmessage "showErrorToast", "No se han encontrado resultados."
    return

getDetailsGroup = (event) ->
    btn = @
    data = new Object
    data.listDetails = true
    data.code = @value
    $.getJSON "", data, (response) ->
        if response.status
            $tb = $("table.table-copy > tbody")
            $tb.empty()
            template = "<tr>
                        <td>{{ item }}</td>
                        <td>{{ code }}</td>
                        <td>{{ name }}</td>
                        <td>{{ meter }}</td>
                        <td>{{ unit }}</td>
                        <td>{{ quantity }}</td>
                        </tr>"
            for x of response.details
                response.details[x].item = parseInt(x) + 1
                $tb.append Mustache.render template, response.details[x]
            $(".capdet").text "#{btn.getAttribute "data-desc"} - #{btn.getAttribute "data-mat"}"
            $("div.mcopy > div > div").find(".body-one").fadeOut 300
            $("div.mcopy > div.modal-dialog").addClass "modal-lg"
            $("div.mcopy > div > div").find(".body-two").fadeIn 1000
            return
        else
            $().toastmessage "showWarningToast", "No se han encontrado detalles. #{response.raise}"
            return
    return

backSearch = (event) ->
    $(".capdet").text ""
    $("div.mcopy > div > div").find(".body-two").fadeOut 300
    $("div.mcopy > div.modal-dialog").removeClass "modal-lg"
    $("div.mcopy > div > div").find(".body-one").fadeIn 1000
    return

copyClipboard = (event) ->
    data = new Object
    data.copyClipboard = true
    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
    data.replace = $("input[name=replace]").is(":checked")
    det = new Array
    $("table.table-copy > tbody > tr").each (index, element) ->
        $td = $(element).find "td"
        det.push
            "materials": $td.eq(1).text(),
            "quantity": $td.eq(5).text()
        return
    data.details = JSON.stringify det
    $.post "", data, (response) ->
        if response.status
            location.reload()
            return
        else
            $().toastmessage "showErrorToast", "No se a guardado la lista."
            return
    , "json"
    return