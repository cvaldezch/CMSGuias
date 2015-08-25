app = angular.module 'EmpApp', ['ngCookies', 'ngSanitize']
      .config ($httpProvider) ->
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
        $httpProvider.defaults.xsrfCookieName = 'csrftoken'
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
        return

app.controller "empCtrl", ($scope, $http, $cookies) ->
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
  angular.element(document).ready ->
    console.log "ready"
    $('.datepicker').pickadate
      container: 'body'
      format: 'yyyy-mm-dd'
    $('.modal-trigger').leanModal()
    $scope.listEmployee()
    return
  $scope.predicate = 'fields.firstname'
  $scope.listEmployee = ->
    $http.get '',
      params:
        'list': true
    .success (response) ->
      console.log response
      if response.status
        $scope.list = response.employee
        return
      else
        swal "Alerta!", "No se han encontrado datos.", "warning"
        return
    return
  return

