# load funtions of page
$(document).ready ->
  $(".description, .block-add-mat").hide()
  $(".in-date").datepicker
    minDate: "0"
    maxDate: "+2M"
    changeMonth: true
    changeYear: true
    showAnim: "slide"
    dateFormat: "yy-mm-dd"

  $(".btnadd").click ->
    aggregate_materials()
    return

  $(".btn-edit-cantidad").click ->
    edit_quantity_tmp()
    return

  $(".btn-delete-mat").click ->
    $mid = $(".del-mid")
    $dni = $(".empdni")
    $btn = $(this)
    $token = $("[name=csrfmiddlewaretoken]")
    unless $mid.html() is ""
      $btn.button "loading"
      data =
        dni: $dni.val()
        mid: $mid.html()
        csrfmiddlewaretoken: $token.val()

      $.post "/json/post/delete/tmp/materials/", data, ((response) ->
        if response.status
          $btn.button "reset"
          list_temp_materials()
          $(".modal-delete-mid").modal "hide"
        return
      ), "json"
    return

  list_temp_materials()
  $(".btn-add-mat").click ->
    $block = $(".block-add-mat")
    $btn = $(".btn-add-mat > span")
    if $block.is(":hidden")
      $block.show "blind", 600
      $btn.removeClass("glyphicon-plus").addClass "glyphicon-minus"
    else
      $block.hide "blind", 600
      $btn.addClass("glyphicon-plus").removeClass "glyphicon-minus"
    console.log "yes, go it"
    return

  $(".btn-list").click ->
    list_temp_materials()
    return

  $(".btn-niples").click ->
    get_niples()
    return

  $(".btn-del-all-temp-show").click ->
    $(".modal-delete-all-temp").modal "show"
    return

  $(".btn-up-file-show").click ->
    $(".modal-up-file").modal "show"
    return

  $(".btn-del-all-temp").click ->
    data =
      dni: $(".empdni").val()
      csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()

    $.post "/json/post/delete/all/temp/order/", data, ((response) ->
      location.reload()  if response.status
      return
    ), "json"
    return

  $(".btn-order-show").click (event) ->
    event.preventDefault()
    $(".modal-order").modal "show"
    return


  # bedside order
  # loading projects
  $.getJSON "/json/get/projects/list/", (response) ->
    if response.status
      $pro = $(".pro")
      $pro.empty()
      template = "<option value='{{proyecto_id}}'>{{nompro}}</option>"
      for x of response.list
        $pro.append Mustache.render(template, response.list[x])
    return

  $.getJSON "/json/get/stores/list/", (response) ->
    if response.status
      $al = $(".al")
      $al.empty()
      template = "<option value='{{almacen_id}}'>{{nombre}}</option>"
      for x of response.list
        $al.append Mustache.render(template, response.list[x])
    return

  $(".pro").click (event) ->
    event.preventDefault()
    $sub = $(".sub")
    $sec = $(".sec")

    # get list subprojects
    $.getJSON "/json/get/subprojects/list/",
      pro: @value
    , (response) ->
      if response.status
        template = "<option value='{{subproyecto_id}}'>{{nomsub}}</option>"
        $sub.empty()
        $sub.append "<option value=''>-- Nothing --</option>"
        for x of response.list
          $sub.append Mustache.render(template, response.list[x])
      return

    data = pro: @value
    $.getJSON "/json/get/sectors/list/", data, (response) ->
      if response.status
        template = "<option value='{{sector_id}}'>{{nomsec}} {{planoid}}</option>"
        $sec.empty()
        for x of response.list
          $sec.append Mustache.render(template, response.list[x])
      return

    return

  $(".tofile").click (event) ->
    event.preventDefault()
    $("#file").click()
    return

  $("#file").change ->
    console.log "in change"
    $(".file-container,.tofile").removeClass("alert-warning text-warning").addClass "alert-success text-success"  unless @value is ""
    return

  $(".btn-saved-order").click (event) ->
    $(".modal-order").modal "hide"
    $().toastmessage "showToast",
      text: "Seguro(a) que termino de ingresar los materiales al pedido?"
      buttons: [
        {
          value: "No"
        }
        {
          value: "Si"
        }
      ]
      type: "confirm"
      sticky: true
      success: (result) ->
        if result is "Si"
          setTimeout (->
            $().toastmessage "showToast",
              text: "Seguro(a) que termino de ingresar los Niples al pedido, recuerde que una vez que se guarde el pedido no podra modificarse.?"
              buttons: [
                {
                  value: "No"
                }
                {
                  value: "Si"
                }
              ]
              type: "confirm"
              sticky: true
              success: (resp2) ->
                if resp2 is "Si"

                  #
                  setTimeout (->
                    $().toastmessage "showToast",
                      sticky: true
                      text: "Desea Generar Pedido almacén?"
                      type: "confirm"
                      buttons: [
                        {
                          value: "No"
                        }
                        {
                          value: "Si"
                        }
                      ]
                      success: (resp3) ->
                        if resp3 is "Si"
                          data = new FormData($("form").get(0))
                          $.ajax
                            data: data
                            url: ""
                            type: "POST"
                            dataType: "json"
                            cache: false
                            processData: false
                            contentType: false
                            success: (response) ->
                              console.log response
                              location.reload()  if response.status
                              return

                        else
                          $(".modal-order").modal "show"
                        return

                    return
                  ), 600

                #
                else
                  $(".modal-order").modal "show"
                return

            return
          ), 600
        else
          $(".modal-order").modal "show"
        return

    return

  $(".obs").focus ->
    $(this).animate
      height: "102px"
    , 600
    return

  $(".obs").blur ->
    $(this).animate
      height: "34px"
    , 600
    return


  # download template
  $(".btn-down-temp").click (event) ->
    url = "/media/storage/templates/Orderstmp.xls"
    window.open url, "_blank"
    return

  $(".show-input-file-temp").click (event) ->
    event.preventDefault()
    $(".input-file-temp").click()
    return

  $(".btn-upload-file-temp").click (event) ->
    $input = $("[name=input-file-temp]").get(0)
    file = $input.files[0]
    btn = this
    if file?
      data = new FormData()
      data.append "ftxls", file
      data.append "csrfmiddlewaretoken", $("[name=csrfmiddlewaretoken]").val()
      $.ajax
        url: "/json/post/upload/orders/temp/"
        type: "POST"
        dataType: "json"
        data: data
        cache: false
        contentType: false
        processData: false
        beforeSend: ->
          $(btn).button "loading"
          return

        success: (response) ->
          $(btn).button "complete"
          if response.status
            setTimeout (->
              location.reload()
              return
            ), 1000
          return

    else
      $().toastmessage "showWarningToast", "No se a seleccionado un archivo!"
    return

  return

