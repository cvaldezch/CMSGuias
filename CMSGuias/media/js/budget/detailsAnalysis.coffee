$(document).ready ->
    # block materials
    getMaterialsAll()
    getManPowerAll()
    getlistTools()
    $(".materialsadd, .addmanpower, .addpaneltools").hide()
    $("[name=materials], [name=measure], [name=manpower], [name=tools], [name=measuret]").chosen
        width: "100%"
    $("[name=materials]").on "change", getmeasure
    $("[name=measure]").on "change", getsummary
    $(".bshowaddmat").on "click", showAddMaterial
    $(".bmrefresh").on "click", refreshMaterials
    $(".btnaddmat").on "click", addMaterials
    $(document).on "dblclick", ".editm", showEditMaterials
    $(document).on "click", ".btn-edit-materials", editMaterials
    $(document).on "change", ".edit-tmp-quantity, .edit-tmp-price", calcPartitalMaterial
    $(document).on "click", ".btn-del-materials", delMaterials
    $(".bdelmatall").on "click", delMaterialsAll
    $(".bshownewmat").on "click", openNewMaterial
    # block end
    # block manpower
    $(".bshowaddmp").on "click", showAddManPower
    $(".btnaddmp").on "click", addManPower
    $(".bmprefresh").on "click", refreshManPower
    $(".bdelmp").on "click", delManPowerAll
    $(document).on "dblclick", ".editmp", showEditManPower
    $(document).on "click", ".btn-edit-mp", editManPower
    $(document).on "click", ".btn-del-mp", delManPower
    $(".bshownewmp").on "click", openNewManPower
    # end block
    # block tools
    $(".bshownewtools").on "click", openNewTools
    $("[name=tools]").on "change", getMeasureTools
    $("[name=measuret]").on "change", getSummaryTools
    $(".baddtools").on "click", addTools
    $(".bdeltools").on "click", delToolsAll
    $(document).on "dblclick", ".edittools", showEditTools
    $(document).on "click", ".btnedittool", editTools
    $(document).on "click", ".btndeltool", delTools
    $(".btoolsrefresh").on "click", refreshTools
    $(".bshowaddtool").on "click", showaddTools
    $(".indicator").css "background", "#2d2d2d"
    # end block
    return

# block Materials
getMaterialsAll = (event) ->
    context = new Object()
    context.searchName = true
    context.name = ''
    $.getJSON "/materials/", context, (response) ->
        if response.status
            $op = $("[name=materials]")
            $op.empty()
            template = """{{#names}}<option value="{{name}}">{{name}}</option>{{/names}}"""
            $op.html Mustache.render template, response
            $op.trigger "chosen:updated"
            getmeasure()
    return

getmeasure = (event) ->
    context = new Object
    context.searchMeter = true
    context.name = $("[name=materials]").val()
    $.getJSON "/materials/", context, (response) ->
        if response.status
            $se = $("[name=measure]")
            $se.empty()
            $se.append "<option></option>"
            template = """{{#meter}}<option value="{{code}}">{{measure}}</option> {{/meter}}"""
            $se.html Mustache.render template, response
            $se.trigger "chosen:updated"
            setTimeout ->
                getsummary()
                return
            , 200
            return
    return

getsummary = (event) ->
    context = new Object
    context.scode= $("[name=measure]").val()
    context.summary = true
    if context.scode.length is 15
        $.getJSON "/materials/", context, (response) ->
            if response.status
                template = """<table class="table table-condensed font-11"><tbody><tr><th>Código</th><td class="matid">{{ summary.materials }}</td></tr><tr><th>Nombre</th><td>{{ summary.name }}</td></tr><tr><th>Media</th><td>{{ summary.measure }}</td></tr><tr><th>Unidad</th><td>{{ summary.unit }}</td></tr></tbody></table>"""
                $s = $("[name=summary]")
                $s.empty()
                $s.html Mustache.render template, response
                $("[name=mprice]").val response.summary.price
                return
    else
        swal "Alerta!", "El código del material no es valido.", "warning"
    return

