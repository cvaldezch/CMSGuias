$(document).ready ->
    $(".bedside-after, .panel-bedside").hide()
    $("input[name=dates], input[name=traslado], input[name=validez]").datepicker "minDate" : "0", "dateFormat" : "yy-mm-dd", "showAnim" : "slide"
    $(document).on "blur", "input[name=prices], input[name=desct]", saveBlurDigit
    $(document).on "blur", "input[name=brands], input[name=models]", saveBlurString
    $(document).on "change", "input[name=dates]", saveBlurString
    $(".btn-file").on "click", showBrowser
    $(document).on "change", "input[name=sheettech]", uploadSheet
    calcTotals()
    $(".btn-show-bedside").on "click", showBedsideAfter
    $(".btn-cancel").on "click", showBedsideBefore
    $(".btn-send").on "click", saveBedside
    tinymce.init
        selector: "textarea[name=obser]",
        theme: "modern",
        menubar: false,
        statusbar: false,
        plugins: "link contextmenu fullscreen",
        fullpage_default_doctype: "<!DOCTYPE html>",
        font_size_style_values : "10px,12px,13px,14px,16px,18px,20px",
        toolbar1: "styleselect | fontsizeselect | fullscreen |"
        toolbar2: "undo redo | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent |"
    setTimeout ->
        $(document).find("div#mceu_2").click (event) ->
            if $(@).attr("aria-pressed") is "false" or $(@).attr("aria-pressed") is undefined
                $(".navbar").hide()
            else if $(@).attr("aria-pressed") is "true"
                $(".navbar").show()
            return
    , 2000
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
    if not isNaN parseFloat @value
        btn = @
        data = new Object()
        data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
        if @name is "prices"
            data.blur = "price"
        else if @name is "desct"
            data.blur = "desct"
        data.val = parseFloat @value
        data.materials = @getAttribute "data-mat"
        $.post "", data, (response) ->
            console.log response
            if response.status
                $td = $("table > tbody > tr.#{btn.getAttribute "data-mat"} > td")
                quantity = response.quantity
                if data.blur is "desct"
                    price = parseFloat $td.eq(4).find("input").val()
                    discount = parseFloat data.val
                else
                    price = parseFloat data.val
                    discount = parseFloat if $td.eq(5).find("input").val() is "" then 0 else $td.eq(5).find("input").val()
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

saveBlurString = (event) ->
    console.log @value
    if $.trim(@value) and $.trim(@value) isnt "None"
        data = new Object()
        data.val = @value
        data.blur = @name
        data.materials = @getAttribute "data-mat"
        data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
        $.post "", data
    return

showBrowser = (event) ->
    $("input[name=sheettech]").click()
    .attr "data-mat", @value
    return

uploadSheet = (event) ->
    if $.trim(@getAttribute "data-mat") isnt "" and @files[0] isnt null
        input = @
        data = new FormData()
        data.append "type", "file"
        data.append "materials", @getAttribute "data-mat"
        data.append "sheet", @files[0]
        data.append "csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val()
        $.ajax
            url : ""
            data : data
            type : "POST"
            dataType : "json"
            cache : false
            contentType : false
            processData : false
            success : (response) ->
                console.log response
                if not response.status
                    $().toastmessage "showWarningToast", "No se a podido cargar la hoja técnica. #{response.raise}"

                $file = $(input)
                $file.attr "data-mat", ""
                $file.val ""
                clon = $file.clone()
                $file.replaceWith(clon)
                #$file.attr "data-mat", ""
    else
        @setAttribute = ""
    return

showBedsideAfter = (event) ->
    $(".bedside-after, .panel-bedside").show 600
    $(".bedside-before").hide 200

showBedsideBefore = (event) ->
    $(".bedside-after, .panel-bedside").hide 200
    $(".bedside-before").show 600
    return

saveBedside = (event) ->
    data = new Object()
    data.traslado = $("input[name=traslado]").val()
    data.validez = $("input[name=validez]").val()
    data.moneda = $("select[name=moneda]").val()
    data.contacto = $("input[name=contact]").val()
    data.obser = $("#obser_ifr").contents().find("body").html()
    if data.traslado.length == 10 and data.traslado isnt "" and data.validez.length is 10 and data.validez isnt "" and data.moneda isnt ""
        data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
        data.client = true
        $.post "", data, (response) ->
            if response.status
                console.log(response)
                data = new Object()
                data.texto = "System<br><br>Se a respondido a la cotización Nro #{response.quote} del proveedor RUC #{response.supplier} #{response.reason}<br><br><br>---------------------------------<br><strong>System ICR PERU S.A.</strong>"
                data.para = "logistica@icrperusa.com"
                data.asunto = "Respuesta de Cotización"
                parameter = $.param data
                url = "http://190.41.246.91:3000/?#{ parameter }"
                windowmsg = window.open url, "Send Msg", "toolbar=no, scrollbars=no, resizable=no, width=100, height=100"
                setTimeout ->
                    windowmsg.close()
                    return
                , 8000
                $().toastmessage "showNoticeToast", "Se ha guardado y enviado la cotización."
                setTimeout ->
                    location.reload()
                , 2600
        return
    else
        $().toastmessage "showWarningToast", "Existe un campo vacio o con formato incorrecto, revise y vuelva a intentarlo."
    return