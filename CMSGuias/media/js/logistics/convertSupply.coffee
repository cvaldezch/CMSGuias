$(document).ready ->
  $(".panel-quote,.panel-buy,.table-details").hide()
  $(".btn-proccess").on "click", showConvert
  $("[name=transfer_buy],[name=traslado_quote]").datepicker
    dateFormat: "yy-mm-dd"
    showAnim: "slide"

  $("[name=obser_quote]").focusin(->
    @setAttribute "rows", 3
    return
  ).focusout ->
    @setAttribute "rows", 1
    return

  $(".conquote,.conbuy").on "click", selectConvert
  $("[name=select]").on "change", changeRadio
  $(".btn-new").on "click", newDocument
  $(".btn-clean").on "click", cleanControls
  $(document).on "change", "input[name=chk]", changeCheck
  $(".btn-save").on "click", savedDocument
  $(".btn-finish").on "click", terminateSupply
  $("button.btn-back").on "click", comeBack
  $("button.btn-purchase").on "click", createPurchase
  $("table.table-float").floatThead
    useAbsolutePositioning: true
    scrollingTop: 50
  $(window).scroll ->
    $("table.table-float").floatThead "reflow"
  return


# functions
terminateSupply = (event) ->
  $().toastmessage "showToast",
    type: "confirm"
    sticky: true
    text: "Parece que has terminada de cotizar o compar, Deseas terminar con la order de suministro?"
    buttons: [
      {
        value: "No"
      }
      {
        value: "Si"
      }
    ]
    success: (res) ->
      if res is "Si"
        data = new Object()
        data["csrfmiddlewaretoken"] = $("[name=csrfmiddlewaretoken]").val()
        data["supply"] = $("[name=supply]").val()
        data["type"] = "finish"
        $.post "", data, ((response) ->
          console.log response
          if response.obj
            $().toastmessage "showNoticeToast", "Bien, se a completado el suministro <b>Nro " + data.supply + ".</b>"
            setTimeout (->
              location.href = "/logistics/supply/to/convert/"
              return
            ), 3000
          return
        ), "json"
      return

  return

savedDocument = (event) ->
  # validate data
  pass = false
  counter = 0
  btn = this
  data = new Object()
  arr = new Array()

  # first check whether the selected materials, at least one
  $("input[name=chk]").each ->
    if @checked
      counter += 1
      arr.push
        mid: @id
        cant: @value
        brand: @getAttribute("data-brand")
        model: @getAttribute("data-model")

    return

  if counter > 0

    # validate header data
    $(".panel-" + btn.value).find("select,input,textarea").each ->
      if $(this).is("textarea")
        data[@name.replace("_".concat(btn.value), "")] = @value
        return true
      unless $.trim(@value) is ""
        name = @name.replace("_".concat(btn.value), "")
        if name is "traslado"
          unless validateFormatDate(@value)
            $().toastmessage "showWarningToast", "Campo \"Fecha\" no valido."
            pass = false
            return pass
        data[name] = @value
        pass = true
      else
        $().toastmessage "showWarningToast", "Existe un campo vacio o no se a seleccionado, revise los campos."
        pass = false
        return false
      return

    if pass
      $().toastmessage "showToast",
        type: "confirm"
        sticky: true
        text: "Desea Generar la cotización para ".concat($("[name=supplier_" + btn.value + "]").find("option:selected").text())
        buttons: [
          {
            value: "Si"
          }
          {
            value: "No"
          }
        ]
        success: (result) ->
          if result is "Si"
            data["newid"] = (if $.trim($("[name=nro-" + btn.value + "]").val()) isnt "" then "0" else "1")
            data["id"] = $("[name=nro-" + btn.value + "]").val()  if data.newid is "0"
            data["mats"] = JSON.stringify(arr)
            data["type"] = btn.value
            data["supply"] = $("[name=supply]").val()
            data["csrfmiddlewaretoken"] = $("[name=csrfmiddlewaretoken]").val()
            console.log data
            $.post "", data, ((response) ->
              console.info response
              if response.status
                $("[name=nro-" + btn.value + "]").val response.id
                $().toastmessage "showNoticeToast", "Se ha guardado Correctamente. <br > <strong> Nro " + response.id + ".</strong><br> para el proveedor <strong>" + $("[name=supplier_" + btn.value + "]").val() + "</strong>"
                $(".btn-new").click()
              else
                $().toastmessage "showErrorToast", "Error: Not proccess <q>Transaction</q>."
              return
            ), "json"
          return

  else
    $().toastmessage "showWarningToast", "Debe seleccionar por lo menos un material."
  return

changeCheck = (event) ->
  event.preventDefault()
  counter = 0
  recount = 0
  $("[name=chk]").each ->
    unless @checked
      $("input[name=select]").attr "checked", false
      recount += 1

    #return false;
    else
      counter += 1
    return

  #console.log("re "+recount+" co "+counter);
  if recount is $("input[name=chk]").length
    $("input[name=select]").each ->
      @checked = true  if @value is 0
      return

  else if counter is $("input[name=chk]").length
    $("input[name=select]").each ->
      @checked = true  if @value is 1
      return

  return

cleanControls = (event) ->
  event.preventDefault()
  $(".panel-" + @value).find("input,select,textarea").each ->
    if $(this).is("select")
      @selectedIndex = 0
    else
      @value = ""
    return

  return

newDocument = (event) ->
  sts = Boolean($(this).attr("status"))
  unless sts
    $(this).text(" Cancelar").attr "status", "new"
    $("<span></span>").prependTo this
    $(".btn-new > span").removeClass("glyphicon-file").addClass "glyphicon-remove"
  else
    $(this).text(" Nuevo").removeAttr "status"
    $("<span></span>").prependTo this
    $(".btn-new > span").addClass("glyphicon-file").removeClass "glyphicon-remove"
  $(".btn-new > span").addClass "glyphicon"
  $(".panel-" + @value).find((if not sts then ":disabled" else "input,select,textarea,.btn-clean,.btn-save")).each ->
    $(this).attr "disabled", sts
    return

  return