showAddMaterial = (event) ->
    if $(".materialsadd").is(":visible")
        $(this).removeClass "btn-warning"
        .addClass "btn-default"
        $(".materialsadd").hide 800
    else
        $(this).removeClass "btn-default"
        .addClass "btn-warning"
        $(".materialsadd").show 800
    return

addMaterials = (event) ->
    context = new Object()
    context.materials = $(".matid").text()
    context.quantity = $("[name=mquantity]").val()
    context.price = $("[name=mprice]").val()
    if context.materials.length is 15
        if context.quantity isnt ""
            if context.price isnt ""
                context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
                context.addMaterials = true
                $.post "", context, (response) ->
                    if response.status
                        getListMaterials()
                        return
                    else
                        swal "Error!", "Error al guardar los cambios. #{response.raise}", "error"
                        return
                , "json"
            else
                swal "Alerta!", "Precio invalido.", "warning"
        else
            swal "Alerta!", "Cantidad invalida.", "warning"
    else
        swal "Alerta!", "Código de material incorrecto.", "warning"
    return

getListMaterials = (event) ->
    context = new Object
    context.listMaterials = true
    $.getJSON "", context, (response) ->
        if response.status
            $tbl = $(".tmaterials tbody")
            $tbl.empty()
            template = """{{#materials}}<tr data-edit="{{pk}}"><td>{{index}}</td><td>{{code}}</td><td>{{name}}</td><td>{{unit}}</td><td>{{quantity}}</td><td>{{price}}</td><td>{{partial}}</td><td class="text-center"><button class="btn btn-warning btn-xs btn-edit-materials" value="{{ pk }}" data-materials="{{ code }}" disabled><span class="fa fa-edit"></span></button></td><td class="text-center"><button class="btn btn-danger btn-xs btn-del-materials" value="{{ pk }}" data-materials="{{ code }}"><span class="fa fa-trash"></span></button></td></tr>{{/materials}}"""
            counter = 1
            response.index = ->
                return counter++
            $tbl.html Mustache.render template, response
            getUnitaryPrice()
            return
        else
            swal "Alerta!", "Error al Obtener la lista. #{response.raise}.", "warning"
            return
    return

refreshMaterials = (event) ->
    getMaterialsAll()
    getListMaterials()
    return

openNewMaterial = (event) ->
    win = window.open "/materials/", "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600"
    interval = window.setInterval ->
        if win == null or win.closed
            window.clearInterval interval
            getMaterialsAll
            return
    , 1000
    return win

showEditMaterials = ->
    if $(".edit-tmp-quantity").length
        $(".edit-tmp-quantity").parent("td").html $(".edit-tmp-quantity").val()
    if $(".edit-tmp-price").length
        $(".edit-tmp-price").parent("td").html $(".edit-tmp-price").val()
    $tr = $(this)
    $td = $tr.find "td"
    console.log $td
    quantity = $td.eq(4).text()
    $(".btn-edit-materials").attr "disabled", true
    $td.eq(7).find("button").attr "disabled", false
    ###if quantity.indexOf "," then quantity=  quantity.replace ",", "."
    quantity = parseFloat quantity###
    price = $td.eq(5).text()
    $td.eq(4).html """<input type="text" value="#{quantity}" class="form-control input-sm col-2 edit-tmp-quantity">"""
    $td.eq(5).html """<input type="text" value="#{price}" class="form-control input-sm col-2 edit-tmp-price">"""
    return

editMaterials =  (event) ->
    context = new Object
    context.quantity = $(".edit-tmp-quantity").val()
    context.price = $(".edit-tmp-price").val()
    context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
    try
        if not context.quantity.match /^[+]?[0-9]+[\.[0-9]+]?/
            swal "Alerta!", "No se a ingreso un número, cantidad incorrecta.", "warning"
            return false
        if not context.price.match /^[+]?[0-9]+[\.[0-9]+]?/
            swal "Alerta!", "No se a ingreso un número, precio incorrecto.", "warning"
            return false
        context.editMaterials = true
        context.materials = @getAttribute "data-materials"
        context.id = @value
        $.post "", context, (response) ->
            if response.status
                $(".edit-tmp-quantity").parent("td").parent("tr").find("td").eq(7).find("button").attr "disabled", true
                $(".edit-tmp-quantity").parent("td").html $(".edit-tmp-quantity").val()
                $(".edit-tmp-price").parent("td").html $(".edit-tmp-price").val()
                return
            else
                swal "Alerta!", "No se a podido editar. #{response.raise}.", "warning"
                return
        , "json"
    catch e
        swal "Alerta", "No se habilito la edición.", "warning"
    return

