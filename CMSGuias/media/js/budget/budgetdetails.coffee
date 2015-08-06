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
  $scope.getItem = ->
    $http.get "",
      params:
        item: true
      (response) ->
        if response.status
          console.log response
          $scope.item = response.lit
          return
        else
          swal "Error", "no se han encontrado datos. #{response.raise}", "error"
          return
    return
  return