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
    $scope.getListAreaMaterials()
    $scope.getProject()
    $('.modal-trigger').leanModal()
    # $table = $(".floatThead")
    # $table.floatThead
    #   zIndex: 998
    # angular.element($window).bind 'resize', ->
    #   if $window.innerWidth < 980
    #     $(".floatThead").floatThead 'destroy'
    #   if $window.innerWidth > 981
    #     $(".floatThead").floatThead 'reflow'
    #     return
    return
  $scope.getListAreaMaterials = ->
    data =
      dslist: true
    $http.get "", params: data
    .success (response) ->
      if response.status
        console.log response
        $scope.dsmaterials = response.list
        console.log $scope.dsmaterials
        return
      else
        swal "Error!", "al obtener la lista de materiales del área", "error"
        return
    return
  # $scope.unitList = ->
  #   $http.get '/unit/list',
  #     list: true
  #   .success (response) ->
  #     if response.status
  #       $scope.unit = response.unit
  #       return
  #     else
  #       swal "Error", "no hay datos para mostrar, Unidad", "error"
  #       return
  #   return
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
      $http
        url: ""
        data: $.param data
        method: "post"
      .success (response) ->
        if response.status
          $scope.getListAreaMaterials()
          return
        else
          swal "Error", " No se guardado los datos", "error"
          return
    console.log data
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
        $scope.ascsector = response.sector
        return
      else
        swal "Error", "No se pudo cargar los datos del sector", "error"
        return
    return
  # $scope.$watch 'gui.smat', ->
  #   $(".floatThead").floatThead 'reflow'
  #   return
  return