$(document).ready ->
    # block search materials
    $(".panel-add,input[name=read],.step-second").hide()
    $("input[name=description]").on "keyup", keyDescription
    $("input[name=description]").on "keypress", keyUpDescription
    $("select[name=meter]").on "click", getSummaryMaterials
    $("input[name=code]").on "keypress", keyCode
    # endblock
    $(".panel-add-mat, .view-full").hide()
    $(".btn-show-mat").on "click", openAddMaterial
    $("input[name=plane]").on "change", uploadPlane
    $(".btn-show-planes").on "click", panelPlanes
    $("[name=show-full]").on "click", viewFull
    $("[name=plane-del]").on "click", delPlane
    $("[name=show-plane]").on "click", (event) ->
        $("input[name=plane]").click()
    return

# block get Materiales
keyDescription = (event) ->
    key = `window.Event ? event.keyCode : event.which`
    if key isnt 13 and key isnt 40 and key isnt 38 and key isnt 39 and key isnt 37
        getDescription @value.toLowerCase()
    if key is 40 or key is 38 or key is 39 or key is 37
        moveTopBottom key
    return

keyCode = (event) ->
    key = if window.Event then event.keyCode else event.which
    if key is 13
        searchMaterialCode @value

searchMaterial = (event) ->
    desc = $("input[name=description]").val()
    code = $("input[name=code]").val()
    if code.length is 15
        searchMaterialCode code
    else
        getDescription $.trim(desc).toLowerCase()

# endBlock

openAddMaterial = (event) ->
    event.preventDefault()
    $(".panel-add-mat").toggle ->
        if $(".btn-show-mat").is(":hidden")
            $(@).find("span").removeClass "glyphicon-chevron-up"
            .addClass "glyphicon-chevron-down"
        else
            $(".btn-show-mat").find("span").removeClass "glyphicon-chevron-down"
            .addClass "glyphicon-chevron-up"
    return

uploadPlane = (event) ->
    console.log @files[0]
    if @files[0] isnt null
        data = new FormData()
        data.append("type", "plane")
        data.append("files", @files[0])
        data.append("proyecto", $("input[name=pro]").val())
        data.append("subproyecto", $("input[name=sub]").val())
        data.append("sector", $("input[name=sec]").val())
        data.append("csrfmiddlewaretoken", $("[name=csrfmiddlewaretoken]").val())
        $.ajax
            data : data,
            url : "",
            type : "POST",
            dataType : "json",
            cache : false,
            processData: false,
            contentType: false,
            success : (response) ->
                if response.status
                    location.reload()
                else
                    $().toastmessage "showErrorToast", "No se ha cargado un archivo."
    else
        $().toastmessage "showWarningToast", "No se ha cargado un archivo."
    return

panelPlanes = (event) ->
    btn = @
    $(".panel-planes > .panel-body").toggle ->
        if $(".panel-planes > .panel-body").is(":hidden")
            $(btn).find("span").removeClass "glyphicon-chevron-up"
            .addClass "glyphicon-chevron-down"
        else
            $(btn).find("span").removeClass "glyphicon-chevron-down"
            .addClass "glyphicon-chevron-up"
    return

viewFull = (event) ->
    btn = @
    $(".view-full").toggle ->
        if $(@).is(":hidden")
            $(".navbar").show "blind", 600
            return
        else
            $(".navbar").hide "blind", 600
            $("#planefull").attr "src", btn.value
            # $("#planefull").reload()
            return
    return

delPlane = (event) ->
    data = new Object()
    data.type = "delplane"
    data.files = @value
    data.pro = $("input[name=pro]").val()
    data.sub = $("input[name=sub]").val()
    data.sec = $("input[name=sec]").val()
    data.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
    $().toastmessage "showToast",
        "text" : "Desea eliminar el <q>Plano</q>?"
        "type" : "confirm"
        "sticky" : true
        buttons : [{value:'Si'},{value:'No'}]
        success : (result) ->
            if result is "Si"
                $.post "", data, (response) ->
                    if response.status
                        location.reload()
                    else
                        $().toastmessage "showWarningToast", "Error, al eliminar el plano."
    return