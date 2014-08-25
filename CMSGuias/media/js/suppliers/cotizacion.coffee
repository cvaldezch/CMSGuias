$(document).ready ->
    $(".btn-show-key").on "click", showAuthenticateKeys
    $(".btn-valid-key").on "click", showQuotation
    return

showAuthenticateKeys = ->
    $("[name=ruc]").val @getAttribute "data-ruc"
    $("[name=quote]").val @getAttribute "data-quote"
    $(".mkey").modal "toggle"
    return

showQuotation = ->
    data = new Object()
    data.ruc = $("[name=ruc]").val()
    data.quote = $("[name=quote]").val()
    data.key = $("[name=keys]").val()
    if data.ruc isnt "" and data.quote isnt "" and data.key isnt ""
        if data.key.length == 11
            data.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
            $.post "", data, (response) ->
                if response.status
                    location.href = "/suppliers//"
                else
                    $().toastmessage "showErrorToast", "El key ingresado es incorrecto."
            , "json"

        else
            $().toastmessage "showWarningToast", "El key no tiene el formato correcto."
    else
        $().toastmessage "showWarningToast", "Existe un campo vacio."
    return