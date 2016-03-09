app = angular.module 'programingApp', ['ngCookies']
      .config ($httpProvider) ->
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
        $httpProvider.defaults.xsrfCookieName = 'csrftoken'
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
        return

app.controller 'programingCtrl', ($scope, $http, $cookies, $timeout) ->
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
  $scope.group =
    rgba: ""
  $scope.perdni = ""
  $scope.area = ""
  $scope.charge = ""
  angular.element(document).ready ->
    $('.modal-trigger').leanModal()
    $(".datepicker").pickadate
      container: 'body'
      format: 'yyyy-mm-dd'
      selectMonths: true
      selectYears: true
    $scope.lgroup()
    $scope.getDSectorList()
    $(".modal").css "max-height", "80%"
    $scope.perdni = angular.element("#perdni")[0].value
    $scope.area = angular.element("#area")[0].value
    $scope.charge = angular.element("#charge")[0].value
    console.log $scope.perdni
    console.log $scope.area
    console.log $scope.charge
    return
  $scope.$watch 'group.colour', (val, old) ->
    $scope.group.rgba = hextorbga(val, 0.5)
    return
  $scope.lgroup = ->
    data =
      'listg': true
    $http.get '', params: data
      .success (response) ->
        if response.status
          $scope.sglist = response.sg
          return
        else
          swal "Error!", "No se han obtenido datos. #{response.raise}", "error"
          return
    return
  $scope.saveGroup = ->
    $("#mlgroup").closeModal()
    data = $scope.group
    data.saveg = true
    $http
      url: ''
      method: 'post'
      data: $.param data
    .success (response) ->
      if response.status
        Materialize.toast 'Se guardado correctamente', 1800
        $("#mgroup").closeModal()
        $scope.listGroup()
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
          if !$("#mlgroup").is(":visible")
            $("#mlgroup").openModal()
          setTimeout ->
            $('.dropdown-button').dropdown()
            return
          , 600
          return
        else
          swal "Error!", "No se han obtenido datos. #{response.raise}", "error"
          return
    return
  $scope.showESG = ->
    $scope.group =
      sgroup_id: this.$parent.x.pk
      name: this.$parent.x.fields.name
      colour: rgbtohex this.$parent.x.fields.colour
      observation: this.$parent.x.fields.observation
    $("#mgroup").openModal()
    return
  $scope.saveArea = ->
    data = $scope.dsector
    data.saveds = true
    form = new FormData()
    for k, v of data
      console.log "#{k} #{v}"
      form.append k, v
    if $("[name=plane]").get(0).files.length > 0
      form.append "plane", $("[name=plane]").get(0).files[0]
    form.append "csrfmiddlewaretoken", $("[name=csrfmiddlewaretoken]").val()
    $.ajax
      url: ''
      data: form
      type: 'post'
      dataType: 'json'
      contentType: false
      cache: false
      processData: false
      success: (response) ->
        if response.status
          $scope.getDSectorList()
          $("#mdsector").closeModal()
          return
        else
          swal "Error!", "No se guardo los datos. #{response.raise}", "error"
          return
    return
  $scope.datechk = ->
    start = $scope.dsector.datestart.split("-")
    end = $scope.dsector.dateend.split("-")
    start = new Date start[0], start[1], start[2]
    end = new Date end[0], end[1], end[2]
    if end < start
      console.log "fecha de termino menor a la de inicio"
      return
  $scope.getDSectorList = ->
    data =
      'listds': true
    $http.get '', params: data
      .success (response) ->
        if response.status
          $scope.dslist = response.ds
          return
        else
          swal "Error!", "No se han obtenidos datos. #{response.raise}", "error"
          return
    return
  $scope.getPrices = ->
    $http.get "", params: 'valPrices': true
    .success (response) ->
      if response.status
        $scope.withoutPrices = response.list
        console.log $scope.withoutPrices
        console.log response.list
        $("#mwithoutprices").openModal()
        console.log "Se encontraron materielas sin precio"
        return
      else
        swal "Felicidades!", "No se han encontrado materiales sin precios.", "success"
        return
    return
  $scope.savePricewithout = ($event)->
    console.log $event
    data =
      savePricewithout: true
      value: $event.target.value
      materials: $event.target.dataset.materials
      field: $event.target.dataset.field
    $http
      url: ''
      method: 'post'
      data: $.param data
    .success (response) ->
      if not response.status
        swal "Error", "No se guardo el precio, Intentelo nuevamente.", "warning"
        return
    return
  $scope.approvedAreas = ($event) ->
    swal
      title: "Aprobar Áreas?"
      text: "desea aprobar realmente todas las áreas."
      type: "warning"
      showCancelButton: true
      confirmButtonText: "Si! aprobar"
      confirmButtonColor: "#dd6b55"
      closeOnConfirm: true
      closeOnCancel: true
    , (isConfirm) ->
      if isConfirm
        $event.currentTarget.disabled = true
        $event.currentTarget.innerHTML = """<i class="fa fa-spinner fa-pulse"></i> Procesando"""
        data =
          approvedAreas: true
        $http
          url: ''
          method: 'post'
          data: $.param data
        .success (response) ->
          if response.status
            Materialize.toast "Áreas aprobadas!", 2600
            console.log response
            location.reload()
            return
          else
            $event.currentTarget.innerHTML = """<i class="fa fa-times"></i> Error"""
            swal "Error!", "No se a aprobado las áreas.", "error"
            return
        return
    return
  $scope.uploadFile = ($event) ->
    swal
      title: 'Desea procesar el archivo?'
      type: 'warning'
      showCancelButton: true
      confirmButtonColor: '#dd6b55'
      confirmButtonText: 'Si!'
      cancelButtonText: 'No!'
      closeOnCancel: true
      closeOnConfirm: true
    , (isConfirm) ->
      if isConfirm
        $event.currentTarget.disabled = true
        $event.currentTarget.innerHTML = """<i class="fa fa-spinner fa-pulse"></i> Cargando..."""
        data = new FormData()
        data.append "uploadFile", true
        data.append "upload", $("#fileUp")[0].files[0]
        data.append "csrfmiddlewaretoken", $("[name=csrfmiddlewaretoken]").val()
        console.log data
        $.ajax
          url: ""
          type: "post"
          data: data
          dataType: "json"
          cache: false
          contentType: false
          processData: false
          success: (response) ->
            console.log response
            if response.status
              $event.currentTarget.innerHTML = """<i class="fa fa-cog fa-spin"></i> Procesando"""
              data =
                processData: true
                filename: response.name
              $http
                url: ''
                method: 'post'
                data: $.param data
              .success (result) ->
                if result.status
                  Materialize.toast "Hoja Procesada!"
                  $timeout (->
                    location.reload()
                    return
                  ), 1600
                else
                  $event.currentTarget.disabled = false
                  $event.currentTarget.innerHTML = """<i class="fa fa-upload"></i> Cargar"""
                  Materialize.toast "Error al Procesar!", 2600
            else
              $event.currentTarget.disabled = false
              $event.currentTarget.innerHTML = """<i class="fa fa-upload"></i> Cargar"""
            return
        return
    return
  $scope.delarea = ($event) ->
    console.log $event
    swal
      title: "Desea eliminar el area?"
      text: "debe de tener en cuenta que se perderan todos los datos relacionados al área"
      type: "warning"
      showCancelButton: true
      confirmButtonText: "Si!, eliminar"
      confirmButtonColor: "#dd6b55"
      cancelButtonText: "No"
      closeOnConfirm: true
      closeOnCancel: true
    , (isConfirm) ->
      if isConfirm
        console.log "area del"
        data =
          'delarea': true
          'ds': $event.currentTarget.dataset.dsector
        $http
          url: ""
          data: $.param data
          method: 'post'
        .success (response) ->
          if response.status
            $scope.getDSectorList()
            return
          else
            swal "Error!", "Se a producido un error. #{response.raise}", "error"
            return
    return
  $scope.delsgroup = ($event) ->
    console.log $event
    swal
      title: "Desea eliminar el grupo?"
      text: "debe de tener en cuenta que se perderan todos los datos relacionados al grupo"
      type: "warning"
      showCancelButton: true
      confirmButtonText: "Si!, eliminar"
      confirmButtonColor: "#dd6b55"
      cancelButtonText: "No"
      closeOnConfirm: true
      closeOnCancel: true
    , (isConfirm) ->
      if isConfirm
        console.log "sgroup del"
        data =
          'delsgroup': true
          'sgroup': $event.currentTarget.dataset.sgroup
        $http
          url: ""
          data: $.param data
          method: 'post'
        .success (response) ->
          if response.status
            $scope.listGroup()
            return
          else
            console.log "#{response.raise} , query fail"
            swal "Error!", "Se a producido un error. #{response.raise}", "error"
            return
    return
  $scope.test = ->
    data =
      processData: true
      filename: `"C:\\Users\\MIDDENDORF\\Documents\\development\\django\\venvicrperu\\icrperu\\CMSGuias\\media/storage/Temp/tmpaPR15121.xlsx"`
    $http
      url: ''
      method: 'post'
      data: $.param data
    .success (result) ->
      console.log result
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
