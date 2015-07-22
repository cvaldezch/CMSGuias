$ ->
  # $(".panel-sbudget, .panel-details-budget").hide()
  $("select").material_select()
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
  $.getJSON "", param, (repsonse) ->
    if response.status
      colone = """
      <dt>Presupuesto</dt>
      <dd>{{ budget.budget_id }}</dd>
      <dt>Cliente</dt>
      <dd>{{ budget.customers }}</dd>
      <dt>Dirección</dt>
      <dd></dd>
      <dt>Observación</dt>
      <dd></dd>
      """
      coltwo =
        """
        <dt>Registrado</dt>
        <dd></dd>
        <dt>Jornada Diaria</dt>
        <dd></dd>
        <dt>F. Entrega</dt>
        <dd></dd>
        <dt>Moneda</dt>
        <dd></dd>
        """
      $(".panel-budgets").toggle 800,"linear"
    else
      $().toastmessage "showErrorToast", "No se encontraron datos. #{response.raise}"
      return
  return

# implement AngularJS
app = angular.module 'BudgetApp', []
app.controller 'BudgetCtrl', ($scope) ->
  $scope.ssearch = false
  $scope.bgdetails = false
  $scope.$watch 'bgdetails', (val) ->
    console.log val
    return
  return