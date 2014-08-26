$(document).ready ->
    $("input[name=dates]").datepicker "minDate" : "0", "dateFormt" : "yy-mm-dd", "showAnim" : "slide"
    $(document).on "blur", "input[name=prices], input[name=desct]", saveBlurDigit
    calcTotals()
    return

validMinandMax = (item) ->
    if $.trim(item.value) isnt ""
        if parseFloat($.trim(item.value)) >= parseInt(item.getAttribute "min") and parseFloat($.trim(item.value)) <= parseInt(item.getAttribute "max")
            return true
        else
            item.value = item.getAttribute "min"
            return false
    else
        item.value = item.getAttribute "min"
        # $().toastmessage "showWarningToast", "Debe de ingresar un digito."
        return false
    return

saveBlurDigit = (event) ->
    validMinandMax(@)
    if isNaN(@value)
        data = new Object()
        data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
        if @name is "prices"
            data.blur = "price"
        else if @name is "desct"
            data.blur = "desct"
        data.val = @value
        $.post "", data, (response) ->
            console.log response
            if response.status
                $td = $("table > tbody > tr.#{@getAttribute "data-mat"} > td")
                quantity = response.quantity
                if data.blur is "desct"
                    price = parseFloat $td.eq(4).val()
                    discount = parseFloat data.val
                else
                    price = parseFloat data.val
                    discount = parseFloat if $td.eq(5).val() is "" then 0 else $td.eq(5).val()
                discount = (price - ((price * discount) / 100))
                amount = (quantity * discount)
                $td.eq(6).text amount.toFixed(2)
                calcTotals()
        return
    return

calcTotals = ->
    amount = 0
    $("table > tbody > tr").each (index, element)->
        amount += parseFloat $(element).find("td").eq(6).text()
        return
    cigv = parseInt $("input[name=igv]").val()
    igv = ((amount * cigv) / 100)
    totals = (amount + igv)
    $(".subtc").text amount.toFixed 2
    $(".igvc").text igv.toFixed 2
    $(".totalc").text totals.toFixed 2
    return