calcPartitalMaterial = (event) ->
    $tr = $(@).parent("td").parent("tr")
    quantity = $tr.find("td").eq(4).find("input").val()
    price = $tr.find("td").eq(5).find("input").val()
    if quantity.indexOf(",") is 1
        quantity = quantity.replace ",", "."
    if price.indexOf(",") is 1
        price = price.replace ",", "."
    quantity = parseFloat quantity
    price = parseFloat price
    $tr.find("td").eq(6).text (quantity * price).toFixed(2)
    return

delMaterials = (event) ->
    btn = this
    swal
        title: "Eliminar",
        text: "Realmente deseas eliminar el material?"
        type: "warning"
        showCancelButton: true
        confirmButtonColor: "#dd9b55"
        confirmButtonText: "Si, eliminar!"
    , (isConfirm) ->
        if isConfirm
            context = new Object
            context.materials = btn.getAttribute "data-materials"
            context.id = btn.value
            context.delMaterials = true
            context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
            $.post "", context, (response) ->
                if response.status
                    swal "Alerta", "Se a eliminado el material.", "warning"
                    getListMaterials()
                    return
                else
                    swal "Alerta", "No se a podido eliminar el material. #{response.raise}", "warning"
                    return
            return
    return

delMaterialsAll = (event) ->
    swal
        title: "Eliminar todo los materiales",
        text: "Realmente deseas eliminar todo la lista de materiales?"
        type: "warning"
        showCancelButton: true
        confirmButtonText: "Si, eliminar"
        confirmButtonColor: "#bb0655"
    , (isConfirm) ->
        if isConfirm
            context = new Object
            context.delMaterialsAll = true
            context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
            $.post "", context, (response) ->
                if response.status
                    swal "Felicidades", "Se a eliminado el material.", "success"
                    getListMaterials()
                    return
                else
                    swal "Error", "No se a podido eliminar el material. #{response.raise}", "error"
                    return
            return
    return

# block Man power
getManPowerAll = (event) ->
    context = new Object
    context.listcbo = true
    $.getJSON "/manpower/list/cbo/", context, (response) ->
        if response.status
            $cm = $("[name=manpower]")
            $cm.empty()
            template = """{{#list}}<option value="{{cargo_id}}">{{cargos}}</option>{{/list}}"""
            $cm.html Mustache.render template, response
            $cm.trigger "chosen:updated"
        else
            swal "Alerta!", "Error al listar combo. #{response.raise}", "warning"
            return
    return

showAddManPower = (event) ->
    if $(".addmanpower").is ":visible"
        $(this).removeClass "btn-warning"
        .addClass "btn-default"
        $(".addmanpower").hide 800
    else
        $(this).removeClass "btn-default"
        .addClass "btn-warning"
        $(".addmanpower").show 800
    return

addManPower = (event) ->
    context = new Object
    context.addMan = true
    context.performance = $(".performance").text()
    context.manpower = $("[name=manpower]").val()
    context.gang = $("[name=mpgang]").val()
    context.price = $("[name=mpprice]").val()
    if context.manpower is ""
        swal "Alerta!", "Codigo para Mano de obra es incorrecto.", "warning"
        return false
    if not context.gang.match /^[+]?[0-9]{1,3}[\.[0-9]{0,3}]?/
        swal "Alerta!", "Cuadrilla invalida.", "warning"
        return false
    if not context.price.match /^[+]?[0-9]+[\.[0-9]{0,4}]?/
        swal "Alerta!", "El precio ingresado es incorrecto.", "warning"
        return false
    context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
    $.post "", context, (response) ->
        if response.status
            listManPower()
        else
            swal  "Alerta!", "Error al agregar mano de poder. #{response.raise}", "warning"
            return
    , "json"
    return

