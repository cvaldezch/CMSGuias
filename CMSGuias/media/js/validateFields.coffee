## functions for validate fields in a form

validateFormatDate = (data) ->
    value = data
    pass = false
    RegExpattern = `/^\d{4}\-\d{1,2}\-\d{1,2}$/` # Format DDBB /^\d{2}\/\d{2}\/\d{4}$/
    if value isnt "" and value.match(RegExpattern)
        pass = true
    return pass

convertNumber = (val) ->
    if isNaN(val)
        num = val.replace ",", "."
        num = parseFloat(num)
    else
        num = parseFloat(val)
    return num