# add material a temp
aggregate_materials = ->
  $mid = $(".id-mat")
  $cant = $(".cantidad")
  $dni = $(".empdni")
  $token = $("[name=csrfmiddlewaretoken]")
  if $mid.html() isnt "" and $cant.val() isnt ""
    data =
      mid: $mid.html()
      cant: $cant.val()
      dni: $dni.val()
      brand: $("select[name=brand]").val()
      model: $("select[name=model]").val()
      csrfmiddlewaretoken: $token.val()
    if $("input[name=gincludegroup]").length
      if $("input[name=gincludegroup]").is(":checked")
        data.details = JSON.stringify tmpObjectDetailsGroupMaterials.details
    $.post "/json/post/aggregate/tmp/materials/", data, ((response) ->
      console.log response
      if response.status
        list_temp_materials()
      else
        console.error "Error en la transación add"
      return
    ), "json"
  else
    console.warn "No se a ingresado codigo y cantidad."
  return


# list of materials temp
list_temp_materials = ->
  $mid = $(".id-mat")
  $mid = $(".edit-mid")  unless $(".edit-mid").html() is ""
  $.getJSON "/json/get/list/temp/order/",
    dni: $(".empdni").val()
  , (response) ->
    if response.status
      $tbody = $("[template-data-user=tmporder]")
      $tbody.empty()
      if response.list.length > 0
        template = "<tr class=\"{{!new}}\">
              <td class='text-center'>{{ item }}</td>
              <td>{{ materiales_id }}</td>
              <td>{{ matnom }}</td>
              <td>{{ matmed }}</td>
              <td>{{ brand }}</td>
              <td>{{ model }}</td>
              <td class='text-center'>{{ unidad }}</td>
              <td class='text-center'>{{ cantidad }}</td>
              <td class='text-center'>
                <button class='btn btn-xs btn-info text-black' onClick='btn_edit_show({{ materiales_id }},{{ cantidad }});'>
                  <span class='glyphicon glyphicon-edit'></span>
                </button>
              </td>
              <td class='text-center'>
                <button class='btn btn-xs btn-danger text-black' onClick='btn_delete_show({{ materiales_id }},{{ cantidad }})'>
                <span class='glyphicon glyphicon-remove'></span>
              </button>
              </td>
              </tr>"
        for x of response.list
          tmp = template
          if response.list[x].materiales_id is $mid.html()
            tmp = tmp.replace "{{!new}}", "success"
          else
            tmp = tmp.replace "{{!new}}", "warning"
          $tbody.append Mustache.render(tmp, response.list[x])
        $(".success").ScrollTo
          duration: 1000
          callback: ->
            setTimeout (->
              $(".well").ScrollTo duration: 1000
              $(".description").focus()
              return
            ), 1000
            return
    return

