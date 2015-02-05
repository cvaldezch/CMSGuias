$(document).ready ->
  $(document).on "change", "input[type=radio]", selectedChk
  $(document).on "change", "input[type=checkbox]", changeChk
  $(document).on "click", "button", resgisterMaterial
  setTimeout ->
    validregisterOld()
    return
  , 600
  $("table.table-float").floatThead
      useAbsolutePositioning: false
      scrollingTop: 50
  return


# functions
resgisterMaterial = (event) ->
  event.preventDefault()
  name = @name.substr(3)
  counter = 0
  arr = new Array()
  # valid checkbox selected
  $("[name=chk#{name}]").each ->
    if @checked and not $(this).is ":disabled"
      counter += 1
      arr.push
        oid: name
        mid: @getAttribute "data-mat"
        brand: @getAttribute "data-brand"
        model: @getAttribute "data-model"
        cant: parseFloat(@value)
    return
  if counter > 0
    data = new Object()
    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
    data.mats = JSON.stringify(arr)
    data.add-ori = "PE"
    $.post "", data, (response) ->
      if response.status
        for i of arr
          $("[name=chk#{arr[i].oid}]").attr "disabled", "disabled"
      return
    , "json"
  else
    $().toastmessage "showWarningToast", "No se han seleccionado materiales."
    return
  return

changeChk = (event) ->
  event.preventDefault()
  name = @name.substr(3)
  $chk = $("[name=chk" + name + "]")
  chk = 0
  $("[name=rdo" + name + "]").each ->
    if @value is ""
      @checked = true
    else
      $("[name=btn" + name + "]").attr "disabled", false
    return

  $chk.each ->
    chk += 1  if @checked
    return

  $("[name=btn" + name + "]").attr "disabled", (if chk is 0 then true else false)
  return

selectedChk = (event) ->
  event.preventDefault()
  name = @name.substr(3)
  value = Boolean(@value)
  $("input[name=chk" + name + "]").each ->
    return true  if $(this).is(":disabled")
    @checked = value
    return

  $("button[name=btn" + name + "]").attr "disabled", not value
  return

validregisterOld = ->
  $("button").each ->
    name = @name.substr(3)
    chk = 0
    $chkt = $("input[name=chk" + name + "]")
    console.log name
    $chkt.each ->
      chk += 1  if @checked
      return

    console.log chk
    if chk is 1
      return true
    else if chk > 1 and chk < $chkt.length or chk is $chkt.length
      $("[name=rdo" + name + "]").attr "disabled", "disabled"
      $("[name=btn" + name + "]").attr "disabled", "disabled"
    $("[name=rdo" + name + "]").attr "disabled", false  if chk > 1 and chk < $chkt.length
    return

  return
