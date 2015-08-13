app = angular.module 'bidApp', ['ngCookies', 'ngSanitize']
      .config ($httpProvider) ->
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
        $httpProvider.defaults.xsrfCookieName = 'csrftoken'
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
        return

app.controller 'bidCtrl', ($scope, $http, $cookies) ->
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
  angular.element(document).ready ->
    console.log 'init document'
    $(".modal-trigger").leanModal()
    $scope.getItem()
    return
  $scope.item = {}
  $scope.getItem = ->
    $http.get "",
      params:
        item: true
    .success (response) ->
      if response.status
        $scope.item = response.lit[0]
        # console.log $scope.item
        return
      else
        swal "Error", "no se han encontrado datos. #{response.raise}", "error"
        return
    return
  $scope.listDetails = ->
    params =
      listDetails: true
    $http.get "", params: params
      .success (response) ->
        if response.status
          $scope.details = response.lanalysis
          console.log $scope.details
          return
        else
          swal "Alerta!", "No se han encontrado datos. #{response.raise}", "warning"
          return
    return
  $scope.actionEdit = ->
    params = details
    $http
      url: ''
      method: 'post'
      data: $.param params
    .success (response) ->
      if response.status
        $scope.list
      else
        swal "Error!", "No se a podido guardar los cambios. #{response.raise}", "error"
        return
    return
  $scope.searchAnalysis = ($event) ->
    if $event.keyCode is 13
      params =
        searchBy: $event.currentTarget.name
        searchVal: $event.currentTarget.value
        searchAnalysis: true
      $http.get "", params: params
        .success (response) ->
          if response.status
            $scope.listAnalysis = response.analysis
            return
          else
            swal "Alerta!", "No hay datos para tu busqueda", "info"
            return
    return
  $scope.showAnalysis = ->
    $scope.adda =
      analysis: this.x.analysis
      name: this.x.name
      unit: this.x.unit
      performance: this.x.performance
      amount: this.x.amount
    $("#manalysis").closeModal()
    $scope.ashow = true
    return
  $scope.addAnalysis = ->
    data = $scope.adda
    # console.log typeof data.quantity
    if typeof(data.quantity) is "undefined"
      swal "Alerta!", "No se a ingresado una cantidad para el analisis.", "warning"
      return false
    data.addAnalysis = true
    $http
      method: "post"
      url: ""
      data: $.param data
    .success (response) ->
      if response.status
        $scope.listDetails()
        $scope.ashow = false
        return
      else
        swal "Error", "No se podido agregar el analysis", "error"
        return
    console.log data
    return
  return