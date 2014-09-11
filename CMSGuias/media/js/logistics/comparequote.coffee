$(document).ready ->
    $(".btn-refresh-price").on "click", calcPriceEdit
    $("input[name=select]").on "change", changeMaterials
    $(".btn-purchase").on "click", choicePrice
    calcamounts()
    return

calcamounts = (event) ->
    $("input[name=suppliers]").each (index, supplier)->
        amount = 0
        $("input[name=edit#{supplier.value}]").each (index, input) ->
            amount += parseFloat input.getAttribute "data-amount"
            return
        $(".amount#{supplier.value}").html amount.toFixed 2
        igv = (amount * (parseFloat($("input[name=igv]").val())/100))
        $(".igv#{supplier.value}").html igv.toFixed 2
        total = (amount + igv)
        $(".total#{supplier.value}").html total.toFixed 2
        return
    return

calcPriceEdit = (event) ->
    if @value isnt ""
        supplier = @value
        amount = 0
        $("input[name=edit#{supplier}]").each (index, input) ->
            amount += (parseFloat(input.getAttribute("data-quantity")) * parseFloat(input.value))
            return
        $(".amountedit#{supplier}").html amount.toFixed 2
        igv = (amount * (parseFloat($("input[name=igv]").val())/100))
        $(".igvedit#{supplier}").html igv.toFixed 2
        total = (amount + igv)
        $(".totaledit#{supplier}").html total.toFixed 2
        return
    return

changeMaterials = (event) ->
    if @checked
        val = Boolean parseInt @value
        $("input[name=mats]").each (index, element) ->
            element.checked = val
            return
    return

choicePrice = ->
    counter = 0
    $("input[name=mats]").each (index, element) ->
        if element.checked
            counter += 1
            return
    if counter > 0
        $(".choice-price").modal "toggle"
        $(".btn-origin, .btn-edit").val @value
    else
        $().toastmessage "showWarningToast", "Debe de seleccionar por lo menos un material para poder generar la orden de compra."
    return