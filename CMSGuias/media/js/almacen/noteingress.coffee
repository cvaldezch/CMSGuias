$(document).ready ->
    $("input[name=sdate], input[name=edate]").datepicker "showAnim" : "slide", "dateFormat" : "dd-mm-yy"
    $("button.search").on "click", search
    $("input[name=opsearch]").on "change", changeSearch
    $(document).on "click", ".dropedit", getEditDetails
    $(document).on "click", ".dropanular", getEditDetails
    return

changeSearch = (event) ->
    $(@).each ->
        if @checked
            if @value is "nro"
                $("input[name=number]").attr "disabled", false
                $("[name=status]").val ''
                .attr "disabled", true
                $("[name=sdate], [name=edate]").val ''
                .attr "disabled", true
            if @value is "status"
                $("[name=status]").attr "disabled", false
                $("[name=number]").val ''
                .attr "disabled", true
                $("[name=sdate], [name=edate]").val ''
                .attr "disabled", true
            if @value is "date"
                $("[name=sdate], [name=edate]").attr "disabled", false
                $("[name=number]").val ''
                .attr "disabled", true
                $("[name=status]").val ''
                .attr "disabled", true
    return

search = (event) ->
    $nro = $("input[name=number]")
    $status = $("select[name=status]")
    $sdate = $("input[name=sdate]")
    $edate = $("input[name=edate]")
    context = new Object
    if $nro.val().length == 10
        context.nro = $nro.val()
    if $status.val().length
        context.status = $status.val()
    if $sdate.val().length == 10
        context.sdate = $sdate.val()
    if $edate.val().length == 10
        context.edate = $edate.val()
    if Object.getOwnPropertyNames(context).length
        context.search = true
        $.getJSON "", context, (response) ->
            if response.status
                template = "<td class=\"text-center\">{{ item }}</td>
                        <td class=\"text-center\">{{ ingress }}</td>
                        <td class=\"text-center\">{{ purchase }}</td>
                        <td class=\"text-center\">{{ invoice }}</td>
                        <td class=\"text-center\">{{ register }}</td>
                        <td class=\"text-center\">{{ status }}</td>
                        <td class=\"text-center\">
                            <div class=\"btn-group\">
                                <button type=\"button\" class=\"btn btn-xs btn-success dropdown-toggle\" data-toggle=\"dropdown\" aria-expanded=\"false\">
                                    <span class=\"fa fa-gears\"></span>
                                </button>
                                <ul class=\"dropdown-menu\" role=\"menu\">
                                    <li><a class=\"text-left dropedit\" data-value=\"{{ ingress }}\"><small>Editar</small></a></li>
                                    <li><a class=\"text-left dropanular\" data-value=\"{{ ingress }}\"><small>Anular</small></a></li>
                                </ul>
                            </div>
                        </td>"
                $table = $("table.table-noteingress > tbody")
                $table.empty()
                for x of response.list
                    response.list[x].item = parseInt(x) + 1
                    $table.append Mustache.render template, response.list[x]
                return
            else
                $().toastmessage "showErrorToast", "No se a podido obtener datos. #{response.raise}"
                return
    return

getEditDetails = ->
    value = @getAttribute "data-value"
    if value.length is 10
        context = new Object
        context.ingress = value
        context.details = true
        $.getJSON "", context, (response) ->
            if response.status
                $("input[name=ingress]").val response.ingress
                $("input[name=storage]").val response.storage
                $("input[name=purchase]").val response.purchase
                $("input[name=guide]").val response.guide
                $("input[name=invoice]").val response.invoice
                $("input[name=motive]").val response.motive
                $("input[name=observation]").val response.observation
                $tb = $("table.table-details > tbody")
                $tb.empty()
                template = "<tr>
                                <td>{{ item }}</td>
                                <td>{{ name }} - {{ meter }}</td>
                                <td>{{ brand }}</td>
                                <td>{{ model }}</td>
                                <td>{{ quantity }}</td>
                            </tr>"
                for x of response.details
                    response.details[x].item = parseInt(x) + 1
                    $tb.append Mustache.render template, response.details[x]
                return
            else
                $().toastmessage "showWarningToast", "No se pudo obtener el detalle de la Nota de Ingreso."
                return
        return
    else
        $().toastmessage "showWarningToast", "El código de la nota de ingreso es incorrecto."
    return