$(document).ready ->
  $(".content, .btn-back, .btn-compress").hide()
  $(document).on "change", "[name=sel]", changeSelect
  $(".btn-delete-all").on "click", deleteTmp
  $(".btn-gen").on "click", showGen
  $(".btn-compress").on "click", compressList
  $(".btn-back").on "click", backlist
  $(".obser").focusin((event) ->
    @rows = 3
    return
  ).focusout (event) ->
    @rows = 1
    return

  $("input[name=ingreso]").datepicker
    minDate: "0"
    maxDate: "+6M"
    showAdnim: "blind"
    dateFormat: "yy-mm-dd"

  $(".btn-generate").on "click", generateSupply
  $("input[value=true]").change().attr "disabled", true
  $("input[name=chk]").attr "disabled", true
  setTimeout (->
    $(".btn-compress").click()
    return
  ), 600
  return


# functions
deleteTmp = (event) ->
  event.preventDefault()
  $().toastmessage "showToast",
    text: "Realmente desea eliminar todo el temporal de suministro?"
    sticky: true
    type: "confirm"
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
        data = {}
        data["csrfmiddlewaretoken"] = $("input[name=csrfmiddlewaretoken]").val()
        data["tipo"] = "deltmp"
        $.post "", data, (response) ->
          location.reload()
          return

      return

  return

generateSupply = (event) ->
  chk = undefined #arr = new Array(),
  pass = undefined
  data = new Object()

  # validate materials checked
  $("input[name=quote]").each ->
    if @checked

      #arr.push({"mid": this.title, "cant": this.value });
      pass = true
    else
      pass = false
    return

  if pass
    $("[name=almacen],[name=asunto],[name=ingreso]").each ->
      unless $(this).val() is ""
        data[@name] = $(this).val()
      else
        pass = false
      return

  else
    $().toastmessage "showWarningToast", "No se han seleccionado materiales para suministrar."
  if pass

    # data['mats'] = arr;
    data["obser"] = $("[name=obser]").val()

    #data['asunto'] = $("input[name=asunto]").val();
    data["csrfmiddlewaretoken"] = $("input[name=csrfmiddlewaretoken]").val()
    data.generateSupply = true
    console.log data
    $.post "", data, (response) ->
      console.log response
      if response.status
        $().toastmessage "showNoticeToast", "Suministro Generado: <br /> Nro " + response["nro"]
        setTimeout (->
          location.reload()
          return
        ), 2800
      return

  else
    $().toastmessage "showWarningToast", "Se a encontrado un campo vacio."
  return

backlist = (event) ->
  event.preventDefault()
  $(".table-first").show "slide", 400
  $(".data-condensed").hide "blind", 200
  $(".btn-gen").click()
  return

compressList = (event) ->
  event.preventDefault()
  array = new Array()

  # recover id materials
  $("input[name=chk]").each ->
    array.push @value  if @checked
    return

  if array.length > 0
    data = new Object()
    data["mats"] = JSON.stringify(array)
    $.getJSON "", data, (response) ->
      console.log response
      if response.status
        $tb = $(".data-condensed > tbody")
        template = "<tr>
                    <td>{{ item }}</td>
                    <td><input type='checkbox' name='quote' value='{{ cantidad }}' title='{{ materiales_id }}' checked DISABLED /></td>
                    <td>{{ materiales_id }}</td>
                    <td>{{ matnom }}</td>
                    <td>{{ matmed }}</td>
                    <td>{{ unidad }}</td>
                    <td>{{ brand }}</td>
                    <td>{{ model }}</td>
                    <td>{{ cantidad }}</td>
                    <td>{{ stock }}</td>
                    </tr>"
        $tb.empty()
        for x of response.list
          response.list[x].item = (parseInt(x) + 1)
          $tb.append Mustache.render(template, response.list[x])
        $(".table-first").hide "slide", 200
        $(".data-condensed").show "blind", 400
      return

  else
    $().toastmessage "showWarningToast", "No se han seleccionado materiales, para comprimir"
  return

showGen = (event) ->
  event.preventDefault()
  $(".content").toggle ->
    unless $(this).is(":hidden")
      $(".btn-gen > span").removeClass("glyphicon-chevron-down").addClass "glyphicon-chevron-up"
    else
      $(".btn-gen > span").removeClass("glyphicon-chevron-up").addClass "glyphicon-chevron-down"
    return

  return

changeSelect = (event) ->
  event.preventDefault()
  rdo = this
  $("[name=chk]").each ->
    @checked = Boolean(rdo.value)
    return

  return
