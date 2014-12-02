$(document).ready ->
    $("input[name=select]").on "change", changeSelect
    $("button.btn-quotation").on "click", createTmpQuatation
    $("button.btn-purchase").on "click", createTmpPurchase
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
    return data

createTmpQuatation = (event) ->
    data = new Object
    data.details = getListCheck()
    setTimeout ->
        if data.details.length
            $().toastmessage "showToast",
                text: "Desea generar el temporal para la cotización?"
                type: "confirm"
                sticky: true
                buttons: [{value:"Si"}, {value:"No"}]
                success: (result) ->
                    if result is "Si"
                        data.quote = true
                        data.details = JSON.stringify data.details
                        data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
                        $.post "", data, (response) ->
                            if response.status
                                $().toastmessage "showNoticeToast", "se a generado el tmp de cotización."
                                setTimeout ->
                                    href = "/logistics/quote/single/"
                                    return
                                , 2600
                                return
                            else
                                $().toastmessage "showErrorToast", "No se podido crear temp para la cotización."
                                return
                        return
            return
        else
            $().toastmessage "showWarningToast", "No se han encontrado materiales para cotizar."
            return
    , 300
    return

createTmpPurchase = (event) ->
    data = new Object
    data.details = getListCheck()
    setTimeout ->
        if data.details.length
            $().toastmessage "showToast",
                text: "Desea generar el temporal para la orden de compra?"
                type: "confirm"
                sticky: true
                buttons: [{value:"Si"}, {value:"No"}]
                success: (result) ->
                    if result is "Si"
                        data.purchase = true
                        data.details = JSON.stringify data.details
                        data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
                        $.post "", data, (response) ->
                            if response.status
                                $().toastmessage "showNoticeToast", "se a generado el tmp de la orden de compra."
                                setTimeout ->
                                    href = "/logistics/purchase/single/"
                                    return
                                , 2600
                                return
                            else
                                $().toastmessage "showErrorToast", "No se podido crear temp para la compra."
                                return
                        return
            return
        else
            $().toastmessage "showWarningToast", "No se han encontrado materiales para Comprar."
            return
    , 300
    return