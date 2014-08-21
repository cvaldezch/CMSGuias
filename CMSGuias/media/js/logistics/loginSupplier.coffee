$(document).ready ->
    $("select[name=proveedor]").on "click", getDataProveedor
    $(".btn-default").on "click", openSupplier
    return

getDataProveedor = ->
    if @value isnt ""
        data =  new Object()
        data.ruc = @value
        data.exists = true
        $.getJSON "", data, (response)->
            if response.status
                $("input[name=username]").val response.username
                return
            $("input").attr "disabled", false
    return

openSupplier = ->
    url = "/logistics/crud/create/supplier/"
    win = window.open url, "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600"
    interval = window.setInterval ->
        if win == null or win.closed
            window.clearInterval interval
            location.reload
            return
    , 1000
    return win

save_or_update_username = ->
    data = new Object()
    data.username = $("input[name=username]").val()
    data.supplier = $("select[name=proveedor]").val()
    data.password = $("input[name=passwd]").val()
    confirm = $("input[name=confirm]").val()
    if data.supplier isnt ""
        if data.username isnt ""
            if data.password is confirm
                data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
                $.post "", data, (response) ->
                    if response.status
                        location.reload()
                        return
            else
                $().toastmessage "showWarningToast", "la contraseña es inconrrecta."
        else
            $().toastmessage "showWarningToast", "Ingrese un usuario."
    else
        $().toastmessage "showWarningToast","Seleccione un <q>Proveedor</q>."
    return