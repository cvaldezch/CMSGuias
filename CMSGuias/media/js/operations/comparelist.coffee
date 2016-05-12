app = angular.module "compareApp", ['ngCookies',]
      .config ($httpProvider) ->
              $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
              $httpProvider.defaults.xsrfCookieName = 'csrftoken'
              $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
              return
# ctrl.$inject = ['$scope', '$http', '$timeout', 'fDSMetrado']
app.factory 'fDSMetrado', ($http, $cookies, $q) ->
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
  obj = new Object
  uri = location.pathname
  obj.getCompare = ->
    deffered = $q.defer()
    $http.get "#{uri}", params: 'glist': true
    .success (response) ->
      deffered.resolve response
      return
    return deffered.promise
  obj.getDataMaterials = (materials) ->
    deffered = $q.defer()
    prm =
      'brandbymaterials': true
      'materials': materials
    $http.get "/brand/list/", params: prm
    .success (response) ->
      deffered.resolve response
      return
    return deffered.promise
  obj.getModel = (brand) ->
    # deffered = $q.defer()
    prm =
      'modelbybrand': true
      'brand': brand
    $http.get "/brand/list/", params: prm
    # deffered.promise
  obj.getBrand = ->
    prm =
      lbrand: true
    $http.get "", params: prm
  obj.update = (options = {}) ->
    prm = options
    $http.get "", params: prm
  obj.saveBrand = (options = {}) ->
    $http
      url: ''
      method: 'post'
      data: $.param options
  obj.saveModel = (options = {}) ->
    $http
      url: ''
      method: 'post'
      data: $.param options
  obj
app.controller 'ctrl', ($scope, $cookies, $timeout, $q, fDSMetrado) ->
  $scope.ebrand = ""
  $scope.brand = []
  $scope.model = []
  $scope.ename = ""
  $scope.eunit = ""
  angular.element(document).ready ->
    angular.element('.modal-trigger').leanModal()
    # angular.element("select").material_select()
    console.log "estamos listos!"
    $scope.loadList()
    return
  $scope.loadList = ->
    $scope.loader = false
    fDSMetrado.getCompare()
    .then (data) ->
      $scope.list = data.lst
      $scope.currency = data.currency
      $scope.symbol = data.symbol
      $scope.salesap = data.salesap
      $scope.sales = data.sales
      $scope.operations = data.operations
      $scope.diff = data.diff
      $scope.loader = true
    , (error) ->
      console.error "error al cargar los datos"
    return

  $scope.openEdit = ($event) ->
    $cell = $event.currentTarget.cells
    if $cell[9].innerText.replace(' ', '') isnt ""
      fDSMetrado.getDataMaterials($cell[1].innerText)
      .then (response) ->
        # console.log $scope.brand
        $("#medit").openModal()
        $scope.brand = response.data
        $timeout ->
           # console.log $cell
          $scope.ename = $cell[2].innerText
          $scope.eunit = $cell[5].innerText
          $scope.ematc = $cell[1].innerText
          $scope.eprice = $cell[6].innerText
          $scope.esales = $cell[7].innerText
          $scope.ebrand = $cell[0].children[0].dataset.brand
          $scope.obrand = $cell[0].children[0].dataset.brand
          $scope.omodel = $cell[0].children[0].dataset.model
          $scope.lmodel();
          # $timeout (-> $scope.model = $cell[0].children[0].dataset.model;return), 400
          return
        , 600
        $timeout ->
          $scope.emodel = $cell[0].children[0].dataset.model
          return
        , 1200
        return
      , (error) ->
        console.error error
    return

  $scope.lmodel = ->
    fDSMetrado.getModel($scope.ebrand)
    .success (response) ->
      console.log response
      $scope.model = response.model
    return
  $scope.getBrand = ->
    fDSMetrado.getBrand()
    .success (response) ->
      $scope.vbrand = response.brand
    return
  $scope.saveChange = ($event) ->
    obj =
      materials: $scope.ematc
      brand: $scope.ebrand
      model: $scope.emodel
      obrand: $scope.obrand
      omodel: $scope.omodel
      ppurchase: $scope.eprice
      psales: $scope.esales
      'saveChange': true
    fDSMetrado.update(obj)
    .success (response) ->
      if response.status
        swal
          title: "Felicidades!"
          text: ""
          type: "success"
          allowOutsideClick: false
          timer: 2600
        $scope.ematc = ""
        $scope.ename = ""
        $scope.eunit = ""
        $scope.obrand = ""
        $scope.omodel = ""
        $scope.loadList()
        $("#medit").closeModal()
      else
        swal "No se ha guardado los cambios", "", "warning"
      return
    return
  $scope.saveBrand = ->
    prm = 
      'brand': $scope.nbrand
      'saveBrand': true
    fDSMetrado.saveBrand(prm)
    .success (response) ->
      if response.statuts
        angular.element("#mbrand").closeModal()
      else
        swal "No se ha guardado los cambios", "", "warning"
    return
  $scope.saveModel = ->
    prm = 
      'brand': $scope.sbrand
      'model': $scope.nmodel
      'saveBrand': true
    fDSMetrado.saveModel(prm)
    .success (response) ->
      if response.statuts
        angular.element("#").closeModal()
      else
        swal "No se ha guardado los cambios", "", "warning"
    return
  $scope.openaBrand = ->
    angular.element("#mbrand").openModal()
    return
  $scope.openaModel = ->
    $scope.getBrand()
    angular.element("#mmodel").openModal()
    return
  $scope.closeBrand = ->
    angular.element("#mbrand").closeModal()
    return
  $scope.closeModel = ->
    angular.element("#mmodel").closeModal()
    return
  $scope.exportData = ->
    # location.href = '?export'
    window.open '?export=true', '_blank'
    return
  # $scope.$watch 'obrand', (nw, old) ->
  #   console.log nw
  #   console.log old
  #   return
  return
