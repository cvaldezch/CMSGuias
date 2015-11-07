$ ->
  $("[name=name]").restrictLength $("#pres-max-length")
  # $(".showAnalysis").on "click", showAnalysis
  $(".agroup").on "click", openGroup
  $(".ounit").on "click", openUnit
  $(".btn-saveAnalysis").on "click", saveAnalysis
  $("[name=ssearch]").on "change", searchChange
  $(".btn-search").on "click", searchAnalysis
  $(document).on "click", ".bedit", editAnalysis
  $(document).on "click", ".bdel", delAnalysis
  $(".bedit, .bdel").css "cursor", "pointer"
  $(".analysisClose").on "click", clearEdit
  $('select').material_select()
  $('.dropdown-button').dropdown
    constrain_width: 200
  $('.modal-trigger').leanModal()
  $(".modal.bottom-sheet").css "max-height", "60%"
  return

openGroup = ->
  url = $(this).attr("data-href")
  win = window.open url, "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600"
  interval = window.setInterval ->
    if not win? or win.closed
      window.clearInterval interval
      data = new Object()
      data.list = true
      $.getJSON "/sales/budget/analysis/group/list/", data, (response) ->
        if response.status
          $group = $("[name=group]")
          $group.empty()
          Mustache.tags = new Array("[[", "]]")
          $group.html Mustache.render """[[#list]]<option value=[[agroup_id]]">[[ name ]]</option>[[/list]]""", response
        return
    return
  , 1000
  win

openUnit = ->
  url = $(this).attr "data-href"
  win = window.open(url, "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600")
  interval = window.setInterval ->
    if not win? or win.closed
      window.clearInterval interval
      data = new Object()
      data.list = true
      $.getJSON "/unit/list/", data, (response) ->
        if response.status
          $group = $("[name=unit]")
          $group.empty()
          Mustache.tags = new Array("[[", "]]")
          $group.html Mustache.render """[[#unit]]<option value="[[unidad_id]]">[[ uninom ]]</option>[[/unit]]""", response
        return
    return
  , 1000
  win

saveAnalysis = (e) ->
  $group = $('[name=group]').val()
  $name = $('[name=name]').val()
  $unit = $('[name=unit]').val()
  $performance = $('[name=performance]').val()
  if typeof($group) is 'undefined'
    return false
  if typeof($name) is 'undefined'
    return false
  if typeof($unit) is 'undefined'
    return false
  if typeof($performance) is 'undefined'
    return false
  context = {}
  context.group = $group
  context.name = $name
  context.unit = $unit
  context.performance = $performance
  context.csrfmiddlewaretoken = $('[name=csrfmiddlewaretoken]').val()
  if $('[name=edit]').val().length is 8
    context.edit = true
    context.analysis_id = $('[name=edit]').val()
  else
    context.analysisnew = true
  $.post '', context, (response) ->
    if response.status
      swal 'Felicidades!', 'Se guardaron los camnbios correctamente.', 'success'
      clearEdit()
      setTimeout ->
        location.reload()
        return
      , 2600
      return
    else
      swal 'Error', "Error al registrar analysis. #{response.raise}", 'error'
      return
  , 'json'
  e.preventDefault()
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
      template = """[[#analysis]]<tr><td>[[ index ]]</td><td>[[ code ]]</td><td>[[ name ]]</td><td>[[ unit ]]</td><td>[[ group ]]</td><td class="center-align">[[ performance ]]</td><td>[[ total ]]</td><td><button class="dropdown-button btn yellow darken-2" type="button" data-activates="dropdown"><i class="fa fa-gears"></i></button><ul class="dropdown-content" id="dropdown"><li class="text-left"><a role="menuitem" tabindex="-1" href="/sales/budget/analysis/group/details/[[code]]/"><span class="fa fa-list-alt"></span> Detalle</a></li><li class="text-left"><a role="menuitem" tabindex="-1" class="bedit" data-value="[[code]]" data-group="[[group]]" data-name="[[name]]" data-unit="[[unit]]" data-performance="[[performance]]"><span class="fa fa-edit"></span> Editar</a></li><li class="text-left"><a role="menuitem" tabindex="-1" class="bdel" data-value="[[analysis_id]]"><span class="fa fa-trash"></span> Eliminar</a></li></ul></td></tr>[[/analysis]]"""
      $tb = $("table > tbody")
      $tb.empty()
      Mustache.tags = new Array("[[", "]]")
      $tb.html Mustache.render(template, response)
      $('.dropdown-button').dropdown
        constrain_width: 200
    else
      swal "Alerta!", "Error al buscar. #{response.raise}", "warning"
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
editAnalysis = ->
  $('[name=group]').val this.getAttribute 'data-group'
  $('[name=name]').val this.getAttribute 'data-name'
  $('[name=unit]').val this.getAttribute 'data-unit'
  $('[name=performance]').val this.getAttribute 'data-performance'
  $('[name=edit]').val this.getAttribute 'data-value'
  $('#manalysis').openModal 'show'
  return

# Delete analysis
delAnalysis = (event) ->
  btn = this
  swal
    title: "Eliminar Analisis?"
    text: "Realmente desea eliminar el Analisis de Precio Unitario?"
    type: "warning"
    showCancelButton: true
    confirmButtonColor: "#dd6b55"
    confirmButtonText: "Si, eliminar!"
    cancelButtonText: "No, Cancelar"
    closeOnConfirm: true
    closeOnCancel: true
  , (isConfirm) ->
    if isConfirm
      context = new Object
      context.delAnalysis = true
      context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
      context.analysis = btn.getAttribute "data-value"
      $.post "", context, (response) ->
        if response.status
          location.reload()
          return
        else
          swal "Error", "Error al eliminar el Anlisis de Precio", "warning"
          return
      return
  return

clearEdit = (event) ->
  $("[name=name]").val ""
  $("[name=performance]").val ""
  $("[name=edit]").val ""
  return