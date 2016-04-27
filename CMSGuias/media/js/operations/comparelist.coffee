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
  obj.getDataMaterials = (materails) ->
    deffered = $q.defer()
    prm =
      'setdata': true
      'materails': materails
    $http.get "", params: prm
    .success (response) ->
      deffered.resolve response
      return
    return deffered.promise
  obj
app.controller 'ctrl', ($scope, $cookies, $timeout, $q, fDSMetrado) ->
  angular.element(document).ready ->
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
      .then (data) ->
        $("#medit").openModal()
        $scope.brand = data.brand
        $scope.model = data.model
      , (error) ->
        console.error error
    return
  return
