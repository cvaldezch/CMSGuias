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

app.controller 'DSCtrl', ($scope, $http, $cookies, $compile) ->
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
    # console.log this
    data =
      'lstnipp': true
      'materials': this.$parent.x.fields.materials.pk
    $http.get "", params: data
    .success (response) ->
      if response.status
        count = 1
        response.desc = ->
          return (type, render) ->
            for k, v of response.dnip
              if k is this.fields.tipo
                return render v
        response.index = -> return count++
        script = """{{#nip}}<tr class="text-12"><td class="center-align">{{index}}</td><td class="center-align">{{fields.cantidad}}</td><td class="center-align">{{fields.cantshop}}</td><td class="center-align">{{fields.tipo}}</td><td>Niple {{#desc}}{{>fields.tipo}}{{/desc}}</td><td>{{fields.materiales.fields.matmed}}</td><td>x</td><td>{{fields.metrado}} cm</td><td>{{fields.comment}}</td><td><a href="#" ng-click="nedit($event)" data-pk="{{pk}}" data-materials="{{fields.materiales.pk}}"><i class="fa fa-edit"></i></a></td><td><a href="#" ng-click="ndel($event)" data-pk="{{pk}}" data-materials="{{fields.materiales.pk}}" class="red-text text-darken-1"><i class="fa fa-trash"></i></a></td></tr>{{/nip}}"""
        $det = $(".nip#{data.materials}")
        $det.empty()
        tbs = Mustache.render script, response
        el = $compile(tbs)($scope)
        $det.html el
        $ori = $("#typenip > option").clone()
        $dest = $(".t#{data.materials}")
        $dest.empty()
        $dest.append $ori
        $scope.calNipple data.materials
        $edit = $("#nipple#{data.materials}edit")
        $edit.val ""
        $edit.removeAttr "data-materials"
        $edit.removeAttr "data-meter"
        $edit.removeAttr "data-quantity"
        return
      else
        console.log "nothing data"
        return
    return
  $scope.calNipple = (materials) ->
    tot = parseFloat($(".to#{materials}").text() * 100)
    ing = 0
    $(".nip#{materials} > tr").each ->
      $td = $(this).find("td")
      ing += (parseFloat($td.eq(1).text()) * parseFloat($td.eq(7).text().split(" cm")))
      return
    dis = (tot - ing)
    console.log tot
    console.log ing
    console.log dis
    $(".co#{materials}").html ing
    $(".dis#{materials}").html dis
    return
  $scope.ndel = ($event) ->
    swal
      title: "Eliminar Niple?"
      text: "#{$event.target.offsetParent.parentElement.childNodes[1].innerText} #{$event.target.offsetParent.parentElement.childNodes[4].innerText} #{$event.target.offsetParent.parentElement.childNodes[7].innerText}"
      type: "warning"
      showCancelButton: true
      confirmButtonColor: "#dd6b55"
      confirmButtonText: "Si, eliminar!"
      cancelButtonText: "No!"
      closeOnCancel: true
      closeOnConfirm: true
    , (isConfirm) ->
      if isConfirm
        data =
          delnipp: true
          id: $event.currentTarget.dataset.pk
          materials: $event.currentTarget.dataset.materials
        $http
          url: ""
          method: "post"
          data: $.param data
        .success (response) ->
          if response.status
            $edit = $("#nipple#{data.materials}edit")
            $edit.val ""
            $edit.removeAttr "data-materials"
            $edit.removeAttr "data-meter"
            $edit.removeAttr "data-quantity"
            setTimeout ->
              # console.log $(".rf#{data.materials}")
              $(".rf#{data.materials}").trigger 'click'
              return
            , 800
            return
          else
            swal "Error", "No se a eliminado el niple", "error"
            return
        return
    return
  $scope.nedit = ($event) ->
    materials = $event.currentTarget.dataset.materials
    $("#nipple#{materials}measure").val $event.target.offsetParent.parentElement.childNodes[7].innerText.split(" cm")[0]
    $("#nipple#{materials}type").val $event.target.offsetParent.parentElement.childNodes[3].innerText
    $("#nipple#{materials}quantity").val $event.target.offsetParent.parentElement.childNodes[1].innerText
    $("#nipple#{materials}observation").val $event.target.offsetParent.parentElement.childNodes[8].innerText
    $("#nipple#{materials}edit").val $event.currentTarget.dataset.pk
      .attr "data-materials", materials
      .attr "data-quantity", $event.target.offsetParent.parentElement.childNodes[1].innerText
      .attr "data-meter", $event.target.offsetParent.parentElement.childNodes[7].innerText.split(" cm")[0]
    setTimeout ->
      $(".sdnip#{materials}").click()
      return
    , 100
    return
  $scope.listTypeNip = ->
    $http.get "", params: 'typeNipple': true
    .success (response) ->
      if response.status
        $scope.tnipple = response.type
        return
    return
  $scope.saveNipple = ->
    row = this
    data =
      metrado: $("#nipple#{row.$parent.x.fields.materials.pk}measure").val()
      tipo: $("#nipple#{row.$parent.x.fields.materials.pk}type").val()
      cantidad: $("#nipple#{row.$parent.x.fields.materials.pk}quantity").val()
      cantshop: $("#nipple#{row.$parent.x.fields.materials.pk}quantity").val()
      comment: $("#nipple#{row.$parent.x.fields.materials.pk}observation").val()
      materiales: row.$parent.x.fields.materials.pk
      nipplesav: true
    if data.measure is ""
      swal "Alerta!", "No se ha ingresado una medida para este niple.", "warning"
      data.nipplesav = false
    if data.quantity is ""
      swal "Alerta!", "No se ha ingresado una cantidad para este niple.", "warning"
      data.nipplesav = false
    $edit = $("#nipple#{data.materiales}edit")
    dis = parseFloat $(".dis#{data.materiales}").text()
    nw = (parseFloat(data.cantidad) * parseFloat(data.metrado))
    if $edit.val() isnt ""
      data.edit = true
      data.id = $edit.val()
      data.materiales = $edit.attr "data-materials"
      meter = parseFloat $edit.attr "data-meter"
      quantity = parseFloat $edit.attr "data-quantity"
      if (nw < (meter * quantity))
        dis += ((meter * quantity) - nw)
    console.log dis
    console.log nw
    cl = (dis - nw)
    console.log cl
    if cl < 0
      swal "Alerta!", "La cantidad ingresada es mayor a la cantidad disponible de la tuberia.", "warning"
      data.nipplesav = false
    if data.nipplesav
      $http
        url: ""
        method: "post"
        data: $.param data
      .success (response) ->
        if response.status
          $edit.val ""
          .attr "data-materials", ""
          .attr "data-quantity", ""
          .attr "data-meter", ""
          setTimeout ->
            $(".rf#{data.materiales}").trigger 'click'
            return
          , 800
          return
        else
          swal "Error", "No se a guardado el niple.", "error"
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
    # console.log count
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
