$(document).ready ->
    $("[name=dates],[name=datee]").datepicker "changeMonth": true, "changeYear": true, "showAnim": "slide", "dateFormat": "yy-mm-dd"
    $("[name=search]").on "change", changeradio
    $(".btn-search").on "click", searchquote
    $(".btn-view").on "click", viewReport
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