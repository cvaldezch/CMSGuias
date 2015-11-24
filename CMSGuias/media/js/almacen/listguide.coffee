$(document).ready ->
  $('input[name=dates]').datepicker
    showAnim: 'slide'
    dateFormat: 'yy-mm-dd'
  $('.btn-show-gv').click (event) ->
    event.preventDefault()
    $('.btn-gv').val @value
    $('.mview').modal 'show'
    return
  $('.btn-gv').click (event) ->
    event.preventDefault()
    url = "/reports/guidereferral/#{this.value}/#{this.name}/"
    window.open url, '_blank'
    return
  $('input[name=search]').change ->
    $('input[name=search]').each ->
      if @checked
        $("input[name= @value ]").attr 'disabled', false
      else
        $("input[name= @value ]").attr 'disabled', true
      return
    return
  $('.btn-search').click (event) ->
    event.preventDefault()
    searchGuide()
    return
  # search guide referral
  searchGuide = ->
    # variables
    input = null
    data = {}
    $("input[name=search]").each ->
      if @checked
        input = @value
      return
    if input isnt null
      data['tra'] = input
      $("input[name=#{input}]").each ->
        data[@id] = if $.trim(this.value) == '' then '' else @value
        return
      $.getJSON '', data, (response) ->
        if response.status
          $tb = $('tbody')
          temp = """<tr class='success tr{{guia_id}}'><td class='text-center'>{{item}}</td><td class='text-center'>{{guia_id}}</td><td>{{nompro}}</td><td>{{traslado}}</td><td>{{connom}}</td><td class='text-center'><button class='btn btn-link btn-sm text-black btn-show-gv' onClick='view(this);' value='{{guia_id}}'><span class='glyphicon glyphicon-paperclip'></span></button></td><td class='text-center'><button class='btn btn-link btn-sm text-black'  onclick='show_annular(this);' value='{{guia_id}}'><span class='glyphicon glyphicon-fire'></span></button></td></tr>"""
          $tb.empty()
          for i of response.list
            $tb.append Mustache.render(temp, response.list[i])
        return
    else
      $().toastmessage 'showWarningToast', 'Los campos se encuentrán vacios.'
    return

  $('.btn-annular').click (event) ->
    $btn = $(this)
    $btn.attr "disabled", true
    val = $('.series').html().trim()
    if val isnt ""
      data =
        'series': val
        'observation': $("[name=obser]").val()
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      $.post '', data, ((response) ->
        if response.status
          $('.mannular').modal 'hide'
          $().toastmessage 'showNoticeToast', "Se a anulado la Guía de Remisión #{val} correctamente."
          $btn.attr "disabled", false
          setTimeout (->
            location.reload()
            return
          ), 2600
        return
      ), 'json'
    else
      $().toastmessage 'showWarningToast', 'No se puede anular la Guía de Remisión.'
    return
  return

view = (tag) ->
  $('.btn-gv').val tag.value
  $('.mview').modal 'show'
  return

show_annular = (obj) ->
  $('.series').html obj.value
  $('.mannular').modal 'show'
  return
