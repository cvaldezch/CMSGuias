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
    height: 200
    toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image"
  $(".modal.bottom-sheet").css "max-height", "80%"
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
      $edit = $("[name=budget]").val()
      if typeof($edit) isnt "undefined"
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
  $scope.ssearch = false
  $scope.bgbedside = false
  $scope.test = ->
    console.log "you dblclick me!"
    return
  return