$(document).ready ->
    getMaterialsAll()
    $("[name=materials], [name=measure]").chosen
        width: "100%"
    $("[name=materials]").on "change", getmeasure
    $("[name=measure]").on "change", getsummary
    return

getMaterialsAll = (event) ->
    context = new Object()
    context.searchName = true
    context.name = ''
    $.getJSON "/materials/", context, (response) ->
        if response.status
            $op = $("[name=materials]")
            $op.empty()
            template = "{{#names}}<option value=\"{{ name }}\">{{ name }}</option>{{/names}}"
            $op.html Mustache.render template, response
            $op.trigger "chosen:updated"
    return

getmeasure = (event) ->
    #console.log @value
    context = new Object
    context.searchMeter = true
    context.name = @value
    $.getJSON "/materials/", context, (response) ->
        if response.status
            $se = $("[name=measure]")
            $se.empty()
            $se.append "<option></option>"
            template = "{{#meter}} <option value=\"{{code}}\">{{measure}}</option> {{/meter}}"
            $se.html Mustache.render template, response
            $se.trigger "chosen:updated"
    return

getsummary = (event) ->
    context = new Object
    context.scode= $("[name=measure]").val()
    context.summary = true
    if context.scode.length is 15
        $.getJSON "/materials/", context, (response) ->
            if response.status
                template = "
                    <table class=\"table table-condensed\">
                        <tbody>
                            <tr>
                                <th>Código</th>
                                <td>{{ summary.materiales_id }}</td>
                            </tr>
                            <tr>
                                <th>Nombre</th>
                                <td>{{ summary.matnom }}</td>
                            </tr>
                            <tr>
                                <th>Unidad</th>
                                <td>{{ summary.unidad__uninom }}</td>
                            </tr>
                        </tbody>
                    </table>"
                $s = $("[name=summary]")
                $s.empty()
                #console.log response.summary.materiales_id
                $s.html Mustache.render template, response
                return
    else
        $().toastmessage "showWarningToast", "El código del material no es valido."
    return