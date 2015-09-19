app = angular.module 'programingApp', ['ngCookies']
      .config ($httpProvider) ->
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
        $httpProvider.defaults.xsrfCookieName = 'csrftoken'
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
        return

app.controller 'programingCtrl', ($scope, $http, $cookies) ->
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
  $scope.group =
    rgba: ""
  angular.element(document).ready ->
    $('.modal-trigger').leanModal()
    return
  $scope.$watch 'group.colour', (val, old) ->
    $scope.group.rgba = hextorbga(val, 0.5)
    return
  $scope.saveGroup = ->
    data = $scope.group
    data.saveg = true
    $http
      url: ''
      method: 'post'
      data: $.param data
    .success (response) ->
      if response.status
        swal
          title: "Felicidades"
          text: "se guardo los datos correctamente.",
          type: "success"
          timer: 2600
        return
      else
        swal "Error", "no se a guardado los datos. #{response.raise}", "error"
        return
    return
  $scope.listGroup = ->
    data =
      'listg': true
    $http.get '', params: data
      .success (response) ->
        if response.status
          $scope.sglist = response.sg
          $("#mlgroup").openModal()
          setTimeout ->
            $('.dropdown-button').dropdown()
          , 800
          return
        else
          swal "Error!", "No se han obtenido datos. #{response.raise}", "error"
          return
    return
  $scope.showESG = ->
    console.log this.$parent.x.fields.colour
    console.log  rgbtohex this.$parent.x.fields.colour
    $scope.group =
      sgroup_id: this.$parent.x.pk
      name: this.$parent.x.fields.name
      colour: rgbtohex this.$parent.x.fields.colour
      observation: this.$parent.x.fields.observation
    $("#mgroup").openModal()
    return
  $scope.editGroup = ->
    data =
      saveg: true
    $http
      url: ''
      data: $.param data
      method: 'post'
    .success (response) ->
      if response.status
      else
        swal "Error", "Error al guardar los datos. #{response.raise}", "error"
        return
    return
  return

hextorbga = (hex, alf=1) ->
  `if (typeof(hex) == "undefined"){
    hex = ""
  }`
  if hex.charAt(0) is "#"
    hex = hex.substring(1, 7)
    r = parseInt hex.substring(0, 2), 16
    g = parseInt hex.substring(2, 4), 16
    b = parseInt hex.substring(4, 6), 16
    return """rgba(#{r},#{g},#{b},#{alf})"""
  else
    return hex

rgbtohex = (rgb) ->
  # console.log typeof rgb
  if typeof(rgb) isnt "undefined" and rgb.length > 9
    array = rgb.split(',')
    r = parseInt array[0].split('(')[1]
    g = parseInt array[1]
    b = parseInt array[2]
    # console.log r
    # console.log g
    # console.log b
    return "##{byte2Hex(r)}#{byte2Hex(g)}#{byte2Hex(b)}"
  else
    console.log "nothing rgba"
  return

byte2Hex = (n) ->
  nybHexString = "0123456789ABCDEF";
  return String(nybHexString.substr((n >> 4) & 0x0F,1)) + nybHexString.substr(n & 0x0F,1)
