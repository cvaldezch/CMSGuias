app = angular.module 'supApp', ['ngCookies', 'ngSanitize']
      .config ($httpProvider) ->
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
        $httpProvider.defaults.xsrfCookieName = 'csrftoken'
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
        return

app.controller 'supCtrl', ($scope, $http, $cookies) ->
  $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
  $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
  angular.element(document).ready ->
    console.log "ready"
    $('.datepicker').pickadate
      container: 'body'
      format: 'yyyy-mm-dd'
    $('.modal-trigger').leanModal()
    $(".modal.bottom-sheet").css "max-height", "60%"
    $scope.listSupplier()
    # $scope.listCharge()
    return
  $scope.listSupplier = ->
    $http.get '',
      params:
        'list': true
    .success (response) ->
      console.log response
      if response.status
        $scope.list = response.supplier
        return
      else
        swal "Alerta!", "No se han encontrado datos.", "warning"
        return
    return
  $scope.saveSupplier = ->
    if typeof($scope.supplier.proveedor_id) is "undefined"
      return false
    params = $scope.supplier
    params.save = true
    params.pais = $("[name=pais]").val()
    params.departamento = $("[name=departamento]").val()
    params.provincia = $("[name=provincia]").val()
    params.distrito = $("[name=distrito]").val()
    console.log params
    # $http
    #   url: ''
    #   method: 'post'
    #   data: $.param params
    # .success (response) ->
    #   if response.status
    #     swal 'Felicidades!', 'Se guardo los datos correctamente.', 'success'
    #     $scope.listEmployee()
    #     $("#madd").closeModal()
    #     return
    #   else
    #     swal 'Error', 'error al guardar los cambios.', 'error'
    #     return
    return
  $scope.showEdit = ->
    $scope.supplier =
      proveedor_id: this.x.pk
      razonsocial: this.x.fields.razonsocial
      direccion: this.x.fields.direccion
      telefono: this.x.fields.telefono
      tipo: this.x.fields.tipo
      origen: this.x.fields.origen
      contact: this.x.fields.contact
      email: this.x.fields.email
      # pais: this.x.fields.pais.pk
      # departamento: this.x.fields.departamento.pk
      # provincia: this.x.fields.provincia.pk
      # distrito: this.x.fields.distrito.pk
    option = this
    $("[name=pais]").val option.x.fields.pais.pk
      .click()
    setTimeout ->
      $("[name=departamento]").val option.x.fields.departamento.pk
        .click()
    , 800
    setTimeout ->
      $("[name=provincia]").val option.x.fields.provincia.pk
        .click()
    , 1800
    setTimeout ->
      $("[name=distrito]").val option.x.fields.distrito.pk
    , 2600
    $("#madd").openModal()
    console.log $scope.supplier
    return
  return