$(document).ready ->
    $("[name=dates],[name=datee]").datepicker "changeMonth": true, "changeYear": true, "showAnim": "slide", "dateFormat": "yy-mm-dd"
    $("[name=search]").on "change", changeradio
    $(".btn-search").on "click", searchquote
    $(".btn-view").on "click", viewReport
    $(".btn-show-send").on "click", showMessage
    $(".btn-send").on "click", sendMessages
    $(".btn-del").on "click", annularQuote
    init()
    return

init = ->
    tinymce.init
        selector: "textarea[name=text]",
        height: 200,
        theme: "modern",
        menubar: false,
        statusbar: false,
        plugins: "link contextmenu",
        font_size_style_values : "10px,12px,13px,14px,16px,18px,20px",
        toolbar: "undo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | fontsizeselect"
    return

changeradio = (event)->
    event.preventDefault()
    $(@).each ->
        if @checked
            if @value is "code"
                $("[name=code]").attr "disabled", false
                $("[name=dates],[name=datee]").attr "disabled", true
                return
            else if @value is "dates"
                $("[name=dates],[name=datee]").attr "disabled", false
                $("[name=code]").attr "disabled", true
                return
    return

searchquote = (event) ->
    event.preventDefault()
    data = {}
    pass = false
    # validate fileds search
    $("[name=search]").each ->
        if @checked
            if @value is "code"
                if $("[name=code]").val() is ""
                    $("[name=code]").focus()
                    $().toastmessage "showWarningToast", "Campo vacio, este campo no puede estar vacio."
                else
                    pass = true
                    data = "by": "code", "code": $("[name=code]").val()
                return
            else if @value is "dates"
                $("[name=dates],[name=datee]").each ->
                    if @name is "datee"
                        data.datee = @value
                        return true
                    if @value is ""
                        @focus()
                        $().toastmessage "showWarningToast", "Campo vacio, este campo no puede estar vacio."
                        return false
                    else
                        pass = true
                        data = "by": "dates", "dates": @value
                        return
                return
    if pass
        $.getJSON '', data, (response) ->
            if response.status
                template = """
                            <tr>
                            <td>{{ item }}</td>
                            <td>{{ cotizacion_id }}</td>
                            <td>{{ proveedor_id }}</td>
                            <td>{{ razonsocial }}</td>
                            <td>{{ keygen }}</td>
                            <td>{{ traslado }}</td>
                            <td>
                                <button class="btn btn-xs btn-link text-blue"><span class="glyphicon glyphicon-eye-open"></span></button>
                            </td>
                            <td>
                                <button class="btn btn-xs btn-link text-green"><span class="glyphicon glyphicon-envelope"></span></button>
                            </td>
                            <td>
                                <button class="btn btn-xs btn-link text-red"><span class="glyphicon glyphicon-fire"></span></button>
                            </td>
                            </tr>
                            """
                $tb = $("table > tbody")
                $tb.empty()
                for k of response.list
                   response.list[k].item = (parseInt(k) + 1)
                   $tb.append Mustache.render template, response.list[k]

                return
    return

viewReport = (event) ->
    quote = @value
    supplier = $(@).attr "data-sup"
    pass = false
    if quote is ""
        $().toastmessage "showWarningToast", "no se puede mostrar el report: fatal id quote."
        return false
    else
        pass = true
    if supplier is ""
        $().toastmessage "showWarningToast", "no se puede mostrar el report: fatal id supplier."
        return false
    else
        true
    if pass
        url = "/reports/quote/#{quote}/#{supplier}"
        window.open url, "_blank"
    return

