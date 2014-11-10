$(document).ready ->
    # Elements loading hidden
    $(".panel-add-materials").hide()
    $(".btn-add-show").on "click", showPanelAdd
    $(".btn-add").on "mouseenter mouseleave",  btnAddChangeIcon
    $("input[name=cantidad]").on "keydown", numberOnly
    $("button.btn-add").on "click", addMaterials
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
            template = "<tr class=\"tr{{ code }}\">
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