btn_edit_show = (id, cant) ->
  id = String(id).valueOf()
  unless id is ""
    data = mid: id
    $.getJSON "/json/get/details/materials/", data, (response) ->
      if response.status
        $(".edit-mid").html id
        $(".edit-des").html response.matnom
        $(".edit-med").html response.matmed
        $(".edit-unid").html response.unidad_id
        $(".edit-cant").val cant
        $(".modal-edit-cant").modal "show"
      return

  return

btn_delete_show = (id, cant) ->
  $.getJSON "/json/get/details/materials/",
    mid: id
  , (response) ->
    if response.status
      $(".del-mid").html id
      $(".del-des").html response.matnom
      $(".del-med").html response.matmed
      $(".del-unid").html response.unidad_id
      $(".del-cant").html cant
      $(".modal-delete-mid").modal "show"
    return

  return

edit_quantity_tmp = ->
  $mid = $(".edit-mid")
  $cant = $(".edit-cant")
  $dni = $(".empdni")
  $btn = $(".btn-edit-cantidad")
  $token = $("[name=csrfmiddlewaretoken]")
  if $mid.html() isnt "" and $cant.val() isnt 0
    $btn.button "loading"
    data =
      dni: $dni.val()
      mid: $mid.html()
      cantidad: $cant.val()

      csrfmiddlewaretoken: $token.val()

    $.post "/json/post/update/tmp/materials/", data, ((response) ->
      if response.status
        $btn.button "reset"
        $(".modal-edit-cant").modal "hide"
        list_temp_materials()
        setTimeout (->
          $(".edit-mid").html ""
          return
        ), 3000
      return
    ), "json"
  return

