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
    $http.get "", params: params
      .success (response) ->
        if response.status
          $scope.details = response.details
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

  return