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
      data = matnom: $nom.val()
      $.getJSON "/json/get/meter/materials/", data, (response) ->
        template = "<option value=\"{{ materiales_id }}\">{{ matmed }}</option>"
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
  $pro = $("input[name=pro]")
  $sec = $("input[name=sec]")
  if $nom.val().trim() isnt "" and $med.val() isnt ""
    data =
      matnom: $nom.val()
      # matmed: $med.val()
      matid: $med.val()
      pro: $pro.val()
      sec: $sec.val()
    $.getJSON "/json/get/resumen/details/materiales/", data, (response) ->
      console.log(response);
      searchUnitOption()
      template = """<tr><th>Codigo :</th><td class='id-mat'>{{materialesid}}</td></tr><tr><th>Descripción :</th><td>{{matnom}}</td></tr><tr><th>Medida :</th><td>{{matmed}}</td></tr><tr><th>Unidad :</th><td>{{unidad}}</td></tr>"""
      $tb = $(".tb-details > tbody")
      $tb.empty()
      for x of response.list
        $tb.append Mustache.render(template, response.list[x])
      searchBrandOption()
      autoSearchMaterialGroup(response.list[0].materialesid)
      $("input[name=cantidad]").val response.list[0].quantity
      $("input[name=precio]").val response.list[0].purchase
      $("input[name=sales]").val response.list[0].sale
      $("input[name=sale]").val response.list[0].sale
      $lstp = $("#lstpurchase")
      $lstp.empty()
      if $lstp.length > 0 and response.purchase
        $lstp.append Mustache.render """{{#purchase}}<option label="{{currency}}" value="{{purchase}}" />{{/purchase}}""", response
      $lsts = $("#lstsales")
      $lsts.empty()
      if $lsts.length > 0 and response.purchase
        $lsts.append Mustache.render """{{#purchase}}<option label="{{currency}}" value="{{sales}}" />{{/purchase}}""", response
      if $("#unit").length > 0
        setTimeout ->
          console.log response.list[0].unidad
          $("#unit").val response.list[0].unidad
          return
        , 800
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
    data.pro = $("input[name=pro]").val()
    data.sec = $("input[name=sec]").val()
    $.getJSON "/json/get/materials/code/", data, (response) ->
      mats = response
      if response.status
        ## here search group material

        ##
        #$("[name=description]").val(response.list.matnom);
        $met = $("[name=meter]")
        $met.empty()
        searchUnitOption()
        $met.append Mustache.render("<option value='{{ matmed }}'>{{ matmed }}</option>", response.list)
        $("[name=description]").val response.list.matnom
        template = "<tr><th>Codigo :</th><td class='id-mat'>{{ materialesid }}</td></tr><tr><th>Descripción :</th><td>{{ matnom }}</td></tr><tr><th>Medida :</th><td>{{ matmed }}</td></tr><tr><th>Unidad :</th><td>{{ unidad }}</td></tr>"
        $tb = $(".tb-details > tbody")
        $tb.empty()
        $tb.append Mustache.render(template, response.list)
        searchBrandOption()
        $("input[name=cantidad]").val response.list.quantity
        $("input[name=precio]").val response.list.purchase
        $("input[name=sale]").val response.list.sale
        $("input[name=sales]").val response.list.sale
        $lstp = $("#lstpurchase")
        $lstp.empty()
        if $lstp.length > 0 and response.purchase
          $lstp.append Mustache.render """{{#purchase}}<option label="{{currency}}" value="{{purchase}}" />{{/purchase}}""", response
        $lsts = $("#lstsales")
        $lsts.empty()
        if $lsts.length > 0 and response.purchase
          $lsts.append Mustache.render """{{#purchase}}<option label="{{currency}}" value="{{sales}}" />{{/purchase}}""", response
        if $("#unit").length > 0
          setTimeout ->
            console.log response.list.unidad
            $("#unit").val response.list.unidad
            return
          , 800
      else
        console.log "materials not found"
        $().toastmessage "showWarningToast", "The material not found."
      return
  return

