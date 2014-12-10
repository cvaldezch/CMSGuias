$(document).ready ->
    $(".btn-erase-fields,.btn-generate").hide()
    $("input[name=start],input[name=execution]").datepicker
        changeMonth: true
        changeYear: true
        closeText: "Cerrar"
        dateFormat: "yy-mm-dd"
        showAnim: "slide"
        showButtonPanel: true
    $("select[name=project]").on "click", selectProject
    return

selectProject = (event) ->
    $pro = $(@)
    if $pro.val()
        data = new Object
        data.pro = $pro.val()
        data.changeProject = true
        $.getJSON "", data, (response) ->
            if response.status
                $sub = $("[name=subproject]")
                $sub.empty()
                if response.subprojects
                    tmp = "<option value=\"{{ id }}\">{{ x.subproject }}</option>"
                    for x of response.subprojects
                        $sub.append Mustache.render tmp, response.subprojects[x]
                $("input[name=arrival]").val response.address
                return
            else
                $().toastmessage "showErrorToast", "No se a encontrado Proyectos. #{response.raise}"
                return
    return