listManPower = (event) ->
    context = new Object
    context.listManPower = true
    $.getJSON "", context, (response) ->
        if response.status
            $tb = $(".tmanpower > tbody")
            template = """{{#manpower}}<tr class="editmp"><td>{{index}}</td><td>{{code}}</td><td>{{name}}</td><td>{{unit}}</td><td>{{gang}}</td><td>{{quantity}}</td><td>{{price}}</td><td>{{partial}}</td><td class="text-center"><button class="btn btn-xs btn-warning btn-edit-mp" value="{{ id }}" data-mp="{{code}}" disabled><span class="fa fa-edit"></span></button></td><td class="text-center"><button class="btn btn-danger btn-xs btn-del-mp" value="{{ id }}" data-mp="{{code}}"><span class="fa fa-trash"></span></button></td></tr>{{/manpower}}"""
            $tb.empty()
            counter = 1
            response.index = ->
                return counter++
            $tb.html Mustache.render template, response
            getUnitaryPrice()
            return
        else
            swal "Alerta!", "No se obtenido resultados. #{response.raise}", "warning"
            return
    return

delManPowerAll = (event) ->
    swal
        title: "Eliminar?"
        text: "Realmente desea eliminar todo la lista de Mano de Obra?"
        type: "warning"
        showCancelButton: true
        confirmButtonText: "Si, eliminar"
        confirmButtonColor: "#ddb655"

    , (isConfirm) ->
        if isConfirm
            context = new Object
            context.delManPowerAll = true
            context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
            $.post "", context, (response) ->
                if response.status
                    listManPower()
                    return
                else
                    swal "Error", "Error al eliminar toda la lista. #{response.raise}", "error"
                    return
            , "json"
            return
    return

refreshManPower = (event) ->
    getManPowerAll()
    listManPower()
    return
# end block

showEditManPower = (event) ->
    if $(".edit-mp-gang").length
        $(".edit-mp-gang").parent("td").html $(".edit-mp-gang").val()
    if $(".edit-mp-price").length
        $(".edit-mp-price").parent("td").html $(".edit-mp-price").val()
    $tr = $(@)
    $td = $tr.find "td"
    gang = $td.eq(4).text()
    $td.eq(8).find("button").attr "disabled", false
    price = $td.eq(6).text()
    $td.eq(4).html """<input type="text" value="#{gang}" class="form-control input-sm col-2 edit-mp-gang">"""
    $td.eq(6).html """<input type="text" value="#{price}" class="form-control input-sm col-2 edit-mp-price">"""
    return

editManPower = (event) ->
    context = new Object
    context.addMan = true
    context.gang = $(".edit-mp-gang").val()
    context.price = $(".edit-mp-price").val()
    context.performance = $(".performance").text()
    context.manpower = @getAttribute "data-mp"
    if not context.gang.match /^[+]?[0-9]{1,3}[\.[0-9]{0,3}]?/
        swal "Alerta!", "Cuadrilla invalida.", "warning"
        return false
    if not context.price.match /^[+]?[0-9]+[\.[0-9]{0,4}]?/
        swal "Alerta!", "El precio ingresado es incorrecto.", "warning"
        return false
    context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
    $.post "", context, (response) ->
        if response.status
            listManPower()
            return
        else
            swal "Alerta!", "Error al editar los campos. #{response.raise}", "warning"
            return
    , "json"
    return

delManPower = (event) ->
  btn = @
  swal
    title: "Eliminar?"
    text: "Realmente deseas eliminar la mano de Obra?"
    type: "warning"
    showCancelButton: true
    confirmButtonColor: "#ddb655"
    confirmButtonText: "Si, eliminar"
  , (isConfirm) ->
      if isConfirm
        context = new Object
        context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
        context.delMan = true
        context.manpower = btn.getAttribute "data-mp"
        $.post "", context, (response) ->
          if response.status
            listManPower()
            return
          else
            swal "Alerta!", "Error al eliminar la mano de obra. #{response.raise}", "warning"
            return
        , "json"
  return