changeRadio = (event) ->
  if @checked
    value = parseInt(@value)
    $("input[name=chk]").each ->
      @checked = Boolean(value)
      return
  return

getlistMateriales = (id_su) ->
  unless id_su is ""
    url = "/json/get/details/supply/#{id_su}/"
    $.getJSON url, (response) ->
      if response.status
        $tb = $(".table-details > tbody")
        $tb.empty()
        template = "<tr>
                    <td>{{ counter }}</td>
                    <td>
                        <input type=\"checkbox\" name=\"chk\" id=\"{{ materiales_id }}\" value=\"{{ cantidad }}\" data-brand=\"{{ brand }}\" data-model=\"{{ model }}\">
                    </td>
                    <td>{{ materiales_id }}</td>
                    <td>{{ materiales__matnom }}</td>
                    <td>{{ materiales__matmed }}</td>
                    <td>{{ materiales__unit }}</td>
                    <td>{{ brand }}</td>
                    <td>{{ model }}</td>
                    <td>{{ cantidad }}</td>
                    {{!price}}
                    </tr>"
        for x of response.list
          tmp = template
          if $(".col-price").is(":visible")
            tmp = tmp.replace "{{!price}}", "<td><input type=\"text\" name=\"mats\" class=\"form-control input-sm price{{ materiales_id }}\" data-quantity=\"{{ cantidad }}\" data-material=\"{{ materiales_id }}\" data-brand=\"{{ brand_id }}\" data-model=\"{{ model_id }}\" value=\"0\"></td>"
          response.list[x].counter = (parseInt(x) + 1)
          $tb.append Mustache.render(tmp, response.list[x])
        $pro = $("p.project")

        for x of response.project
            $pro.text "#{response.project[x].nompro}"
        $("table.table-float").floatThead "reflow"
  else
    $().toastmessage "showWaringToast", "Hay un error al traer la lista de materiales. Código incorrecto"
  return

showConvert = (event) ->
  $(".conquote,.conbuy").val(@name).attr
    placeholder: $(this).attr("placeholder")
    data: $(this).attr("data")

  $(".consu").html @name
  $(".mquestion").modal "show"
  $("input[name=supply]").val @name
  return

selectConvert = (event) ->
  # recover list of materials
  value = @value
  $(".table-principal").hide "blind", 600
  if @title is "quote"
    $(".panel-quote").show "slide", 600
    $("[name=traslado_quote]").val $(this).attr("placeholder")
    $("[name=storage_quote]").val $(this).attr("data")
    $(".col-price").addClass("hide")
  else
    $(".panel-buy").show "slide", 600
    $("[name=transfer_buy]").val $(this).attr("placeholder")
    $("[name=storage_buy]").val $(this).attr("data")
    $(".col-price").removeClass("hide")
  $(".table-details").show "slide", 600
  $(".mquestion").modal "hide"
  setTimeout ->
    $("div.panel-details").show "slide", 600
    getlistMateriales value
    $("table.table-float").floatThead "reflow"
    return
  , 150
  return

comeBack = (event) ->
    $(".table-principal").show "blind", 800
    $(".panel-buy").hide "slide", 150
    $(".panel-quote").hide "slide", 150
    $("div.panel-details").hide "slide", 150
    return

createPurchase = (event) ->
    mats = new Array
    $("input[name=chk]").each (index, element) ->
        if element.checked
            mats.push
                "materials": element.id
                "brand": $("input.price#{element.id}").attr "data-brand"
                "model": $("input.price#{element.id}").attr "data-model"
                "quantity": $("input.price#{element.id}").attr "data-quantity"
                "price": $("input.price#{element.id}").val()
            return
    if mats.length
        $().toastmessage "showToast",
            text: "Realmente desea Generar la Orden de Compra?"
            type: "confirm"
            sticky: true
            buttons: [{value:"Si"},{value:"No"}]
            success: (result) ->
                if result is "Si"
                    data = new FormData()
                    data.append "proveedor", $("select[name=supplier_buy]").val()
                    data.append "documento", $("select[name=documents_buy]").val()
                    data.append "pagos", $("select[name=payment_buy]").val()
                    data.append "moneda", $("select[name=currency_buy]").val()
                    if $("input[name=transfer_buy]").val() is "" or $("input[name=transfer_buy]").val().length < 10
                        $().toastmessage "showWaringToast", "Fecha de traslado vacio."
                        return false
                    data.append "traslado", $("input[name=transfer_buy]").val()
                    data.append "contacto", $("input[name=contact_buy]").val()
                    data.append "lugent", $("input[name=delivery]").val()
                    data.append "discount", $("input[name=discount]").val()
                    data.append "csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val()
                    data.append "purchase", true
                    data.append "mats", JSON.stringify mats
                    if $("input[name=deposit]").get(0).files.length
                        data.append "deposito", $("input[name=deposit]").get(0).files[0]
                    console.log data
                    $.ajax
                        url: ""
                        type: "POST"
                        data: data
                        dataType: "json"
                        contentType: false
                        processData: false
                        cache: false
                        success: (response) ->
                            if response.status
                                $().toastmessage "showNoticeToast", "Se a generado la orden de compra. #{response.purchase}"
                                return
                            else
                                $().toastmessage "showErrorToast", "No se a generado la orden de compra. #{response.raise}"
                                return
                    return
    else
        $().toastmessage "showWaringToast", "Debe de elegir por lo menos un material."
    return