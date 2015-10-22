app = angular.module 'dsApp', ['ngCookies']
      .config ($httpProvider) ->
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
        $httpProvider.defaults.xsrfCookieName = 'csrftoken'
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
      .directive 'stringToNumber', ->
          require: 'ngModel'
          link: (scope, element, attrs, ngModel) ->
            ngModel.$parsers.push (value) ->
              return '' + value
            ngModel.$formatters.push (value) ->
              return parseFloat value, 10
            return

app.controller 'DSCtrl', ($scope, $http, $cookies) ->
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
  angular.element(document).ready ->
    $('.modal-trigger').leanModal()
    $scope.getListAreaMaterials()
    $scope.getProject()
    $scope.listTypeNip()
    $table = $(".floatThead")
    $table.floatThead
      position: 'absolute'
      top: 65
      scrollContainer: ($table) ->
        return $table.closest('.wrapper')
    # $table.floatThead
    #   zIndex: 998
    # angular.element($window).bind 'resize', ->
    #   if $window.innerWidth < 980
    #     $(".floatThead").floatThead 'destroy'
    #   if $window.innerWidth > 981
    #     $(".floatThead").floatThead 'reflow'
    #     return
    return
  $scope.getListAreaMaterials = ->
    data =
      dslist: true
    $http.get "", params: data
    .success (response) ->
      if response.status
        $scope.dsmaterials = response.list
        $(".floatThead").floatThead 'reflow'
        $scope.inDropdownTable ".table-withoutApproved"
        return
      else
        swal "Error!", "al obtener la lista de materiales del área", "error"
        return
    return
  $scope.inDropdownTable = (table) ->
    # console.log $("#{table} > tbody > tr").length
    if $("#{table} > tbody > tr").length > 0
      $('.dropdown-button').dropdown()
      return false
    else
      setTimeout ->
        $scope.inDropdownTable table
      , 1400
    return
  $scope.saveMateial = ->
    data = $scope.mat
    data.savepmat = true
    data.ppurchase = $("[name=precio]").val()
    data.psales = $("[name=sales]").val()
    data.brand = $("[name=brand]").val()
    data.model = $("[name=model]").val()
    data.code = $(".id-mat").text()
    if data.quantity <= 0
      swal "Alerta!", "Debe de ingresar una cantidad!", "warning"
      data.savepmat = false
    if data.ppurchase <= 0
      swal "Alerta!", "Debe de ingresar un precio de Compra!", "warning"
      data.savepmat = false
    if data.psales <= 0
      swal "Alerta!", "Debe de ingresar un precio de Venta!", "warning"
      data.savepmat = false
    if data.savepmat
      $http
        url: ""
        data: $.param data
        method: "post"
      .success (response) ->
        if response.status
          $scope.getListAreaMaterials()
          return
        else
          swal "Error", " No se guardado los datos", "error"
          return
    return
  $scope.getProject = ->
    $http.get "/sales/projects/",
    params: 'ascAllProjects': true
    .success (response) ->
      if response.status
        $scope.ascprojects = response.projects
        return
      else
        swal "Error", "No se a cargado los proyectos", "error"
        return
    return
  $scope.getsector = (project) ->
    $http.get "/sales/projects/sectors/crud/",
    params: 'pro': project, 'sub': ''
    .success (response) ->
      if response.status
        $scope.ascsector = response.list
        return
      else
        swal "Error", "No se pudo cargar los datos del sector", "error"
        return
    return
  $scope.ccopyps = (sector) ->
    swal
      title: 'Copiar lista de Sector?'
      text: 'Realmente desea realizar la copia.'
      type: 'warning'
      showCancelButton: true
      confirmButtonColor: '#dd6b55'
      confirmButtonText: 'Si, Copiar'
      cancelButtonText: 'No, Cancelar'
      closeOnConfirm: true
      closeOnCancel: true
    , (isConfirm) ->
      if isConfirm
        if sector
          data =
            project: sector.substring(0, 7)
            sector: sector
            copysector: true
          $http
            url: ""
            method: "post"
            data: $.param data
          .success (response) ->
            if response.status
              location.reload()
              return
            else
              swal "Error", "No se a guardado los datos.", "error"
              return
          return
        else
          swal "Alerta!", "El código de sector no es valido.", "warning"
          return
    return
  $scope.delAreaMA = ->
    swal
      title: 'Realmente desea eliminar?'
      text: 'toda la lista de materiales de esta area.'
      type: 'warning'
      showCancelButton: true
      confirmButtonColor: '#dd6b55'
      confirmButtonText: 'Si, Eliminar'
      cancelButtonText: 'No, Cancelar'
    , (isConfirm) ->
      if isConfirm
        $http
          url: ""
          data: $.param 'delAreaMA': true
          method: 'post'
        .success (response) ->
          if response.status
            location.reload()
            return
          else
            swal "Alerta", "no se elimino los materiales del área", "warning"
            return
        return
    return
  $scope.availableNipple = ->
    mat = this
    swal
      title: "Desea generar Niples de este materiales?"
      text: "#{mat.$parent.x.fields.materials.fields.matnom} #{mat.$parent.x.fields.materials.fields.matmed}"
      type: "warning"
      showCancelButton: true
      confirmButtonColor: "#dd6b55"
      confirmButtonText: "Si, habilitar Niple"
      cancelButtonText: "No"
      timer: 2000
      (isConfirm) ->
        if isConfirm
          $http
            url: ""
            data:
              $.param
                'availableNipple': true
                'materials': mat.$parent.x.fields.materials.pk
                'brand': mat.$parent.x.fields.brand.pk
                'model': mat.$parent.x.fields.model.pk
            method: "post"
          .success (response) ->
            if response.status
              swal "Información", "Nipple habilitado para el material", "info"
              return
          return
    return
  $scope.listNipple = ->
    data =
      'lstnipp': true
      'materials': this.$parent.x.fields.materials.pk
    $http.get "", params: data
    .success (response) ->
      if response.status
        # """<script type="text/ng-template" id="nip#{data.materials}"></script>"""
        script = """{{#nip}}<tr><td></td><td>{{cantidad}}</td><td></td><td>{{}}</td><td></td><td>{{metrado}}</td><td>{{comment}}</td><td></td></tr>{{/nip}}"""
        $det = $(".nip#{data.materials}")
        $det.empty()
        $det.append Mustache.render script, response
        $ori = $("#typenip > option").clone()
        $dest = $(".t#{data.materials}")
        $dest.empty()
        $dest.append $ori
        # $scope["np#{data.materials}"] = response.nip
        return
      else
        console.log "nothing data"
        return
    return
  $scope.listTypeNip = ->
    $http.get "", params: 'typeNipple': true
    .success (response) ->
      if response.status
        $scope.tnipple = response.type
        return
    return
  $scope.$watch 'ascsector', ->
    if $scope.ascsector
      $scope.fsl = true
      $scope.fpl = true
      return
  $scope.$watch 'dsmaterials', ->
    count = 0
    for k of $scope.dsmaterials
      if $scope.dsmaterials[k].fields.nipple
        count++
    console.log count
    if count
      $scope.snipple = true
      setTimeout ->
        $('.collapsible').collapsible()
        return
      , 800
    return
  # $scope.$watch 'gui.smat', ->
  #   $(".floatThead").floatThead 'reflow'
  #   return
  return