# Search Group materials
autoSearchMaterialGroup = (materials) ->
    if $("input[name=gincludegroup]").length and $("input[name=gincludegroup]").is(":checked")
        if $(".msgparent").is(":visible")
            $(".msgparent").addClass "hide"
        data = new Object
        data.materials = materials
        data.searchGroupMaterial = true
        $.getJSON "/json/get/group/materials/bedside/", data, (response) ->
            console.warn response
            if response.status
                if response.result
                    # assess if exists modal
                    if not $("#searchGroupModalGlobal").length
                        $("footer").append modalGlobalGroupMaterial
                    if response.hasOwnProperty('parent')
                        $("#gparent").val 1
                        $(".msgparent").removeClass "hide"
                    else
                        $("#gparent").val 0
                    template = "<tr>
                                <td>{{ item }}</td>
                                <td>{{ description }}</td>
                                <td>{{ name }}</td>
                                <td>{{ tdesc }}</td>
                                <td>
                                    <button class=\"btn btn-xs btn-link text-primary bg-modal-view-details\" value=\"{{ mgroup }}\" data-mat=\"{{ materials }}\">
                                        <span class=\"fa fa-chevron-circle-down\"></span>
                                    </button>
                                </td>
                                </tr>"
                    $tb = $("table.table-group-materials-global > tbody")
                    $tb.empty()
                    for x of response.list
                        response.list[x].item = parseInt(x) + 1
                        $tb.append Mustache.render template, response.list[x]
                    $("#searchGroupModalGlobal").modal "show"
                else
                    $().toastmessage "showErrorToast", "No se han encontrado un grupo de materiales."
            return
    return

getDetailsGroupMaterials = (event) ->
    mgroup = @value
    if mgroup.length is 10
        data = new Object
        data.DetailsGroupMaterials = true
        data.mgroup = mgroup
        $.getJSON "/json/get/group/materials/bedside/", data, (response) ->
            if response.status
                template = "<tr>
                            <td>{{ item }}</td>
                            <td>{{ materials }}</td>
                            <td>{{ name }}</td>
                            <td>
                                {{!meter}}
                            </td>
                            <td>{{ unit }}</td>
                            <td>
                                <input type=\"text\" style=\"width: 80px;\" class=\"form-control input-sm text-right\" value=\"{{ quantity }}\" onKeyUp=\"numberOnly(event);\"></td>
                            </tr>"
                $tb = $("table.table-group-materials-details-global > tbody")
                $tb.empty()
                options = "<option value=\"{{ materials }}\" {{!select}}>{{ meter }}</option>"
                sel = "<select class=\"form-control input-sm\" style=\"width: 200px\">{{!ops}}</select>"
                for x of response.details
                    tmp = template
                    meter = ""
                    s = sel
                    for o of response[response.details[x].materials]
                        op = options
                        if $.trim(response[response.details[x].materials][o].meter) is $.trim(response.details[x].diameter)
                            op = op.replace "{{!select}}", "selected"
                        meter += Mustache.render op, response[response.details[x].materials][o]
                    s = s.replace "{{!ops}}", meter
                    tmp = tmp.replace "{{!meter}}", s
                    response.details[x].item = parseInt(x) + 1
                    $tb.append Mustache.render tmp, response.details[x]
                $("div.global-group-modal-two, .bg-modal-back, .bg-modal-save").removeClass "hide"
                $("div.global-group-modal-one").addClass "hide"
                if parseInt $("#gparent").val()
                    $(".bg-modal-create").removeClass "hide"
                return
            else
                $().toastmessage "showErrorToast", "No hay detalles para mostrar."
                return
        return
    else
        $().toastmessage "showErrorToast", "Formato de Codigo Incorrecto."
        return
    return

