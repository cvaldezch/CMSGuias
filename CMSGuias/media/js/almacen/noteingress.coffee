$(document).ready ->
    $("input[name=sdate], input[name=edate]").datepicker "showAnim" : "slide", "dateFormat" : "dd-mm-yy"
    $("button.search").on "click", search
    $("input[name=opsearch]").on "change", changeSearch
    return

changeSearch = (event) ->
    $(@).each ->
        if @checked
            if @value is "nro"
                @setAttribute "disabled", false
                $("[name=status]").val ''
                $("[name=sdate], [name=edate]").val ''
            if @value is "status"
                $("[name=number]").val ''
                $("[name=sdate], [name=edate]").val ''
            if @value is "date"
                $("[name=number]").val ''
                $("[name=status]").val ''
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
        $.getJSON "", context, (response) ->
            if response.status
                template = "<td class=\"text-center\">{{ item }}</td>
                        <td>{{ ingress_id }}</td>
                        <td>{{ purchase_id }}</td>
                        <td>{{ invoice }}</td>
                        <td>{{ register }}</td>
                        <td>{{ status }}</td>"
                $table = $("table.table-noteingress > tbody")
                $table.empty()
                for x of response.list
                    response.list[x].item = parseInt(x) + 1
                    $table.append Mustache.render template, response.list[x]
                    return
            else
                $().toastmessage "showToastError", "No se a podido obtener datos. #{response.raise}"
                return
    return