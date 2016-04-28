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
  obj
app.controller 'ctrl', ($scope, $cookies, $timeout, $q, fDSMetrado) ->
  $scope.ebrand = ""
  $scope.brand = []
  $scope.model = []
  angular.element(document).ready ->
    angular.element("select").material_select()
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
    if $cell[8].innerText isnt ""
      fDSMetrado.getDataMaterials($cell[1].innerText)
      .then (response) ->
        console.log $scope.brand
        $("#medit").openModal()
        $scope.brand = response.data
        console.log response.data
        console.log $scope.brand
        $timeout ->
          angular.element("select").material_select "update"
        , 800
        return
      , (error) ->
        console.error error
    return

  $scope.lmodel = ->
    console.info $scope.ebrand
    return
  return
