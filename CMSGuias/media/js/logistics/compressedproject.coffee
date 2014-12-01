$(document).ready ->
    $("input[name=select]").on "change", changeSelect
    $("table.table-float").floatThead
        useAbsolutePositioning: false
        scrollingTop: 50
    return

changeSelect = (event) ->
    radio = @
    if @checked
        $("input[name=materials]").each (index, element) ->
            element.checked = Boolean parseInt radio.value
            return
    return

getListCheck = (event) ->
    data = new Array
    $("input[name=materials]").each (index, element) ->
        if element.checked
            data.push
                "materials": element.getAttribute "data-materials"
                "quantity": element.value
                "remainder": element.getAttribute "data-remainder"
                "brand": element.getAttribute "data-brand"
                "model": element.getAttribute "data-model"
            return
    if data.length
        return data

createTmpQuatation = (event) ->
    data = new Object
    data.details = getListCheck()
    setTimeout ->
        if data.details.length
        else
            $().toastmessage "showWarningToast", "No se han encontrado materiales para cotizar."
    , 300
    return

createTmpPurchase = (event) ->
    data = new Object
    data.details = getListCheck()
    setTimeout ->
        if data.details.length
        else
            $().toastmessage "showWarningToast", "No se han encontrado materiales para Comprar."
    , 300
    return