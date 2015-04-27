$(document).ready ->
    getMaterialsAll()
    $(".materialsadd").hide()
    $("[name=materials], [name=measure]").chosen
        width: "100%"
    $("[name=materials]").on "change", getmeasure
    $("[name=measure]").on "change", getsummary
    $(".bshowaddmat").on "click", showAddMaterial
    $(".bmrefresh").on "click", refreshMaterials
    $(".btnaddmat").on "click", addMaterials
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
            getmeasure()
    return

getmeasure = (event) ->
    context = new Object
    context.searchMeter = true
    context.name = $("[name=materials]").val()
    $.getJSON "/materials/", context, (response) ->
        if response.status
            $se = $("[name=measure]")
            $se.empty()
            $se.append "<option></option>"
            template = "{{#meter}} <option value=\"{{code}}\">{{measure}}</option> {{/meter}}"
            $se.html Mustache.render template, response
            $se.trigger "chosen:updated"
            setTimeout ->
                getsummary()
            , 200
    return

getsummary = (event) ->
    context = new Object
    context.scode= $("[name=measure]").val()
    context.summary = true
    if context.scode.length is 15
        $.getJSON "/materials/", context, (response) ->
            if response.status
                template = "
                    <table class=\"table table-condensed font-11\">
                        <tbody>
                            <tr>
                                <th>Código</th>
                                <td class=\"matid\">{{ summary.materials }}</td>
                            </tr>
                            <tr>
                                <th>Nombre</th>
                                <td>{{ summary.name }}</td>
                            </tr>
                            <tr>
                                <th>Media</th>
                                <td>{{ summary.measure }}</td>
                            </tr>
                            <tr>
                                <th>Unidad</th>
                                <td>{{ summary.unit }}</td>
                            </tr>
                        </tbody>
                    </table>"
                $s = $("[name=summary]")
                $s.empty()
                $s.html Mustache.render template, response
                $("[name=mprice]").val response.summary.price
                return
    else
        $().toastmessage "showWarningToast", "El código del material no es valido."
    return

showAddMaterial = (event) ->
    if $(".materialsadd").is(":visible")
        $(@).removeClass "btn-warning"
        .addClass "btn-default"
        $(".materialsadd").hide 800
    else
        $(@).removeClass "btn-default"
        .addClass "btn-warning"
        $(".materialsadd").show 800
    return

addMaterials = (event) ->
    context = new Object()
    context.materials = $(".matid").text()
    context.quantity = $("[name=mquantity]").val()
    context.price = $("[name=mprice]").val()
    if context.materials.length is 15
        if context.quantity isnt ""
            if context.price isnt ""
                context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
                context.addMaterials = true
                $.post "", context, (response) ->
                    if response.status
                        getListMaterials()
                        return
                    else
                        $().toastmessage "showErrorToast", "Error al guardar los cambios. #{response.raise}"
                        return
                , "json"
            else
                $().toastmessage "showWarningToast", "Precio invalido."
        else
            $().toastmessage "showWarningToast", "Cantidad invalida."
    else
        $().toastmessage "showWarningToast", "Código de material incorrecto."
    return

getListMaterials = (event) ->
    context = new Object
    context.listMaterials = true
    $.getJSON "", context, (response) ->
        if response.status
            $tbl = $(".tmaterials tbody")
            $tbl.empty()
            template = "{{#materials}}<tr><td>{{index}}</td><td>{{code}}</td><td>{{name}}</td><td>{{unit}}</td><td>{{quantity}}</td><td>{{price}}</td><td>{{partial}}</td><td class=\"text-center\"><button class=\"btn btn-default btn-xs\"><span class=\"fa fa-edit\"></span></button></td><td class=\"text-center\"><button class=\"btn btn-default btn-xs\"><span class=\"fa fa-trash\"></span></button></td></tr>{{/materials}}"
            counter = 1
            response.index = ->
                return counter++
            $tbl.html Mustache.render template, response
            return
        else
            $().toastmessage "showErrorToast", "Error al Obtener la lista. #{response.raise}."
            return
    return

refreshMaterials = (event) ->
    getMaterialsAll()
    getListMaterials()
    return