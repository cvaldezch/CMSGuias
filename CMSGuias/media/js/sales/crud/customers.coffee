$(document).ready ->
    $("input,select").attr "class", "form-control input-sm"
    $("select[name=pais]").on "change", getDepartamentOption
    $("select[name=departamento]").on "change", getProvinceOption
    $("select[name=provincia]").on "change", getDistrictOption
    $("button.btn-search").on "click", getDataRUC
    setTimeout ->
        $("input[name=ruccliente_id]").on "keyup change", (event) ->
            if @value.length is 11
                getDataRUC()
                return
    , 1500
    if $(".alert-success").is(":visible")
        setTimeout ->
            window.close()
            return
        , 2600
    return

getDataRUC = ->
    ruc = $("input[name=ruccliente_id]").val()
    if ruc.length is 11
        data = new Object()
        data.ruc = ruc
        data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
        #data.capcha = $("input[name=capcha]").val()
        $.post "/json/restful/data/ruc/", data, (response) ->
            console.log response
            if response.status
                $("input[name=razonsocial]").val response.reason
                $("[name=direccion]").val response.address
                $("input[name=telefono]").val response.phone
            else
                $().toastmessage "showWarningToast", "No se a encontrado el Proveedor."
        , "json"
        return
    else
        $().toastmessage "showWarningToast", "El numero de ruc es invalido!"
    return