## functions for validate fields in a form

validateFormatDate = (data) ->
    value = data
    pass = false
    RegExpattern = `/^\d{4}\-\d{1,2}\-\d{1,2}$/` # Format DDBB /^\d{2}\/\d{2}\/\d{4}$/
    if value isnt "" and value.match(RegExpattern)
        pass = true
    return pass

validateEmail = (email) ->
    re = /\S+@\S+\.\S+/
    return re.test email

convertNumber = (val) ->
    if isNaN(val)
        num = val.replace ",", "."
        num = parseFloat(num)
    else
        num = parseFloat(val)
    return num

numberOnly = (event) ->
    #@value = @value.replace `/[^0-9\.]/g`, '' # OK
    #if (String.fromCharCode(event.KeyCode).match(`/[^0-9]/g`))
    #    return false
    # console.info event.keyCode
    # Level Key Windo
    key = `window.Event ? event.keyCode : event.which`
    if key isnt 37 and key isnt 39 and key isnt 8 and key isnt 46 and (key < 48 or key > 57)
        event.preventDefault()
        return false
    return