get_niples = ->
  template = "<div class='panel panel-default panel-warning'>" + "<div class='panel-heading'>" + "<h4 class='panel-title'>" + "<a data-toggle='collapse' class='collapsed' data-parent='#niples' onClick='list_temp_nipples({{materiales_id}});' href='#des{{materiales_id}}'>{{matnom}} - {{matmed}}</a>" + "<span class='pull-right badge badge-warning'>Quedan <span class='res{{materiales_id}}'></span> cm</span>" + "<span class='pull-right badge badge-warning'>Ingresado <span class='in{{materiales_id}}'></span> cm</span>" + "<span class='pull-right badge badge-warning'>Total {{cantidad}} {{unidad}}</span>" + "<input type='hidden' class='totr{{materiales_id}}' value='{{cantidad}}'>" + "</h4>" + "</div>" + "<div id='des{{materiales_id}}' class='panel-collapse collapse'>" + "<div class='panel-body c{{materiales_id}}'>" + "<div class='table-responsive'>" + "<table class='table table-condensed table-hover'>" + "<caption class='text-left'><div class='row'><div class='col-md-4'><div class='btn-group'>" + "<button class='btn btn-default btn-xs btn-add-nipple-{{materiales_id}}' onClick='aggregate_nipples({{materiales_id}});' type='Button' data-loading-text='Proccess...'><span class='glyphicon glyphicon-plus-sign'></span> Agregar</button>" + "<button class='btn btn-default btn-xs' onClick='list_temp_nipples({{materiales_id}});' type='Button' data-loading-text='Proccess...'><span class='glyphicon glyphicon-refresh'></span> Recargar</button>" + "<button class='btn btn-danger btn-xs' onClick='delete_all_temp_nipples({{materiales_id}});' type='Button' data-loading-text='Proccess...'><span class='glyphicon glyphicon-trash'></span> Eliminar Todo</button>" + "</div></div>" + "<div class='col-md-8'><div class='form-inline pull-right'>" + "<div class='form-group '>" + "<select name='controlnipples' class='form-control input-sm tn{{materiales_id}}' title='Tipo Niple' placeholder='Tipo Niple' DISABLED>" + "<option value='A'>A - Roscado</option><option value='B'>B - Ranurado</option><option value='C'>C - Roscado - Ranurado</option>" + "</select>" + "</div>" + "<div class='form-group col-md-4'>" + "<div class='input-group input-group-sm'><input type='number' name='controlnipples' placeholder='Medida' min='0' class='form-control input-sm mt{{materiales_id}}' DISABLED><span class='input-group-addon'><strong>cm</strong><span></div>" + "</div>" + "<div class='form-group'>" + "<input type='number' name='controlnipples' placeholder='Cantidad' min='1' class='form-control input-sm nv{{materiales_id}}' DISABLED>" + "</div>" + "<input type='hidden' class='update-id-{{materiales_id}}' value=''>" + "<input type='hidden' class='update-quantity-{{materiales_id}}' value=''>" + "<button class='btn btn-success text-black btn-sm' name='controlnipples' type='Button' onClick='saved_or_update_nipples({{materiales_id}})' DISABLED><span class='glyphicon glyphicon-floppy-save'></span> Guardar</button>" + "</div></div>" + "</caption>" + "<thead><th>Cantidad</th><th>Descripción</th><th>Diametro</th><th><th><th>Medida</th><th>Unidad</th><th>Editar</th><th>Eliminar</th></thead>" + "<tbody class='tb{{materiales_id}}'></tbody>" + "</table>" + "</div>" + "</div>" + "</div>" + "</div>"

  # bring all the tub for contruction "Nipples"
  $.getJSON "/json/get/nipples/temp/oreder/", (response) ->
    if response.status
      $collapse = $("#niples")
      $collapse.empty()
      for x of response.nipples
        $collapse.append Mustache.render(template, response.nipples[x])
    else
      $().toastmessage "showNoticeToast", "No se han encontrado Tuberia para generar niples."
    return

  return


# enable function that controls
aggregate_nipples = (mid) ->
  mid = String(mid).valueOf()
  $("[name=controlnipples]").attr "DISABLED", false
  $(".update-id-" + mid).val ""
  return

list_temp_nipples = (mid) ->
  mid = String(mid).valueOf()
  unless mid is ""
    data =
      mid: mid
      dni: $(".empdni").val()

    $.getJSON "/json/get/list/temp/nipples/", data, (response) ->
      if response.status
        $tb = $(".tb" + mid)
        template = "<tr><td class='text-center'>{{cantidad}}</td><td>{{matnom}}</td><td>{{matmed}}</td><td>x<td><td class='text-center'>{{metrado}}</td><td class='text-center'>cm</td><td class='text-center'><button type='Button' class='btn btn-xs btn-info text-black' onClick=edit_temp_nipple({{id}},{{materiales_id}},{{cantidad}},{{metrado}},'{{tipo}}');><span class='glyphicon glyphicon-edit'></span></button></td><td class='text-center'><button type='Button' class='text-black btn btn-xs btn-danger' onClick='delete_temp_nipple({{id}},{{materiales_id}})'><span class='glyphicon glyphicon-remove'></span></button></td>"
        $tb.empty()
        totcm = 0
        incm = 0
        res = 0
        totcm = ((parseInt($(".totr" + mid).val())) * 100)
        for x of response.list
          $tb.append Mustache.render(template, response.list[x])
          incm += (response.list[x].cantidad * response.list[x].metrado)
        res = totcm - incm
        $(".in" + mid).html incm
        $(".res" + mid).html res
        if res is 0 or res < 0
          $(".btn-add-nipple-" + mid).attr "disabled", true
        else
          $(".btn-add-nipple-" + mid).attr "disabled", false
      return

  return

