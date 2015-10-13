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

app.controller 'DSCtrl', ($scope, $http, $cookies) ->
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
  angular.element(document).ready ->
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
  $scope.unitList = ->
    $http.get '/unit/list',
      list: true
    .success (response) ->
      if response.status
        $scope.unit = response.unit
      else
        swal "Error", "no hay datos para mostrar, Unidad", "error"
        return
    return
  $scope.saveMateial = ->
    data = $scope.mat
    data.savepmat = true
    data.ppurchase = $("[name=precio]").val()
    data.psales = $("[name=sales]").val()
    data.brand = $("[name=brand]").val()
    data.model = $("[name=model]").val()
    data.code = $(".id-mat").text()
    data.unid = ''
    console.log data
    return
  $scope.$watch 'gui.smat', ->
    $(".floatThead").floatThead('reflow');
    return
  return