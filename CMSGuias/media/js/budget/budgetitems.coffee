app = angular.module 'bItemsApp', ['ngCookies', 'ngSanitize']
      .config ($httpProvider) ->
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
        $httpProvider.defaults.xsrfCookieName = 'csrftoken'
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
        return
app.controller 'BItemsCtrl', ($scope, $http, $cookies) ->
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
  angular.element(document).ready ->
    console.log "init document"
    $('.modal-trigger').leanModal()
    $(".modal.bottom-sheet").css "max-height", "80%"
    $scope.showDetails()
    return

  $scope.bgdetails = false
  $scope.details = {}
  $scope.items = {}
  $scope.showDetails = ->
    params = new Object
    params.budgetData = true
    # params.budget = target
    $scope.bgbedside = true
    console.log params
    $http
      url: ""
      params: params
      method: "GET"
    .success (response) ->
      if response.status
        $scope.details = response.budget
        $scope.getItems()
        return
      else
        swal "Alerta!", "No se encontraron datos. #{response.raise}", "warning"
        return
    return
  # save Details
  $scope.saveItemBudget = ->
    console.log $scope.items
    params = $scope.items
    if not Object.getOwnPropertyNames(params).length
      swal "Alerta!", "Los campos se encontran vacios!", "warning"
      return false
    params.itag = $("[name=itag]").is(":checked")
    if params.iname is 'undefined'
      return false
    if params.ibase is 'undefined'
      return false
    if params.ioffer is 'undefined'
      return false
    params.saveItemBudget = true
    params.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
    params.name = params.iname
    params.offer = params.ioffer
    params.base = params.ibase
    params.tag = params.itag
    if typeof(params.iedit) isnt "undefined"
      params.editItem = params.iedit
      params.budgeti = params.ibudgeti
    if $("[name=budget]").val() isnt "" or not typeof($("[name=budget]").val()) is "undefined"
      params.budget_id = $("[name=budget]").val()
    else
      swal "Alerta!", "No se a encontrado el código del presupuesto.", "warning"
      return false
    $http
      url: ""
      method: "POST"
      data: $.param params
      headers:
        'Content-Type': 'application/x-www-form-urlencoded'
    .success (response) ->
      if response.status
        console.log response
        $scope.getItems()
        $scope.items = {}
        $("#mitems").closeModal()
        return
      else
        swal "Alerta!", "No se guardado los datos. #{response.raise}.", "error"
        return
    return
  $scope.getItems = ->
    params =
      listItems: true
      budget: $scope.details.budget_id
    console.log params
    $http.get "", params: params
      .success (response) ->
        if response.status
          $scope.listItems = response.items
        else
          swal "Error.", "No se ha encontrado datos.  #{response.raise}", "error"
          return
    return
  $scope.showEditItem = ->
    console.log this.mi
    $scope.items =
      iname: this.mi.name
      ibase: this.mi.base
      ioffer: this.mi.offer
      itag: this.mi.tag
      iedit: true
      ibudgeti: this.mi.budgeti
    console.log $scope.items
    $("#mitems").openModal()
    $('.dropdown-button').dropdown()
    return
  $scope.actionCopy = ->
    return

  # $scope.$watch 'bgdetails', (val) ->
  #   console.log val
  #   if val
  #     $scope.ssearch = false
  #   if not val
  #     $scope.details['budget_id'] = ''
  #   return