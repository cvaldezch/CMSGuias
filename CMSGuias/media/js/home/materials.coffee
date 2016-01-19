$(document).ready ->
    $(".panel-new").hide()
    $("button.btn-top-page").on "click", goTopPage
    $("input[name=searchCode]").on "keyup", searchCode
    $("input[name=searchDesc]").on "keyup", searchDesc
    $(document).on "click", "button[name=btnedit]", showEditMaterials
    $("button.btn-show-new").on "click", showNewMaterials
    $("button.btn-save-material").on "click", saveMaterials
    $("button.btn-save-edit").on "click", editMaterials
    $(document).on "click", "button[name=btndel]", delMaterial
    $('table').floatThead
        useAbsolutePositioning: false
        scrollingTop: 50
    return

searchCode = (event)->
    key = event.keyCode or event.which
    if key is 13
        data = new Object
        data.searchCode = true
        data.code = $.trim @value
        $.getJSON "", data, (response) ->
            if response.status
                addResultTable response
    return

searchDesc = (event) ->
    key = event.keyCode or event.which
    if key is 13
        data = new Object
        data.searchDesc = true
        data.desc = $.trim @value
        $.getJSON "", data, (response) ->
            if response.status
                addResultTable response
    return

addResultTable = (response) ->
    template = """{{#list}}<tr>
                <td class="text-center">{{ index }}</td>
                <td class="text-center">{{ materials }}</td>
                <td>{{ name }}</td>
                <td>{{ measure }}</td>
                <td class="text-center">{{ unit }}</td>
                <td>{{ finished }}</td>
                {{#user}}
                <td>{{ area }}</td>
                <td class="text-center">
                    <button value="{{ materials }}" data-des="{{ name }}" data-met="{{ measure }}" data-unit="{{ unit }}" data-acb="{{ finished }}" data-area="{{ area }}" class="btn btn-xs btn-link text-black" name="btnedit">
                        <span class="fa fa-edit"></span>
                    </button>
                </td>
                <td class="text-center">
                    <button class="btn btn-xs btn-link text-red" name="btndel" value="{{ materials }}" data-name="{{ name }}" data-measure="{{ measure }}" >
                        <span class="fa fa-trash-o"></span>
                    </button>
                </td>
                {{/user}}
                </tr>{{/list}}"""
    $tb = $("table > tbody")
    $tb.empty()
    count = 1
    response.index = -> return count++
    $tb.html Mustache.render template, response
    # for x of response.list
    #     response.list[x].item = parseInt(x) + 1
    #     $tb.append Mustache.render template, response.list[x]
    return

showNewMaterials = (event) ->
    $btn = $(@)
    $(".panel-new").toggle "slow", ->
        if @style.display is 'block'
            $btn.removeClass "btn-primary"
            .addClass "btn-default"
            .find "span"
            .eq 0
            .removeClass "fa-plus"
            .addClass "fa-times"
            $btn.find "span"
            .eq 1
            .text "Cancelar"
        else
            $btn.removeClass "btn-default"
            .addClass "btn-primary"
            .find "span"
            .eq 0
            .removeClass "fa-times"
            .addClass "fa-plus"
            $btn.find "span"
            .eq 1
            .text "Numero Material"
            #$('table').floatThead('reflow')
        $('table').floatThead('reflow')
    return

showEditMaterials = (event) ->
    $("button.btn-save-edit").val @value
    $("input[name=ematnom]").val @getAttribute "data-des"
    $("input[name=ematmed]").val @getAttribute "data-met"
    $("input[name=eunidad]").val @getAttribute "data-unit"
    $("input[name=ematacb]").val @getAttribute "data-acb"
    $("input[name=ematare]").val @getAttribute "data-area"
    $(".meditmat").modal "show"
    return

saveMaterials = (event) ->
    data = new Object
    data.materiales_id = $("input[name=materials]").val()
    data.matnom = $("input[name=matnom]").val()
    data.matmed = $("input[name=matmed]").val()
    data.unidad = $("select[name=unidad]").val()
    data.matacb = $("input[name=matacb]").val()
    data.matare = $("input[name=matare]").val()
    if data.materiales_id is "" and data.materiales_id.length < 15
        $().toastmessage "showWarningToast", "El Código de material no es correcto."
        return false
    if data.matnom is ""
        $().toastmessage "showWarningToast", "Debe de ingresar una descripcion para el material."
        return false
    if data.matmed is ""
        $().toastmessage "showWarningToast", "Debe de ingresar un diametro para el material."
        return false
    if data.unidad is ""
        $().toastmessage "showWarningToast", "Debe de ingresar una unidad para el material."
        return false
    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
    data.exists = true
    $.post "", data, (exists) ->
        if not exists.status
            delete data.exists
            data.saveMaterial = true
            $.post "", data, (response) ->
                if response.status
                    $("input[name=searchCode]").val data.materiales_id
                    .trigger jQuery.Event "keyup", which: 13
                    $("button.btn-show-new").trigger "click"
                    $("input[name=materials]").val ""
                    $("input[name=matnom]").val ""
                    $("input[name=matmed]").val ""
                    $("input[name=matacb]").val ""
                    $("input[name=matare]").val ""
                    return
            , "json"
            return
        else
            $().toastmessage "showWarningToast", "El codigo de material que esta intentando ingresar ya existe!."
    , "json"
    return

editMaterials = (event) ->
    data = new Object
    data.materiales_id = @value
    data.matnom = $("input[name=ematnom]").val()
    data.matmed = $("input[name=ematmed]").val()
    data.unidad = $("select[name=eunidad]").val()
    data.matacb = $("input[name=ematacb]").val()
    data.matare = $("input[name=ematare]").val()
    if data.materiales_id is "" and data.materiales_id.length < 15
        $().toastmessage "showWarningToast", "El Código de material no es correcto."
        return false
    if data.matnom is ""
        $().toastmessage "showWarningToast", "Debe de ingresar una descripcion para el material."
        return false
    if data.matmed is ""
        $().toastmessage "showWarningToast", "Debe de ingresar un diametro para el material."
        return false
    if data.unidad is ""
        $().toastmessage "showWarningToast", "Debe de ingresar una unidad para el material."
        return false
    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
    data.saveMaterial = true
    data.edit = true
    $.post "", data, (response) ->
        if response.status
            $("input[name=searchCode]").val data.materiales_id
            .trigger jQuery.Event "keyup", which: 13
            $("input[name=ematnom]").val ""
            $("input[name=ematmed]").val ""
            $("input[name=ematacb]").val ""
            $("input[name=ematare]").val ""
            $(".meditmat").modal "hide"
            return
    , "json"
    return

delMaterial = (event) ->
    btn = @
    $().toastmessage "showToast",
        text: "Realmente desea Eliminar el material: #{@getAttribute "data-name"} #{@getAttribute "data-measure"}"
        sticky: true
        type: "confirm"
        buttons: [{value:'Si'},{value:'No'}]
        success: (result) ->
            if result is "Si"
                data = new Object
                data.materials = btn.value
                data.delete = true
                data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
                $.post "", data, (response) ->
                    if response.status
                        location.reload()
                , "json"
                return
    return