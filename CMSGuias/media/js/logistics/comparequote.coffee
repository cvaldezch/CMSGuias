$(document).ready ->
    $(".step-two").hide()
    $("[name=transfer]").datepicker "showAnim": "slide", changeMonth : true, changeYear : true, dateFormat : "yy-mm-dd", minDate : "0"
    $(".btn-refresh-price").on "click", calcPriceEdit
    $("input[name=select]").on "change", changeMaterials
    $(".btn-purchase").on "click", choicePrice
    $(".btn-origin, .btn-edit").on "click", showStepTwo
    $(".btn-back").on "click", showStepOne
    $(".btn-save-purchase").on "click", savePurchase
    $(".btn-kill").on "click", finishQuote
    $(".btn-show-deposit").click (event) ->
        $("[name=deposit]").click()
        return
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
            pre = 0
            if $("#dscto#{supplier}").is(":checked")
                pre = ((parseFloat(input.value) * parseFloat(input.getAttribute("data-discount"))) / 100)
                pre = (parseFloat(input.value) - pre)
            else
                pre = parseFloat(input.value)

            amount += (parseFloat(input.getAttribute("data-quantity")) * pre)
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
        $(".choice-price").modal "show"
        $(".btn-origin, .btn-edit").attr "data-s", @value
    else
        $().toastmessage "showWarningToast", "Debe de seleccionar por lo menos un material para poder generar la orden de compra."
    return

showStepTwo = (event) ->
    $("input[name=prices]").val @value
    $(".choice-price").modal "hide"
    #$(".data-supplier").
    $("[name=rucandreason]").html @getAttribute("data-s") + " - " + $(".get-reason-#{@getAttribute("data-s")}").text()
    $("[name=ruc]").val @getAttribute "data-s"
    $("[name=reason]").val $(".get-reason-#{@getAttribute("data-s")}").text()
    $(".step-one").fadeOut 200
    $(".step-two").fadeIn 800
    return

showStepOne = (event) ->
    $("input[name=prices]").val ""
    $(".step-two").fadeOut 200
    $(".step-one").fadeIn 800
    return

savePurchase = ->
    form = new FormData()
    data = new Object()
    data.proveedor = $("[name=ruc]").val()
    data.lugent = $("[name=delivery]").val()
    data.documento = $("[name=document]").val()
    data.pagos = $("[name=payment]").val()
    data.moneda = $("[name=currency]").val()
    data.traslado = $("[name=transfer]").val()
    data.contacto = $("[name=contact]").val()
    $deposit = $("[name=deposit]").get(0)
    pass = false
    for k, v of data
        if v isnt ""
            form.append k, v
            pass = true
        else
            pass = false
            $().toastmessage "showWarningToast", "El campo #{k} se encuentra vacio."
            return pass
    if pass
        if $deposit.files[0] isnt null
            form.append "deposito", $deposit.files[0]
        arr = new Array()
        type = $("input[name=prices]").val()
        $("input[name=mats]").each (index, element) ->
            data = new Object()
            if element.checked
                data["materials"] = element.value
                ruc = $("[name=ruc]").val()
                $("input[name=edit#{ruc}]").each (index, input) ->
                    if input.getAttribute("data-id") is element.value
                        if type is "origin"
                            data["price"] = parseFloat input.getAttribute "data-price"
                            data["discount"] = parseFloat input.getAttribute "data-discount"
                        else if type is "editable"
                            data["price"] = parseFloat input.getAttribute "data-price" #parseFloat input.value
                            pre = parseFloat(input.getAttribute("data-price"))
                            if parseFloat(input.value) < pre
                                dis = (pre - parseFloat(input.value))
                                dis = ((dis * 100) / pre)
                                if $("#dscto#{ruc}").is(":checked")
                                    data["discount"] = (parseFloat(input.getAttribute("data-discount")) + dis)
                                else
                                    data["discount"] = dis
                            else
                                if $("#dscto#{ruc}").is(":checked")
                                    if parseFloat(input.getAttribute("data-discount")) > 0
                                        data["discount"] = parseFloat(input.getAttribute("data-discount"))
                                    else
                                        data["discount"] = 0
                                else
                                    if parseFloat(input.value) < pre
                                        dis = (pre - parseFloat(input.value))
                                        dis = ((dis * 100) / pre)
                                        data["discount"] = dis
                                    else
                                        data["discount"] = 0
                        data["brand"] = input.getAttribute "data-brand"
                        data["model"] = input.getAttribute "data-model"
                        data["quantity"] = parseFloat input.getAttribute "data-quantity"
                arr.push data
                return
        console.log arr
        form.append "details", JSON.stringify(arr)
        form.append "purchase", true
        form.append "csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val()
        $.ajax
            url : ""
            type : "POST"
            data : form
            dataType : "json"
            cache : false
            processData : false
            contentType : false
            success : (response) ->
                if response.status
                    $().toastmessage "showNoticeToast", "Felicidades! se a generar la <q>Orden de Compra</q> Nro #{response.purchase}"
                    setTimeout ->
                        #location.href = "/logistics/compare/quote/#{$(".btn-kill").val()}/"
                        $("input[name=edit#{$("[name=ruc]").val()}]").attr "disabled","disabled"
                        $(".btn-purchase").each (index, element) ->
                            if element.value == $("[name=ruc]").val()
                                element.setAttribute("disabled","disabled")
                                return
                        showStepOne()
                    , 3000
                else
                    $().toastmessage "showErrorToast", "No se a podido generar la Orden de compra. Vuelva a intentarlo."
    return

finishQuote = (event) ->
    $().toastmessage "showToast",
        sticky : true
        text : "Si terminas la cotización no podra comprar a los otros proveedor(es) que se envio esta cotización. Seguro que desea terminar la cotización?"
        type : "confirm"
        buttons : [{value:"Si"},{value:"No"}]
        success : (result) ->
            if result is "Si"
                $.post "", {"finish":true, "csrfmiddlewaretoken":$("input[name=csrfmiddlewaretoken]").val()}, (response) ->
                    if response.status
                        location.href = "/logistics/quotation/list/"
                        return
                    else
                        $().toastmessage "showWarningToast", "No se puede terminar la cotización, Vuelva a intentarlo."
                        return
                , "json"
            return
    return