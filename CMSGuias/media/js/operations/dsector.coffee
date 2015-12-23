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

app.controller 'DSCtrl', ($scope, $http, $cookies, $compile, $timeout) ->
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
  $scope.perarea = ""
  $scope.percharge = ""
  angular.element(document).ready ->
    $('.modal-trigger').leanModal()
    $table = $(".floatThead")
    $table.floatThead
      position: 'absolute'
      top: 65
      scrollContainer: ($table) ->
        return $table.closest('.wrapper')
    if $scope.modify > 0
      $scope.modifyList()
    else
      $scope.getListAreaMaterials()
      $scope.getProject()
      $scope.listTypeNip()
    $scope.perarea = angular.element("#perarea")[0].value
    $scope.percharge = angular.element("#percharge")[0].value
    # setTimeout ->
    #   console.log $scope.modify
    #   return
    # , 100
    return
  $scope.getListAreaMaterials = ->
    $scope.dsmaterials = []
    data =
      dslist: true
    $(".table-withoutApproved > thead").append """<tr class="white"><td colspan="13" class="center-align"><div class="preloader-wrapper big active"><div class="spinner-layer spinner-blue-only"><div class="circle-clipper left"><div class="circle"></div></div><div class="gap-patch"><div class="circle"></div></div><div class="circle-clipper right"><div class="circle"></div></div></div></div></td></tr>"""
    $http.get "", params: data
    .success (response) ->
      if response.status
        $(".table-withoutApproved > thead > tr").eq(1).remove()
        $scope.dsmaterials = response.list
        $(".floatThead").floatThead 'reflow'
        $scope.inDropdownTable ".table-withoutApproved"
        $('.dropdown-button').dropdown()
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
        return
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
      if Boolean $("#modify").length
        delete data['savepmat']
        data.savemmat = true
      if $scope.mat.hasOwnProperty("obrand")
        if $scope.mat.obrand
          data.editmat = true
      $http
        url: ""
        data: $.param data
        method: "post"
      .success (response) ->
        if response.status
          Materialize.toast "Material Agregado", 2600
          if Boolean $("#modify").length
            $scope.modifyList()
            return
          else
            $scope.getListAreaMaterials()
            if $scope.mat.hasOwnProperty("obrand")
              $scope.mat.obrand = null
              $scope.mat.omodel = null
            return
          return
        else
          swal "Error", " No se guardado los datos", "error"
          return
    return
  $scope.deleteDMaterial = ($event) ->
    swal
      title: "Eliminar material?"
      text: "realmente dese eliminar el material."
      type: "warning"
      showCancelButton: true
      confirmButtonColor: "#dd6b55"
      confirmButtonText: "Si!, eliminar"
      closeOnConfirm: true
      closeOnCancel: true
    , (isConfirm) ->
      if isConfirm
        data = $event.currentTarget.dataset
        data.delmat = true
        $http
          url: ''
          method: 'post'
          data: $.param data
        .success (response) ->
          if response.status
            $scope.getListAreaMaterials()
            return
        return
    return
  $scope.editDMaterial = ($event) ->
    $scope.mat.code = $event.currentTarget.dataset.materials
    $timeout (->
        e = $.Event 'keypress', keyCode: 13
        $("[name=code]").trigger e
        return
    ), 100
    $timeout (->
      quantity = parseFloat $event.currentTarget.dataset.quantity
      $scope.gui.smat = true
      $("[name=brand]").val $event.currentTarget.dataset.brand
      $("[name=model]").val $event.currentTarget.dataset.model
      $scope.mat =
        quantity: parseFloat quantity
        # brand: $event.currentTarget.dataset.brand
        # model: $event.currentTarget.dataset.model
        obrand: $event.currentTarget.dataset.brand
        omodel: $event.currentTarget.dataset.model
      return
    ), 300
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
      title: "Desea generar Niples para este material?"
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
            , 100
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
      if (nw < (meter * quantity)) or nw > ((meter * quantity))
        dis += Math.abs ((meter * quantity) - nw)
      else if (nw == (meter * quantity))
        dis += (meter * quantity)
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
          .removeAttr "data-materials", ""
          .removeAttr "data-quantity", ""
          .removeAttr "data-meter", ""
          $("#nipple#{data.materiales}measure").val ""
          $("#nipple#{data.materiales}type").val ""
          $("#nipple#{data.materiales}quantity").val ""
          $("#nipple#{data.materiales}quantity").val ""
          $("#nipple#{data.materiales}observation").val ""
          setTimeout ->
            $(".rf#{data.materiales}").trigger "click"
            return
          , 100
          return
        else
          swal "Error", "No se a guardado el niple.", "error"
          return
    return
  $scope.showModify = ->
    $scope.btnmodify = true
    data =
      modifyArea: true
    $http
      url: ''
      method: 'post'
      data: $.param data
    .success (response) ->
      if response.status
        location.reload()
        return
      else
        swal "Error", "No se a podido iniciar la modificación.", "error"
        return
    return
  $scope.modifyList = ->
    data =
      modifyList: true
    $http.get '', params: data
    .success (response) ->
      if response.status
        $scope.lmodify = response.modify
        $scope.calcMM()
        return
      else
        swal 'Error', 'no se a encontrado datos', 'error'
        return
    return
  $scope.showEditM = ($event) ->
    # get brand and model
    elem = this
    $http.get '/brand/list/', params: 'brandandmodel': true
    .success (response) ->
      if response.status
        $scope.brand = response
        $scope.model = response
        response.ifbrand = ->
          if this.pk == elem.$parent.x.fields.brand.pk
            return "selected"
          return
        response.ifmodel = ->
          if this.pk == elem.$parent.x.fields.model.pk
            return "selected"
          return
        btmp = """<select class="browser-default" ng-blur="saveEditM($event)" name="brand" data-old="#{elem.$parent.x.fields.brand.pk}">{{#brand}}<option value="{{pk}}" {{ifbrand}}>{{fields.brand}}</option>{{/brand}}</select>"""
        mtmp = """<select class="browser-default" ng-blur="saveEditM($event)" name="model" data-old="#{elem.$parent.x.fields.model.pk}">{{#model}}<option value="{{pk}}" {{ifmodel}}>{{fields.model}}</option>{{/model}}</select>"""
        bel = Mustache.render btmp, response
        mel = Mustache.render mtmp, response
        $($event.currentTarget.children[3]).html $compile(bel)($scope)
        $($event.currentTarget.children[4]).html $compile(mel)($scope)
        $($event.currentTarget.children[7]).html $compile("""<input type="number" ng-blur="saveEditM($event)" name="quantity" min="1" value="#{elem.$parent.x.fields.quantity}" data-old="#{elem.$parent.x.fields.quantity}" class="right-align">""")($scope)
        $($event.currentTarget.children[8]).html $compile("""<input type="number" ng-blur="saveEditM($event)" name="ppurchase" min="0" value="#{elem.$parent.x.fields.ppurchase}" data-old="#{elem.$parent.x.fields.ppurchase}" class="right-align">""")($scope)
        $($event.currentTarget.children[9]).html $compile("""<input type="number" ng-blur="saveEditM($event)" name="psales" min="0" value="#{elem.$parent.x.fields.psales}" data-old="#{elem.$parent.x.fields.psales}" class="right-align">""")($scope)
        return
    return
  $scope.saveEditM = ($event) ->
    data =
      materials: $event.currentTarget.parentElement.parentElement.children[1].innerText
      name: $event.currentTarget.name
      value: $event.currentTarget.value
    if data.name is "brand"
      data.brand = $event.currentTarget.dataset.old
      if data.value is data.brand
        return false
    else
      data.brand = $event.currentTarget.parentElement.parentElement.children[3].children[0].value
    if data.name is "model"
      data.model = $event.currentTarget.dataset.old
      if data.value is data.model
        return false
    else
      data.model = $event.currentTarget.parentElement.parentElement.children[4].children[0].value
    if data.name is 'quantity' or data.name is 'ppurchase' or data.name is 'psales'
      if parseFloat(data.value) is parseFloat ($event.currentTarget.dataset.old)
        return false
    data.editMM = true
    $http
      url: ''
      method: 'post'
      data: $.param data
    .success (response) ->
      if response.status
        $scope.calcMM()
        for x of $scope.lmodify
          if $scope.lmodify[x].fields.materials.pk is $event.currentTarget.parentElement.parentElement.children[1].innerText and $scope.lmodify[x].fields.brand.pk is data.brand and $scope.lmodify[x].fields.model.pk is data.model
            if data.name is "brand"
              $scope.lmodify[x].fields.brand.pk = $event.currentTarget.parentElement.parentElement.children[3].children[0].selectedOptions[0].value
              $scope.lmodify[x].fields.brand.fields.brand = $event.currentTarget.parentElement.parentElement.children[3].children[0].selectedOptions[0].innerText
              $event.currentTarget.dataset.old = $scope.lmodify[x].fields.brand.pk
            if data.name is "model"
              $scope.lmodify[x].fields.brand.pk = $event.currentTarget.parentElement.parentElement.children[4].children[0].selectedOptions[0].value
              $scope.lmodify[x].fields.brand.fields.brand = $event.currentTarget.parentElement.parentElement.children[4].children[0].selectedOptions[0].innerText
              $event.currentTarget.dataset.old = $scope.lmodify[x].fields.model.pk
            if data.name is "quantity"
               $scope.lmodify[x].fields.quantity = data.value
               $event.currentTarget.dataset.old = $scope.lmodify[x].fields.quantity
            if data.name is "ppurchase"
              $scope.lmodify[x].fields.ppurchase = data.value
              $event.currentTarget.dataset.old = $scope.lmodify[x].fields.ppurchase
            if data.name is "psales"
              $scope.lmodify[x].fields.psales = data.value
              $event.currentTarget.dataset.old = $scope.lmodify[x].fields.psales
            break
        Materialize.toast 'Guardado OK', 1500, 'rounded'
        return
      else
        Materialize.toast "Error, no se guardo, #{response.raise}", 1500
        return
    return
  $scope.closeEditM = ($event) ->
    for x of $scope.lmodify
      if $scope.lmodify[x].fields.materials.pk is $event.currentTarget.parentElement.parentElement.children[1].innerText and $scope.lmodify[x].fields.brand.pk is $event.currentTarget.parentElement.parentElement.children[3].children[0].selectedOptions[0].value and $scope.lmodify[x].fields.model.pk is $event.currentTarget.parentElement.parentElement.children[4].children[0].selectedOptions[0].value
        $event.currentTarget.parentElement.parentElement.children[3].innerHTML = $scope.lmodify[x].fields.brand.fields.brand
        $event.currentTarget.parentElement.parentElement.children[4].innerHTML = $scope.lmodify[x].fields.model.fields.model
        $event.currentTarget.parentElement.parentElement.children[7].innerHTML = $scope.lmodify[x].fields.quantity
        $event.currentTarget.parentElement.parentElement.children[8].innerHTML = $scope.lmodify[x].fields.ppurchase
        $event.currentTarget.parentElement.parentElement.children[9].innerHTML = $scope.lmodify[x].fields.psales
        break
    return
  $scope.delEditM = ($event) ->
    swal
      title: "Eliminar Material?"
      text: "#{$event.currentTarget.parentElement.parentElement.children[2].innerText}"
      type: "warning"
      showCancelButton: true
      confirmButtonText: "Si!, eliminar"
      confirmButtonColor: "#dd6b55"
      cancelButtonText: "No!"
      closeOnConfirm: true
    , (isConfirm) ->
      if isConfirm
        data =
          materials: $event.currentTarget.parentElement.parentElement.children[1].innerText
          brand: $event.currentTarget.dataset.brand
          model:$event.currentTarget.dataset.model
          delMM: true
        $http
          url: ""
          method: "post"
          data: $.param data
        .success (response) ->
          if response.status
            Materialize.toast "Se elimino correctamente", 1500
            $scope.modifyList()
            return
          else
            swal "Error", "No se a podido eliminar el material, intentelo otra vez.", "error"
            return
    return
  $scope.calcMM = ->
    $http.get "", params: samountp: true
    .success (response) ->
      # console.log response
      $scope.amnp = response.maarea.tpurchase
      $scope.amns = response.maarea.tsales
      $scope.ammp = response.mmodify.apurchase
      $scope.amms = response.mmodify.asale
      $scope.amsecp = response.sec[0].fields.amount
      $scope.amsecs = response.sec[0].fields.amountsales
      $scope.amstp = response.msector.tpurchase
      $scope.amsts = response.msector.tsales
    return
  $scope.delAllModifyArea = ($event) ->
    swal
      title: 'Anular Modificación?'
      text: 'se eliminara cualquier modificación realizada.'
      type: 'warning'
      showCancelButton: true
      confirmButtonColor: '#dd6b55'
      confirmButtonText: 'Anular Modificación'
      cancelButtonText: 'No!'
    , (isConfirm) ->
      if isConfirm
        data =
          'annModify': true
        $http
          url: ''
          method: 'post'
          data: $.param data
        .success (response) ->
          if response.status
            $timeout (->
              location.reload()
              return
            ), 2600
            return
          else
            swal "Alerta!", "No se a realizado la acción. #{response.raise}", "error"
            return
        return
    return
  $scope.approvedModify = ($event) ->
    swal
      title: "Aprobar modificación?"
      text: "Desea aprobar las modificaciones del área?"
      type: "warning"
      showCancelButton: true
      confirmButtonColor: "#dd6b55"
      confirmButtonText: "Si!, Aprobar"
      closeOnConfirm: true
      closeOnCancel: true
    , (isConfirm) ->
      if isConfirm
        $event.currentTarget.disabled = true
        $event.currentTarget.innerHTML = """<i class="fa fa-spinner fa-pulse"></i> Procesando"""
        data =
          approvedModify: true
        $http
          url: ""
          method: "post"
          data: $.param data
        .success (response) ->
          if response.status
            Materialize.toast "Se Aprobó!"
            $timeout (->
              location.reload()
              return
            ), 800
            return
          else
            $event.currentTarget.className = "btn red grey-text text-darken-1"
            $event.currentTarget.innerHTML = """<i class="fa fa-timescircle"></i> Error!"""
            return
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