openNewManPower = ->
    win = window.open "/manpower/add", "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600"
    interval = window.setInterval ->
        if win == null or win.closed
            window.clearInterval interval
            getManPowerAll()
            return
    , 1000
    return win

# block tools
# get all list disticnt tools
getlistTools = (event) ->
  context = new Object
  context.listName = true
  $.getJSON "/tools/search/", context, (response) ->
    if response.status
      template = """{{#tools}}<option value="{{ name }}">{{ name }}</option>{{/tools}}"""
      $op = $("[name=tools]")
      $op.empty()
      $op.html Mustache.render template, response
      $op.trigger "chosen:updated"
      getMeasureTools()
    else
      swal "Alerta!", "No existe una lista. #{response.raise}", "warning"
      return
  return
# get  measure for each tools
getMeasureTools = (event) ->
  context = new Object
  context.searchMeasure = true
  context.name = $.trim $("[name=tools]").val()
  $.getJSON "/tools/search/", context, (response) ->
    if response.status
      template = """{{#measure}}<option value="{{ tools_id }}">{{ measure }}</option>{{/measure}}"""
      $mt = $("[name=measuret]")
      $mt.empty()
      $mt.html Mustache.render template, response
      $mt.trigger "chosen:updated"
      setTimeout ->
        getSummaryTools()
      , 300
    else
      swal "Alerta", "No se han obtenido resultados para tu busqueda. #{response.raise}", "warning"
      return
  return
# get summary tools
getSummaryTools = ->
  context = new Object
  context.getSummary = true
  context.tools = $("[name=measuret]").val()
  if context.tools.length isnt 14
    swal "Alerta", "El codigo es incorrecto.", "warning"
    return false
  $.getJSON "/tools/search/", context, (response) ->
    if response.status
      template = """<table class="table table-condensed font-11"><tbody><tr><th>Código </th><td class="tools_id">{{ summary.tools_id }}</td></tr><tr><th>Nombre </th><td>{{ summary.name }}</td></tr><tr><th>Medida</th><td>{{ summary.measure }}</td></tr><tr><th>Unidad </th><td>{{ summary.unit__uninom }}</td></tr></tbody></table>"""
      $ob = $(".summarytools")
      $ob.empty()
      $ob.html Mustache.render template, response
    else
      swal "Alerta", "Error al obtener los datos, #{response.raise}", "warning"
      return
  return

# add tools
addTools = (event) ->
  context = new Object
  context.tools = $(".tools_id").text()
  context.gang = $("[name=gangt]").val()
  context.price = $("[name=pricet]").val()
  context.performance = $(".performance").text()
  if context.tools.length isnt 14
    swal "Alerta!", "Código de herramienta erroneo.", "warning"
    return false
  if not context.gang.match /^[+]?[0-9]{1,3}[\.[0-9]{0,3}]?/
    swal "Alerta!", "La Cuadrila es incorrecta.", "warning"
    return false
  if not context.price.match /^[+]?[0-9]+[\.[0-9]{0,4}]?/
    swal "Alerta!", "El precio ingresado es incorrecto.", "warning"
    return false
  context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
  context.addTools = true
  $.post "", context, (response) ->
    if response.status
      listDetailsTools()
      return
    else
      swal "Alerta!", "No se a podido agregar herramientas. #{response.raise}", "warning"
      return
  return
# edit Tools
editTools = (event) ->
  console.log "click"
  context = new Object
  context.tools = @value
  context.gang = $(".edit-tool-gang").val()
  context.price = $(".edit-tool-price").val()
  context.performance = $(".performance").text()
  if context.tools.length isnt 14
    swal "Alerta!", "Código de herramienta erroneo.", "warning"
    return false
  if not context.gang.match /^[+]?[0-9]{1,3}[\.[0-9]{0,3}]?/
    swal "Alerta!", "La Cuadrila es incorrecta.", "warning"
    return false
  if not context.price.match /^[+]?[0-9]+[\.[0-9]{0,4}]?/
    swal "Alerta!", "El precio ingresado es incorrecto.", "warning"
    return false
  context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
  context.addTools = true
  console.log context
  $.post "", context, (response) ->
    if response.status
      listDetailsTools()
      return
    else
      swal "Alerta!", "No se a podido editar herramientas. #{response.raise}", "warning"
      return
  return