bgModalBack = (event) ->
    $("div.global-group-modal-one").removeClass "hide"
    $("div.global-group-modal-two, .bg-modal-back, .bg-modal-save, .bg-modal-create").addClass "hide"
    return

bgModalErase = (event)->
    $("#searchGroupModalGlobal").modal "hide"
    $("table.table-group-materials-global > tbody").empty()
    $("table.table-group-materials-details-global > tbody").empty()
    $("div.global-group-modal-one").removeClass "hide"
    $("div.global-group-modal-two, .bg-modal-back, .bg-modal-save, .bg-modal-create").addClass "hide"
    tmpObjectDetailsGroupMaterials = new Object
    if $(".msgparent").is(":visible")
        $(".msgparent").addClass "hide"
    return

tmpObjectDetailsGroupMaterials = new Object
bgModalAddMaterials = (event) ->
    tm = new Array
    $("table.table-group-materials-details-global > tbody > tr").each (index, element) ->
        $td = $(element).find("td")
        tm.push
            "materials": $td.eq(3).find("select").val(),
            "quantity": $td.eq(5).find("input").val()
        return
    tmpObjectDetailsGroupMaterials.details = tm
    $("#searchGroupModalGlobal").modal "hide"
    $("table.table-group-materials-global > tbody").empty()
    $("table.table-group-materials-details-global > tbody").empty()
    $("div.global-group-modal-one").removeClass "hide"
    $("div.global-group-modal-two, .bg-modal-back, .bg-modal-save, .bg-modal-create").addClass "hide"
    if $(".msgparent").is(":visible")
        $(".msgparent").addClass "hide"
    return

# Search Brand and Model for the material
searchBrandOption = ->
  $.getJSON "/json/brand/list/option/", (response) ->
    if response.status
      template = "<option value=\"{{ brand_id }}\" {{ select }}>{{ brand }}</option>"
      $brand = $("select[name=brand]")
      $brand.empty()
      for x of response.brand
        if response.brand[x].brand_id is "BR000"
          response.brand[x].select = "selected"
        $brand.append Mustache.render(template, response.brand[x])
      $brand.click()
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
        template = "<option value=\"{{ model_id }}\" {{!sel}}>{{ model }}</option>"
        $model = $("select[name=model]")
        $model.empty()
        for x of response.model
            tmp = template
            if response.model[x].model_id is "MO000"
                tmp = tmp.replace "{{!sel}}", "selected"
            $model.append Mustache.render(tmp, response.model[x])
      else
        $().toastmessage "showWarningToast", "No se a podido obtener la lista de marcas."
      return
  return

searchUnitOption = ->
  $unit = $("[name=unit]")
  if $unit.length
    data =
      list: true
    $.get "/unit/list/", data, (response) ->
      if response.status
        template = """<option selected>--Elije una unidad--</option>{{#lunit}}<option value="{{unidad_id}}">{{uninom}}</option>{{/lunit}}"""
        $unit.empty()
        $unit.html Mustache.render template, response
        return
      else
        $().toastmessage "showWarningToast", "Error al listar unidades"
        return
    return
  return

globalDataBrand = new Object
getDataBrand = ->
  $.getJSON "/json/brand/list/option/", (response) ->
    globalDataBrand = response.brand
    if response.status
      return response.brand
    else
      return new Object
  return
globalDataModel = new Object
getDataModel = ->
  $.getJSON "/json/model/list/option/", (response) ->
      if response.status
        globalDataModel = response.model
        return response.model
      else
        return new Object
  return

setDataBrand = (element, value)->
    $.getJSON "/json/brand/list/option/", (response) ->
        if response.status
            template = "<option value=\"{{ brand_id }}\" {{!sel}}>{{ brand }}</option>"
            $sel = $("#{element}")
            $sel.empty()
            for x of response.brand
                tmp = template
                if response.brand[x].brand_id is value
                    tmp = tmp.replace "{{!sel}}", "selected"
                $sel.append Mustache.render tmp, response.brand[x]
            return
    return

