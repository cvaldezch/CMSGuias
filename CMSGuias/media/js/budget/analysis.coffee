$ ->
  $("[name=name]").restrictLength $("#pres-max-length")
  $(".showAnalysis").on "click", showAnalysis
  $(".agroup").on "click", openGroup
  $(".ounit").on "click", openUnit
  $(".btn-saveAnalysis").on "click", saveAnalysis
  $("[name=ssearch]").on "change", searchChange
  $(".btn-search").on "click", searchAnalysis
  return

showAnalysis = ->
  $("#manalysis").modal "show"
  return

openGroup = ->
  url = $(this).attr("href")
  win = window.open(url, "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600")
  interval = window.setInterval(->
    if not win? or win.closed
      window.clearInterval interval
      data = new Object()
      data.list = true
      $.getJSON "/sales/budget/analysis/group/list/", data, (response) ->
        if response.status
          $group = $("[name=group]")
          $group.empty()
          Mustache.tags = new Array("[[", "]]")
          $group.html Mustache.render("[[#list]]<option value=\"[[agroup_id]]\">[[ name ]]</option>[[/list]]", response)
        return

    return
  , 1000)
  win

openUnit = ->
  url = $(this).attr("href")
  win = window.open(url, "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600")
  interval = window.setInterval(->
    if not win? or win.closed
      window.clearInterval interval
      data = new Object()
      data.list = true
      $.getJSON "/unit/list/", data, (response) ->
        if response.status
          $group = $("[name=unit]")
          $group.empty()
          Mustache.tags = new Array("[[", "]]")
          $group.html Mustache.render("[[#unit]]<option value=\"[[unidad_id]]\">[[ uninom ]]</option>[[/unit]]", response)
        return

    return
  , 1000)
  win

saveAnalysis = (event) ->
  $.validate
    form: "#registration"
    errorMessagePosition: "top"
    onError: ->
      false

    onSuccess: ->
      event.preventDefault()
      #console.log "valid"
      context = new Object()
      context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
      context.group = $("[name=group]").val()
      context.name = $("[name=name]").val()
      context.unit = $("[name=unit]").val()
      context.performance = $("[name=performance]").val()
      if $("[name=edit]").val().length is 8
        context.edit = true
        context.analysis_id = $("[name=edit]").val()
      else
        context.analysisnew = true
      $.post "", context, ((response) ->
        if response.status
          $().toastmessage "showSuccessToast", "Se guardaron los camnbios correctamente."
          setTimeout (->
            location.reload()
            return
          ), 2600
        else
          $().toastmessage "showErrorToast", "Error al registrar analysis"
        return
      ), "json"
      false

  return

searchAnalysis = ->
  rdo = ""
  context = new Object()
  $("[name=ssearch]").each ->
    rdo = @value  if @checked
    return

  if rdo is "0"
    context.code = $("[name=scode]").val()
  else if rdo is "1"
    context.name = $("[name=sname]").val()
  else context.group = $("[name=sgroup]").val()  if rdo is "2"
  context.list = true
  count = 1
  $.getJSON "", context, (response) ->
    if response.status
      response.index = ->
        count++

      template = "[[#analysis]]<tr><td>[[ index ]]</td><td>[[ code ]]</td><td>[[ name ]]</td><td>[[ unit ]]</td><td>[[ performance ]]</td><td>[[ group ]]</td><td><div class=\"dropdown\"><button class=\"btn btn-default dropdown-toggle btn-xs\" type=\"button\" data-toggle=\"dropdown\" aria-expanded=\"true\"><span class=\"caret\"></span></button><ul class=\"dropdown-menu\" role=\"menu\"><li role=\"presentation\"><a role=\"menuitem\" tabindex=\"-1\" href=\"#\">Detalle</a></li><li role=\"presentation\"><a role=\"menuitem\" tabindex=\"-1\" href=\"#\">Editar</a></li><li role=\"presentation\"><a role=\"menuitem\" tabindex=\"-1\" href=\"#\">Eliminar</a></li></ul></div></td></tr>[[/analysis]]"
      $tb = $("table > tbody")
      $tb.empty()
      Mustache.tags = new Array("[[", "]]")
      $tb.html Mustache.render(template, response)
    else
      $().toastmessage "showErrorToast", "Error al buscar. " + response.raise
    return

  return

searchChange = (event) ->
  if @value is "0"
    $("[name=scode]").attr "disabled", false
    $("[name=sname]").attr "disabled", true
    $("[name=sgroup]").attr "disabled", true
  else if @value is "1"
    $("[name=scode]").attr "disabled", true
    $("[name=sname]").attr "disabled", false
    $("[name=sgroup]").attr "disabled", true
  else if @value is "2"
    $("[name=scode]").attr "disabled", true
    $("[name=sname]").attr "disabled", true
    $("[name=sgroup]").attr "disabled", false
  return

# show analysis edit
editAnalysis = (event) ->
  $("[name=group]").val @getAttribute "data-group"
  $("[name=name]").val @getAttribute "data-name"
  $("[name=unit]").val @getAttribute "data-unit"
  $("[name=performance]").val @getAttribute "data-performance"
  $("[name=edit]").val @value
  return