showMessage = (event) ->
    event.preventDefault()
    quote = $(@).val()
    name = $(@).attr "data-name"
    key = $(@).attr "data-key"
    mail = $(@).attr "data-mail"
    if quote isnt "" and name isnt "" and key isnt ""
        text = "
                <p>Estimados Sres. #{ name }:</p>
                <p>Le enviamos la url con el cual prodrán acceder a nuestra cotización.</p>
                <p>Tambien le proporcionamos una clave para poder mostrar la cotización, el número de <strong>cotización</strong> y la <strong>clave</strong> son:</p>
                <p><strong>Nro Cotización:</strong> #{ quote }</p>
                <p><strong>AutoKey : </strong> #{ key }</p>
                <p>Uds. puedén acceder directamente a nuestro sitio web desde estos enlaces:</p>
                <ul><li>Presione <a href=\"http://190.41.246.91/proveedor/\" data-mce-href=\"http://190.41.246.91/proveedor/\" target=\"_blank\" title=\"ICR PERU SA\">aquí</a> para ir al sitio web.<br></li><li><a title=\"ICR PERU SA\" href=\"http://190.41.246.91/proveedor/\" target=\"_blank\" data-mce-href=\"http://190.41.246.91/proveedor/\">http://190.41.246.91/proveedor/</a></li></ul>
                <p><br data-mce-bogus=\"1\"></p>
                <p>Saludos.</p>
                <p><br data-mce-bogus=\"1\"></p>
                <p><strong>Dpto. Logística ICR PERU S.A.</strong></p>
                <p><strong><br data-mce-bogus=\"1\"></strong></p>
                <p>---------------------------------<strong style=\"color: rgb(34, 34, 34); font-family: arial, sans-serif; font-size: 13px;\" data-mce-style=\"color: rgb(34, 34, 34); font-family: arial, sans-serif; font-size: 13px;\"><br></strong><strong style=\"color: rgb(34, 34, 34); font-family: arial, sans-serif; font-size: 13px;\" data-mce-style=\"color: rgb(34, 34, 34); font-family: arial, sans-serif; font-size: 13px;\">Patricia Barbaran ✔<br>Dpto. Logística.</strong><br style=\"color: rgb(34, 34, 34); font-family: arial, sans-serif; font-size: 13px;\" data-mce-style=\"color: rgb(34, 34, 34); font-family: arial, sans-serif; font-size: 13px;\"><span style=\"color: rgb(34, 34, 34); font-family: arial, sans-serif; font-size: 13px;\" data-mce-style=\"color: rgb(34, 34, 34); font-family: arial, sans-serif; font-size: 13px;\">Telef.: 371-0443</span><br style=\"color: rgb(34, 34, 34); font-family: arial, sans-serif; font-size: 13px;\" data-mce-style=\"color: rgb(34, 34, 34); font-family: arial, sans-serif; font-size: 13px;\"><span style=\"color: rgb(34, 34, 34); font-family: arial, sans-serif; font-size: 13px;\" data-mce-style=\"color: rgb(34, 34, 34); font-family: arial, sans-serif; font-size: 13px;\">Nextel: 121 * 7860</span><strong><br data-mce-bogus=\"1\"></strong></p>
                "
        $("#text_ifr").contents().find("body").html(text)
        $("input[name=for]").val mail
        $("input[name=issue]").val "COTIZACIÓN #{ quote }"
        $(".mmail").modal "show"
        return
    else
        $().toastmessage "showWarningToast", "Fail: Not show message, field empty."
        return

sendMessages = ->
    $for = $("input[name=for]")
    if $for.val() isnt ""
        data = {}
        data.texto = $("#text_ifr").contents().find("body").html()
        data.para = $("input[name=for]").val()
        data.asunto = $("input[name=issue]").val()
        parameter = $.param data
        url = "http://190.41.246.91:3000/?#{ parameter }"
        windowmsg = window.open url, "Send Msg", "toolbar=no, scrollbars=no, resizable=no, width=100, height=100"
        $(".mmail").modal "hide"
        setTimeout ->
            windowmsg.close()
            return
        , 8000


annularQuote = (event)->
    quote = @value
    supplier = $(@).attr "data-sup"
    if quote isnt ""
        $().toastmessage "showToast",
            "sticky":true,
            "text": "Desea anular la solicitud de Cotización #{quote} para el proveedor #{supplier}?",
            "type": "confirm",
            "buttons": [{"value":"No"},{"value":"Si"}],
            "success": (result) ->
                if result is "Si"
                    $.post "",
                        "quote": quote,
                        "supplier": supplier,
                        "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val(),
                        (response) ->
                            if response.status
                                $("##{quote}#{supplier}").remove()
                                return
                        , "json"
                    return
    else
        $().toastmessage "showWarningToast", "No se a encontrado el nro de cotización."
    return