setDataModel = (element, value)->
    $.getJSON "/json/model/list/option/", (response) ->
        if response.status
            template = "<option value=\"{{ model_id }}\" {{!sel}}>{{ model }}</option>"
            $sel = $("#{element}")
            $sel.empty()
            for x of response.model
                tmp = template
                if response.model[x].model_id is value
                    tmp = tmp.replace "{{!sel}}", "selected"
                $sel.append Mustache.render tmp, response.model[x]
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

# open window
openBrand = ->
    url = "/brand/new/"
    win = window.open url, "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600"
    interval = window.setInterval ->
        if win == null or win.closed
            window.clearInterval interval
            searchBrandOption()
            return
    , 1000
    return win;

openModel = ->
    url = "/model/new/"
    win = window.open url, "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600"
    interval = window.setInterval ->
        if win == null or win.closed
            window.clearInterval interval
            searchModelOption()
            return
    , 1000
    return win;

#/ Add Event Listener
$(document).on "click", "select[name=brand]", (event) ->
  searchModelOption()
  return
$(document).on "keyup", "input[name=description]", keyDescription
$(document).on "keypress", "input[name=description]", keyUpDescription
$(document).on "click", "select[name=meter]", getSummaryMaterials
$(document).on "keypress", "input[name=code]", keyCode
# Listeners groups
$(document).on "click", ".bg-modal-view-details", getDetailsGroupMaterials
$(document).on "click", ".bg-modal-back", bgModalBack
$(document).on "click", ".bg-modal-erase", bgModalErase
$(document).on "click", ".bg-modal-save", bgModalAddMaterials
# Open window
$(document).on "click", ".btn-new-brand", openBrand
$(document).on "click", ".btn-new-model", openModel

# Templates
modalGlobalGroupMaterial = "
<div class=\"modal fade\" id=\"searchGroupModalGlobal\" data-backdrop=\"static\">
    <div class=\"modal-dialog modal-lg\">
        <div class=\"modal-content\">
            <div class=\"modal-header\">
                <h4 class=\"modal-title\">
                    Grupo de Materiales
                </h4>
            </div>
            <div class=\"modal-body global-group-modal-one\">
                <input type=\"hidden\" id=\"gparent\">
                <div class=\"alert alert-block alert-warning hide msgparent\">
                    <strong>Alerta!</strong>
                    <p>
                        El material no cuenta con un grupo de materiales diseñado para este, pero existén parecidos.
                    </p>
                </div>
                <div class=\"table-responsive\">
                    <table class=\"table table-condensed table-hover table-group-materials-global\">
                        <thead>
                        <tr>
                        <th>Item</th>
                        <th>Descripción</th>
                        <th>Material</th>
                        <th>Tipo</th>
                        <th></th>
                        </tr>
                        </thead>
                        <tbody></tbody>
                    </table>
                </div>
            </div>
            <div class=\"modal-body global-group-modal-two hide\">
                <div class=\"alert alert-info alert-block\">
                    <a data-dismiss=\"alert\" class=\"close\">&times;</a>
                    <strong>Ten encuenta.</strong>
                    <p>
                        Que los cambios realizados en este cuadro son locales no afectán al grupo de materiales guardado inicialmente.
                    </p>
                </div>
                <div class=\"table-responsive\">
                    <table class=\"table table-condensed table-hover table-group-materials-details-global\">
                        <thead>
                        <tr>
                        <th>Item</th>
                        <th>Código</th>
                        <th>Descripción</th>
                        <th>Medida</th>
                        <th>Und</th>
                        <th>Cantidad</th>
                        <th></th>
                        </tr>
                        </thead>
                        <tbody></tbody>
                    </table>
                </div>
            </div>
            <div class=\"modal-footer\">
                <button class=\"btn btn-default btn-sm pull-left bg-modal-erase\">
                    <span class=\"glyphicon glyphicon-remove\"></span>
                    No añadir grupo
                </button>
                <button class=\"btn btn-default btn-sm pull-left bg-modal-back hide\">
                    <span class=\"fa fa-chevron-circle-left\"></span>
                    Regresar
                </button>
                <button class=\"btn btn-danger btn-sm bg-modal-create hide\" disabled>
                    <span class=\"fa fa-list-alt\"></span>
                    Crear Grupo
                </button>
                <button class=\"btn btn-primary btn-sm bg-modal-save hide\">
                    <span class=\"fa fa-save\"></span>
                    Añadir grupo
                </button>
            </div>
        </div>
    </div>