# delete tools
delTools = (event) ->
  btn = this
  swal
    title: "Eliminar",
    text: "Realmente desea eliminar la herramienta?"
    type: "warning"
    showCancelButton: true
    confirmButtonText: "Si, eliminar"
    confirmButtonColor: "#ddb655"
  , (isConfirm) ->
      if isConfirm
        context =  new Object
        context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
        context.delTools = true
        context.tools = btn.value
        $.post "", context, (response) ->
          if response.status
            listDetailsTools()
            return
          else
            swal "Alerta!", "No se a podido eliminar la herramientas. #{response.raise}", "warning"
            return
        return
  return

# delete all tools
delToolsAll = (event) ->
  swal
    title: "Eliminar"
    text: "Realmente desea eliminar toda la lista de herramientas?"
    type: "warning"
    showCancelButton: true
    confirmButtonColor: "#ddb655"
    confirmButtonText: "Si, eliminar"
  , (isConfirm) ->
      if isConfirm
        context = new Object
        context.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
        context.delToolsAll = true
        $.post "", context, (response) ->
          if response.status
            listDetailsTools()
            return
          else
            swal "Alerta!", "No se a eliminado la lista de herramientas. #{response.raise}", "warning"
            return
        return
  return

# listTools details
listDetailsTools = (event) ->
  context = new Object
  context.listTools = true
  $.getJSON "", context, (response) ->
    if response.status
      template = """{{#tools}}<tr class="edittools"><td>{{index}}</td><td>{{code}}</td><td>{{name}}</td><td>{{unit}}</td><td>{{gang}}</td><td>{{quantity}}</td><td>{{price}}</td><td>{{partial}}</td><td><button type="button" class="btn btn-xs btn-warning btnedittool" value="{{ code }}" data-id="{{ id }}" disabled><span class="fa fa-edit"></span></button></td><td><button type="button" class="btn btn-xs btn-danger btndeltool" value="{{ code }}" data-id=" {{ x.id }}"><span class="fa fa-trash"></span></button></td></tr>{{/tools}}"""
      $tb = $(".ttools > tbody")
      counter = 1
      response.index = ->
        return counter++
      $tb.html Mustache.render template, response
      getUnitaryPrice()
      return
    else
      swal "Error", "No se han obtenido datos. #{response.raise}", "error"
      return
  return
# refresh list Tools
refreshTools = (event) ->
  getlistTools()
  listDetailsTools()
  return

showaddTools = (event) ->
  if $(".addpaneltools").is ":visible"
      $(@).removeClass "btn-warning"
      .addClass "btn-default"
      $(".addpaneltools").hide 800
  else
      $(@).removeClass "btn-default"
      .addClass "btn-warning"
      $(".addpaneltools").show 800
  return

showEditTools = (event) ->
  if $(".edit-tool-gang").length
      $(".edit-tool-gang").parent("td").html $(".edit-tool-gang").val()
  if $(".edit-tool-price").length
      $(".edit-tool-price").parent("td").html $(".edit-tool-price").val()
  $tr = $(@)
  $td = $tr.find "td"
  gang = $td.eq(4).text()
  $td.eq(8).find("button").attr "disabled", false
  price = $td.eq(6).text()
  $td.eq(4).html """<input type="text" value="#{gang}" class="form-control input-sm col-2 edit-tool-gang">"""
  $td.eq(6).html """<input type="text" value="#{price}" class="form-control input-sm col-2 edit-tool-price">"""
  return
# open new Tools
openNewTools = ->
  win = window.open "/tools/add", "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600"
  interval = window.setInterval ->
      if win == null or win.closed
          window.clearInterval interval
          getlistTools()
          return
  , 1000
  return win

# get price unitary
getUnitaryPrice = (event) ->
  context = new Object
  context.priceAll = true
  $.getJSON "", context, (response) ->
    if response.status
      $(".tanalysis").text response.total
  return
