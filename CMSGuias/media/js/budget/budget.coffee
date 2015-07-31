$ ->
  # $(".panel-sbudget, .panel-details-budget").hide()
  $("select").material_select()
  $(".modal-trigger").leanModal()
  $("[name=finish]").pickadate
    closeOnSelect: true
    container: 'body'
    selectMonths: true
    selectYears: 15
    format: 'yyyy-mm-dd'
  # .on 'open', ->
  #   $('[name=finish]').appendTo 'body'
  #   return
  $("[name=showBudget]").on "click", showBudget
  $("[name=saveBudget]").on "click", saveBudget
  $(".bsearchbudget").on "click", showSearchBudget
  $(".showbudgetdetails").on "click", getBudgetData
  $(".showbudgetedit").on "click", showBudgetEdit
  tinymce.init
    selector: "textarea[name=observation]"
    menubar: false
    toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image"
  $(".modal.bottom-sheet").css "max-height", "65%"
  return

showBudget = (event) ->
  $("[name=budget]").val ""
  $("#nbudget").openModal()
  console.log "leanModal"
  return

showSearchBudget = (event) ->
  $(".panel-sbudget").toggle "linear"
  return

saveBudget = (event) ->
  $.validate
    form: "#newBudget"
    errorMessagePosition: "top"
    scrollToTopOnError: true
    onError: ->
      false
    onSuccess: ->
      event.preventDefault()
      params = new Object
      params.name = $("[name=name]").val()
      params.customers = $("[name=customers]").val()
      params.address = $("[name=address]").val()
      params.country = $("[name=pais]").val()
      params.departament = $("[name=departamento]").val()
      params.province = $("[name=provincia]").val()
      params.district = $("[name=distrito]").val()
      params.hourwork = $("[name=hours]").val()
      params.finish = $("[name=finish]").val()
      params.base = $("[name=base]").val()
      params.offer = $("[name=offer]").val()
      params.currency = $("[name=currency]").val()
      params.exchange = $("[name=exchange]").val()
      params.observation = $("#observation_ifr").contents().find("body").html()
      params.csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]").val()
      params.saveBudget = true
      $edit = $("[name=budget]")
      if $edit.val()?
        params.edit = true
        params.budget = $edit.val()
      $.post "", params, (response) ->
        if response.status
          location.reload()
          return
        else
          swal "Oops Alert!", "No se han guardado lo datos correctamente. #{response.raise}", "warning"
          return
      , "json"
      false
  return

showBudgetEdit = (event) ->
  $("[name=budget]").val this.getAttribute "data-value"
  return

getBudgetData = (event) ->
  params = new Object
  params.budgetData = true
  params.budget = this.getAttribute "data-value"
  console.log params
  $.getJSON "", params, (response) ->
    if response.status
      colone = """
        <dt>Presupuesto</dt>
        <dd>{{ budget.budget_id }}</dd>
        <dt>Cliente</dt>
        <dd>{{ budget.customers }}</dd>
        <dt>Dirección</dt>
        <dd>{{ budget.address }}, {{ budget.country }}, {{ budget.departament }}, {{ budget.province }}, {{ budget.district }}</dd>
        <dt>Observación</dt>
        <dd>{{ budget.observation }}</dd>
      """
      coltwo =
        """
        <dt>Registrado</dt>
        <dd>{{ budget.register }}</dd>
        <dt>Jornada Diaria</dt>
        <dd>{{ budget.hourwork }}</dd>
        <dt>F. Entrega</dt>
        <dd>{{ budget.finish }}</dd>
        <dt>Moneda</dt>
        <dd>{{ budget.currency }}</dd>
        """
      $(".colone").html Mustache.render colone, response
      $(".coltwo").html Mustache.render coltwo, response
    else
      swal "Alerta!", "No se encontraron datos. #{response.raise}", "warning"
      return
  return

# implement AngularJS
app = angular.module 'BudgetApp', ['ngCookies', 'ngSanitize']
      .config ($httpProvider) ->
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
        $httpProvider.defaults.xsrfCookieName = 'csrftoken'
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
        return
app.controller 'BudgetCtrl', ($scope, $http, $cookies) ->
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
  # $http.defaults.headers.post['X-Requested-With'] = 'XMLHttpRequest'
  # $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
  $scope.ssearch = false
  $scope.bgbedside = false
  $scope.bgdetails = false
  $scope.details = {}
  $scope.items = {}
  $scope.showDetails = (target) ->
    params = new Object
    params.budgetData = true
    params.budget = target
    $scope.bgbedside = true
    console.log params
    $http
      url: ""
      params: params
      method: "GET"
    .success (response) ->
      if response.status
        $scope.details = response.budget
        $scope.bgdetails = true
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
  $scope.$watch 'bgdetails', (val) ->
    console.log val
    if val
      $scope.ssearch = false
      $scope.getItems()
    if not val
      $scope.details['budget_id'] = ''
    return
  return