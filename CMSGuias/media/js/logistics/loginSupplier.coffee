$(document).ready ->
    $("select[name=proveedor]").on "click", getDataProveedor
    return

getDataProveedor = ->
    if @value isnt ""
        data.ruc = @value

        $getJSON "", data, (response)->
            if response.status

    return

openSupplier = ->
    win = window.open "/logistics/crud/create/supplier/"

    return