mat = new Object
counter_materials_global = 0
getDescription = (name) ->
  $.getJSON "/json/get/materials/name/",
    nom: name
  , (response) ->
    template = "<li id='li{{ id }}' onClick=getidli(this);><a class='text-primary' onClick='selectMaterial(this);'>{{ matnom }}</a></li>"
    $opt = $(".matname-global")
    $opt.empty()
    i = 0
    for x of response.name
      response.name[x].id = i
      $opt.append Mustache.render(template, response.name[x])
      i += 1
    $(".matname-global").show()
    $("[name=description]").focus().after $(".matname-global")
    return

  return

getidli = (item) ->
  $("[name=description]").val($("#" + item.id + " > a").text()).focus()
  $(".matname-global").hide()
  counter_materials_global = 0
  getMeters()
  return

# selected material with click or enter
selectMaterial = (all) ->
  $("[name=description]").val(all.innerHTML).focus()
  $(".matname-global").hide()
  counter_materials_global = 0
  return

keyUpDescription = (event) ->
  key = (event.keyCode or event.which)
  if key is 13
    if $(".matname-global").is(":visible")
      $("[name=description]").val $(".item-selected > a").text()
      $(".matname-global").hide()
    getMeters()
    counter_materials_global = 0
  return

getMeters = ->
  $nom = $("[name=description]")
  unless $nom.val() is ""
    data = matnom: $nom.val().trim()
    $.getJSON "/json/get/meter/materials/", data, (response) ->
      template = "<option value='{{ matmed }}'>{{ matmed }}</option>"
      $med = $("[name=meter]")
      $med.empty()
      for x of response.list
        $med.append Mustache.render(template, response.list[x])
      getSummaryMaterials()
      return

  else
    console.warn "The Field Name is empty!"
  return

getSummaryMaterials = ->
  $nom = $("[name=description]")
  $med = $("[name=meter]")
  if $nom.val().trim() isnt "" and $med.val() isnt ""
    data =
      matnom: $nom.val()
      matmed: $med.val()

    $.getJSON "/json/get/resumen/details/materiales/", data, (response) ->

      #console.log(response);
      template = "<tr><th>Codigo :</th><td class='id-mat'>{{materialesid}}</td></tr><tr><th>Descripción :</th><td>{{matnom}}</td></tr><tr><th>Medida :</th><td>{{matmed}}</td></tr><tr><th>Unidad :</th><td>{{unidad}}</td></tr>"
      $tb = $(".tb-details > tbody")
      $tb.empty()
      for x of response.list
        $tb.append Mustache.render(template, response.list[x])
      searchBrandOption()
      return

  return

moveTopBottom = (key) ->
  code = key
  ul = document.getElementById("matname-global")
  if code is 40 #down
    if $("#matname-global li.item-selected").length is 0 #Si no esta seleccionado nada
      $("#matname-global li:first").addClass "item-selected"
    else
      $("#matname-global li:first").addClass "item-selected"
  else if code is 38 #arriba
    $("#matname-global li.item-selected").removeClass "item-selected"
  else if code is 39 #abajo
    liSelected = $("#matname-global li.item-selected")
    if liSelected.length is 1 and liSelected.next().length is 1
      liSelected.removeClass("item-selected").next().addClass "item-selected"
      ul.scrollTop += 30  if counter_materials_global > 9
      counter_materials_global++
  else if code is 37 #izquierda
    liSelected = $("#matname-global li.item-selected")
    if liSelected.length is 1 and liSelected.prev().length is 1
      liSelected.removeClass("item-selected").prev().addClass "item-selected"
      ul.scrollTop -= 30  if counter_materials_global > 9
      counter_materials_global--
  return
# code
searchMaterialCode = (code) ->
  pass = false
  if code.length < 15 or code.length > 15
    $().toastmessage "showWarningToast", "Format Code Invalid!"
    pass = false
  else pass = true  if code.length is 15
  if pass
    data = new Object()
    data["code"] = code
    $.getJSON "/json/get/materials/code/", data, (response) ->
      mats = response
      if response.status

        #$("[name=description]").val(response.list.matnom);
        $met = $("[name=meter]")
        $met.empty()
        $met.append Mustache.render("<option value='{{ matmed }}'>{{ matmed }}</option>", response.list)
        $("[name=description]").val response.list.matnom
        template = "<tr><th>Codigo :</th><td class='id-mat'>{{materialesid}}</td></tr>" + "<tr><th>Descripción :</th><td>{{matnom}}</td></tr>" + "<tr><th>Medida :</th><td>{{matmed}}</td></tr>" + "<tr><th>Unidad :</th><td>{{unidad}}</td></tr>"
        $tb = $(".tb-details > tbody")
        $tb.empty()
        $tb.append Mustache.render(template, response.list)
        searchBrandOption()
      else
        $().toastmessage "showWarningToast", "The material not found."
      return

  return

# Search Brand and Model for the material
searchBrandOption = ->
  $.getJSON "/json/brand/list/option/", (response) ->
    if response.status
      template = "<option value=\"{{ brand_id }}\">{{ brand }}</option>"
      $brand = $("select[name=brand]")
      $brand.empty()
      for x of response.brand
        $brand.append Mustache.render(template, response.brand[x])
    else
      $().toastmessage "showWarningToast", "No se a podido obtener la lista de marcas."
    return

  return

searchModelOption = ->
  brand = $("select[name=brand]").val()
  unless brand is ""
    data = brand: brand
    $.getJSON "/json/model/list/option/", data, (response) ->
      if response.status
        template = "<option value=\"{{ model_id }}\">{{ model }}</option>"
        $model = $("select[name=model]")
        $model.empty()
        for x of response.model
          $model.append Mustache.render(template, response.model[x])
      else
        $().toastmessage "showWarningToast", "No se a podido obtener la lista de marcas."
      return

  return

keyDescription = (event) ->
  key = undefined
  key = (if window.Event then event.keyCode else event.which)
  getDescription @value.toLowerCase()  if key isnt 13 and key isnt 40 and key isnt 38 and key isnt 39 and key isnt 37
  moveTopBottom key  if key is 40 or key is 38 or key is 39 or key is 37
  return

keyCode = (event) ->
  key = undefined
  key = (if window.Event then event.keyCode else event.which)
  searchMaterialCode @value  if key is 13

searchMaterial = (event) ->
  code = undefined
  desc = undefined
  desc = $("input[name=description]").val()
  code = $("input[name=code]").val()
  if code.length is 15
    searchMaterialCode code
  else
    getDescription $.trim(desc).toLowerCase()

#


#/ Add Event Listener
$(document).on "click", "select[name=brand]", (event) ->
  searchModelOption()
  return

$(document).on "keyup", "input[name=description]", keyDescription
$(document).on "keypress", "input[name=description]", keyUpDescription
$(document).on "click", "select[name=meter]", getSummaryMaterials
$(document).on "keypress", "input[name=code]", keyCode
