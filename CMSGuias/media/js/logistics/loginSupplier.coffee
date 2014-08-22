$(document).ready ->
    $("select[name=proveedor]").on "click", getDataProveedor
    $(".btn-default").on "click", openSupplier
    $(".btn-register-supplier").on "click", save_or_update_username
    return

getDataProveedor = ->
    if @value isnt ""
        data =  new Object()
        data.ruc = @value
        data.exists = true
        $.getJSON "", data, (response)->
            console.log response
            if response.exists.status
                $("input[name=username]").val response.exists.username
                .attr "readonly", "readonly"
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
    data.supplier = $.trim($("select[name=proveedor]").val())
    data.password = $.trim($("input[name=passwd]").val())
    confirm = $.trim($("input[name=confirm]").val())
    if data.supplier isnt ""
        if data.username isnt ""
            if data.password is confirm
                data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
                ###hash = CryptoJS.HmacSHA256("", data.password)
                data.password = CryptoJS.enc.Hex.stringify(hash)###
                $.post "", data, (response) ->
                    if response.status
                        $().toastmessage "showNoticeToast", "Se a registrado correctamente al proveedor."
                        setTimeout ->
                            location.reload()
                        , 2600
                        return
                    else
                        $().toastmessage "showWarningToast", "Transaction Error: #{response.raise}"
            else
                $().toastmessage "showWarningToast", "la contraseña es inconrrecta."
        else
            $().toastmessage "showWarningToast", "Ingrese un usuario."
    else
        $().toastmessage "showWarningToast","Seleccione un <q>Proveedor</q>."
    return