</div>
"

###
For search group materials
<div class="col-md-2">
    <div class="form-group has-warning">
        <label class="control-label">Incluir Grupo</label>
        <!-- <div class="btn-group" data-toggle="buttons">
            <label class="btn btn-sm btn-danger btn-block"> -->
            <input type="checkbox" name="gincludegroup" value="0">
             <!--    GM
            </label>
        </div> -->
    </div>
</div>
###
###
# For Sear Material Template
<div class="panel-body panel-add bg-warning">
    <div class="row">
        <div class="col-md-12">
            <div class="row">
                <div class="col-md-4">
                    <div class="form-group has-warning">
                        <label class="control-label">Descripción / Nombre de material</label>
                        <input type="text" class="form-control input-sm" name="description">
                        <ul id="matname-global" class="matname-global"></ul>
                    </div>
                </div>
                <div class="col-md-2">
                    <div class="form-group has-warning">
                        <label class="control-label">Código</label>
                        <input type="text" class="form-control input-sm" maxlength="15" name="code">
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-group has-warning">
                        <label class="control-label">Medida</label>
                        <select class="form-control input-sm" name="meter"></select>
                    </div>
                </div>
                <div class="col-md-6">
                  <div class="row">
                    <div class="col-md-4">
                        <div class="form-group has-warning">
                            <label class="control-label">Metrado/Cantidad</label>
                            <input type="text" class="form-control input-sm" name="quantity" min="1" placeholder="0">
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="form-group has-warning">
                            <label class="control-label">Precio</label>
                            <input type="text" class="form-control input-sm" name="price" min="1" placeholder="0">
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="form-group has-warning">
                            <label class="control-label">Marca</label>
                            <div class="input-group">
                                <select name="brand" id="brand" class="form-control input-sm"></select>
                                <span class="input-group-btn">
                                    <button class="btn btn-sm btn-default btn-new-brand"><span class="glyphicon glyphicon-plus"></span></button>
                                </span>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="form-group has-warning">
                            <label class="control-label">Modelo</label>
                            <div class="input-group">
                                <select name="model" id="model" class="form-control input-sm"></select>
                                <span class="input-group-btn">
                                    <button class="btn btn-default btn-sm btn-new-model"><span class="span glyphicon glyphicon-plus"></span></button>
                                </span>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="form-group has-warning">
                            <label class="control-label">Incluir Grupo</label>
                            <input type="checkbox" name="gincludegroup" value="0">
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="form-group has-warning">
                            <label class="control-label">Agregar</label>
                            <button class="btn btn-block btn-warning text-black btn-add">
                                <span class="glyphicon glyphicon-plus"></span>
                            </button>
                        </div>
                    </div>
                    <div class="col-md-12">
                        <p>
                            <small>
                                El precio del sistema esta expresado en <q class="currency-name">{{ system.moneda.moneda }}</q>
                            </small>
                        </p>
                    </div>
                  </div>
                </div>
                <div class="col-md-6">
                    <div class="alert alert-warning alert-block">
                        <strong>Resumén</strong>
                        <table class="table-condensed tb-details">
                            <tbody></tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
###