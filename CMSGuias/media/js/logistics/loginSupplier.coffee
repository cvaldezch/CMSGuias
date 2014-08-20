$(document).ready ->
    $("select[name=proveedor]").on "click", getDataProveedor
    $(".btn-default").on "click", openSupplier
    return

getDataProveedor = ->
    if @value isnt ""
        data =  new Object()
        data.ruc = @value
        $.getJSON "", data, (response)->
            if response.status
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

