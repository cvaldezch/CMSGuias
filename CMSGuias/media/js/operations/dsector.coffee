app = angular.module 'dsApp', ['ngCookies']
      .config ($httpProvider) ->
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
        $httpProvider.defaults.xsrfCookieName = 'csrftoken'
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
        return

app.controller 'dsCtrl', ($scope, $http, $cookies) ->
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
  angular.element(document).ready ->
    # $scope.gui =
    #   pac: false
    $(".floatThead").floatThead
      zIndex: 998
    return
  $scope.getListArea = ->
    data =
      glist: true
    $http.get "", params: data, (response) ->
      if response.status
        $scope.dsmaterials = response.list
        return
      else
        swal "Error!", "al obtener la lista de materiales del área", "error"
        return
    return
  $scope.saveMateial = ->
    data =
      save: true
    console.log $scope.mat
    return
  $scope.$watch 'gui.smat', ->
      $(".floatThead").floatThead('reflow');
    return
  return