saved_or_update_nipples = (mid) ->
  mid = String(mid).valueOf()
  $update = $(".update-id-" + mid)
  $quantity = $(".mt" + mid)
  $type = $(".tn" + mid)
  $nv = $(".nv" + mid)
  nv = 0
  pass = Boolean(false).valueOf()
  if $quantity.val().trim() is ""
    $().toastmessage "showWarningToast", "No se a ingresado una cantidad."
    return pass
  else
    pass = Boolean(true).valueOf()
    console.info pass
  if $nv.val().trim() is "" or $nv.val().trim() is 0
    nv = 1
  else
    nv = $nv.val()
  valcant = parseInt($quantity.val().trim()) * parseInt(nv)
  res = parseInt($(".res" + mid).html().trim())
  unless $update.val().trim() is ""
    uco = $(".update-quantity-" + mid).val()
    pass = (if valcant <= (parseInt(uco) + res) then Boolean(true).valueOf() else Boolean(false).valueOf())
  else if valcant > res
    pass = Boolean(false).valueOf()
    $().toastmessage "showWarningToast", "La cantidad ingresada es superior a la establecida."
    return false
  if pass and nv >= 1
    data = {}
    if $update.val().trim() is ""
      data =
        tra: "new"
        cant: $quantity.val().trim()
        mid: mid
        type: $type.val()
        veces: nv
        dni: $(".empdni").val()
        csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
    else
      data =
        tra: "update"
        id: $update.val()
        cant: $quantity.val().trim()
        mid: mid
        type: $type.val()
        veces: nv
        dni: $(".empdni").val()
        csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
    $.post "/json/post/saved/temp/nipples/", data, (response) ->
      if response.status
        list_temp_nipples mid
        $("[name=controlnipples]").attr "DISABLED", true
        $(".update-id-" + mid).val ""
        $(".update-quantity-" + mid).val ""
      return

  else
    $().toastmessage "showWarningToast", "La cantidad o la medida no se han ingresado o no son correctas."
  return

edit_temp_nipple = (id, mid, cant, med, tipo) ->
  $("[name=controlnipples]").attr "DISABLED", false
  mid = String(mid).valueOf()
  $(".mt" + mid).val med
  $(".nv" + mid).val cant
  $(".tn" + mid).val tipo
  $(".tn" + mid).attr "DISABLED", true

  #$(".nv"+mid).attr("DISABLED",true);
  $(".update-id-" + mid).val id
  $(".update-quantity-" + mid).val (parseInt(cant) * parseInt(med))
  return

delete_temp_nipple = (id, mid) ->
  $().toastmessage "showToast",
    text: "Seguro(a) que desea eliminar el niple?"
    type: "confirm"
    sticky: true
    buttons: [
      {
        value: "No"
      }
      {
        value: "Si"
      }
    ]
    success: (result) ->
      if result is "Si"
        mid = String(mid).valueOf()
        data =
          id: id
          mid: mid
          dni: $(".empdni").val()
          csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()

        $.post "/json/post/delete/temp/nipples/item/", data, ((response) ->
          if response.status
            mid = String(mid).valueOf()
            list_temp_nipples mid
          return
        ), "json"
      return

  return

delete_all_temp_nipples = (mid) ->
  $().toastmessage "showToast",
    text: "Seguro(a) que desea eliminar toda la lista de niples?"
    type: "confirm"
    sticky: true
    buttons: [
      {
        value: "No"
      }
      {
        value: "Si"
      }
    ]
    success: (result) ->
      if result is "Si"
        mid = String(mid).valueOf()
        data =
          mid: mid
          dni: $(".empdni").val()
          csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()

        $.post "/json/post/delete/all/temp/nipples/", data, ((response) ->
          if response.status
            mid = String(mid).valueOf()
            list_temp_nipples mid
          return
        ), "json"
      return

  return
