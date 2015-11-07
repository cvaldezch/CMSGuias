$ ->
  $("[name=code], [name=name]").on "keyup", keyuppress
  $(document).on "click", ".bdetails", getPricesCode

keyuppress = (ev) ->
  key = if window.ev then ev.keyCode else ev.which
  if key is 13
    console.log this.name
    unless this.name isnt "code" then searchCode() else searchName()
  return

searchCode = (ev) ->
  context = new Object
  context.code = $("[name=code]").val()
  context.searchCode = true
  $.getJSON "", context, (response) ->
    if response.status
      listDetails(response)
      return
    else
      $().toastmessage "showErrorToast", "No se han encontrado resultados."
      return
  return

searchName = (ev) ->
  context = new Object
  context.name = $("[name=name]").val()
  context.searchName = true
  $.getJSON "", context, (response) ->
    if response.status
      listDetails(response)
      return
    else
      $().toastmessage "showErrorToast", "No se han encontrado resultados."
      return
  return

listDetails = (object) ->
  console.info object
  $tb = $(".tdetails > tbody")
  count = 1
  object.index = -> count++
  template = """{{#details}}<tr><td>{{index}}</td><td>{{code}}</td><td>{{name}}</td><td>{{metering}}</td><td><button class="btn btn-xs btn-danger bdetails" value="{{code}}"><span class="fa fa-cogs"></span></button></td></tr>{{/details}}"""
  $tb.empty()
  $tb.html Mustache.render template, object
  return

getPricesCode = (ev) ->
  parameter = new Object
  parameter.prices = true
  parameter.code = this.value
  $.getJSON "", parameter, (response) ->
    if response.status
      $tb = $(".dprices")
      template = """<dl class="dl-horizontal"><dt>Codigo</dt><dd>{{data.code}}</dd><dt>Nombre</dt><dd>{{data.name}} - {{data.metering}}</dd><dt>Unidad</dt><dd>{{data.unit}}<dd></dl><table class="table table-condensed table-hober"><thead><tr><th>Proveedor</th><th>O.Compra</th><th>Moneda</th><th>Fecha</th><th>Precio</th></tr></thead><tbody>{{#prices}}<tr><td>{{supplier}}</td><td>{{purchase}}</td><td>{{currency}}</td><td>{{date}}</td><td>{{price}}</td></tr>{{/prices}}</tbody></table>"""
      $tb.html Mustache.render template, response
      $("#mprices").modal "show"
      return
    else
      $().toastmessage "showErrorToast", "No se han obtenido los precios para este material. #{response.raise}"
      return
  return
