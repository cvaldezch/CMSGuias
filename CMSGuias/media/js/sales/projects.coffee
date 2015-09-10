$(document).ready ->
    $(".btn-save, .panel-pro, div.panel-second").hide()
    $("input[name=comienzo], input[name=fin]").datepicker
        "changeMonth": true
        "changeYear" : true
        "showAnim" : "slide"
        "dateFormat" : "yy-mm-dd"

    $("h4 > a").click (event) ->
        console.log @getAttribute "data-value"
        # $("table.table-#{@getAttribute "data-value"}").floatThead "reflow"
        return
    tinymce.init
        selector: "textarea[name=obser]",
        theme: "modern",
        height: 500,
        menubar: false,
        statusbar: false,
        plugins: "link contextmenu fullscreen",
        fullpage_default_doctype: "<!DOCTYPE html>",
        font_size_style_values : "10px,12px,13px,14px,16px,18px,20px",
        toolbar1: "styleselect | fontsizeselect | fullscreen |"
        toolbar2: "undo redo | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent |"

    setTimeout ->
        $(document).find("#mceu_2").click (event)->
            if $(@).attr("aria-pressed") is "false" or $(@).attr("aria-pressed") is undefined
                $(".navbar").hide()
            else if $(@).attr("aria-pressed") is "true"
                $(".navbar").show()
            return
        $(".btn-add").on "click", showaddProject
        $("[name=pais]").on "click", getDepartamentOption
        $("[name=departamento]").on "click", getProvinceOption
        $("[name=provincia]").on "click", getDistrictOption
        $(".btn-country-refresh").on "click", getCountryOption
        $(".btn-departament-refresh").on "click", getDepartamentOption
        $(".btn-province-refresh").on "click", getProvinceOption
        $(".btn-district-refresh").on "click", getDistrictOption
        $(".btn-add-customers").on "click", showCustomer
        $(".btn-add-country").on "click", showCountry
        $(".btn-add-departament").on "click", showDepartament
        $(".btn-add-province").on "click", showProvince
        $(".btn-add-district").on "click", showDistrict
        $(".btn-save").on "click", CreateProject
        $(".btn-show-edit").on "click",  openUpdateProject
        $(".btn-show-delete").on "click", deleteProject
        return
    , 2000
    $(".btn-link").hover ->
        $(@).css "color", "#808080"
        return
    , ->
        $(@).css "color", "#000"
        return
    return

showaddProject = (event) ->
    # event.preventDefault()
    $btn = $(@)
    $(".panel-pro").toggle ->
        if $(@).is(":hidden")
            $btn.find("span").eq(0).removeClass "glyphicon-remove"
            .addClass "glyphicon-plus"
            $btn.find("span").eq(1).html(" Nuevo Proyecto")
            $(".btn-save").hide()
        else
            $btn.find("span").eq(0).removeClass "glyphicon-plus"
            .addClass "glyphicon-remove"
            $btn.find("span").eq(1).html(" Cancelar")
            $(".btn-save").show()
        # $("table").floatThead "reflow"
    return

# Show upkeep country, departament, province, district, customers
showCustomer = (event) ->
    event.preventDefault()
    url = "/customers/new/"
    window.open url, "Customers", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600"

showCountry = (event) ->
    event.preventDefault()
    url = "/country/new/"
    window.open url, "Country", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=500"

showDepartament = (event) ->
    event.preventDefault()
    url = "/departament/new/"
    window.open url, "Departament", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=500"

showProvince = (event) ->
    event.preventDefault()
    url = "/province/new/"
    window.open url, "Province", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=500"

showDistrict = (event) ->
    event.preventDefault()
    url = "/district/new/"
    window.open url, "District", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=500"

# create new Project
CreateProject = (event) ->
    pass = false
    data = new Object()
    $(".panel-pro").find("input, select").each ->
        if @value is "" or @value is null
            console.log @name
            @.focus()
            pass = false
            swal "Alerta!", "campo vacio #{@name}.", "warning"
            return pass
        else
            data[@name] = $(@).val()
            pass = true
            return
    console.log data
    if pass
        data['obser'] = $("#obser_ifr").contents().find("body").html()
        data['type'] = "new"
        $.post "", data, (response) ->
            if response.status
                swal "Felicidades!", "Se registro el proyecto #{data['nompro']} correctamente!", "success"
                setTimeout ->
                    location.reload()
                , 2000
            else
                swal "Alerta!", "Error en la transacción #{response.raise}.", "warning"
        return
    return

openUpdateProject = (event) ->
    pro = @value
    url = "/almacen/keep/project/#{pro}/edit/"
    openWindow url
    return

openWindow = (url) ->
    win = window.open url, "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600"
    interval = window.setInterval ->
        if win == null or win.closed
            window.clearInterval interval
            location.reload
            return
    , 1000
    return win;

deleteProject = ->
    value = @value;
    $().toastmessage "showToast",
        text: "Eliminar Proyecto, recuerde que al eliminar a #{@title} sera permanentemente.<br>Desea Eliminar el Proyecto?",
        sticky: true
        type: "confirm"
        position: "middle-center"
        buttons: [{value:'No'},{value: 'Si'}]
        success: (result) ->
            if result is "Si"
                data =
                    "proid": value,
                    "csrfmiddlewaretoken": $("input[name=csrfmiddlewaretoken]").val()
                $.post "/almacen/keep/project/", data, (response) ->
                    if response.status
                        if $("table tbody > tr").length > 1
                            $(".tr-"+value).remove()
                            return
                        else
                            location.reload()
                            return
                ,"json"
                return
    return


app = angular.module 'proApp', ['ngSanitize', 'ngCookies']
    .config ($httpProvider) ->
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
        $httpProvider.defaults.xsrfCookieName = 'csrftoken'
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
        return

app.controller 'proCtrl', ($scope, $http, $cookies) ->
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
    # $scope.customers = []
    $scope.sfcustomers = false
    $scope.sfprojects = false
    $scope.pcustomers = true
    $scope.pprojects = false
    $scope.tadmin = false
    angular.element(document).ready ->
        $scope.listCustomers()
        $scope.permission = angular.element("[name=permission]").val()
        if $scope.permission is 'administrator' or $scope.permission is 'ventas'
            $scope.tadmin = true
        if $scope.permission is 'operaciones'
            $scope.pprojects = true
            $scope.pcustomers = false
            $scope.sfcustomers = false
            $scope.sfprojects = false
            $scope.sTable()
        return
    $scope.listCustomers = ->
        params =
            getCustomers: true
        $http.get '', params: params
            .success (response) ->
                if response.status
                    $scope.customers = response.customers
                    setTimeout ->
                        $('.collapsible').collapsible()
                        return
                    , 400
                    return
                else
                    console.log "No result. #{response.raise}"
                    return
        return
    $scope.getProjects = ->
        data =
            getProjects: true
            customer: this.x.fields.ruccliente.pk
        if !$("##{data.customer}").parent().is(":visible")
            $('.collapsible').collapsible()
            $http.get '', params: data
                .success (response) ->
                    if response.status
                        $("##{data.customer}").html Mustache.render """{{#projects}} <li class="collection-item avatar" ondblclick="location.href='manager/{{pk}}/'">
                            <i class="fa fa-building circle" onClick="location.href='manager/{{pk}}/'"></i>
                            <span class="title"><strong>{{pk}} - {{fields.nompro}}</strong></span>
                            <div class="row">
                              <div class="col l6">
                                <strong>Contacto: </strong> {{fields.contact}}
                              </div>
                              <div class="col l6"><strong>Correo: </strong> {{fields.email}}</div>
                              <div class="col l4">
                                <strong>Registrado: </strong> {{fields.registrado}}
                              </div>
                              <div class="col l4">
                                <strong>Inicio: </strong> {{fields.comienzo}}
                              </div>
                              <div class="col l4">
                                <strong>Termino: </strong> {{fields.fin}}
                              </div>
                            </div>
                            <a href="/almacen/keep/project/{{pk}}/edit/" data-ng-show="tadmin" target="popup" class="secondary-content grey-text text-darken-3s #{ if not $scope.tadmin then 'hide'}"><i class="fa fa-edit"></i></a>
                          </li>{{/projects}}""", response
                        # if $scope.permission is 'administrator' or $scope.permission is 'ventas'
                        #     $scope.tadmin = true
                        return
                    else
                        console.log "No data project. #{response.raise}"
                        return
            return
    $scope.ProjectsAll = ->
        data =
            allProjects: true
        $http.get '', params: data
            .success (response) ->
                if response.status
                    $scope.allprojects = response.projects
                    return
                else
                    console.log "error data. #{response.raise}"
                    return
        return
    $scope.showFilter = ->
        if $scope.pcustomers
            $scope.sfcustomers = !$scope.sfcustomers
        if $scope.pprojects
            $scope.sfprojects = !$scope.sfprojects
        return
    $scope.sTable = ->
        row = angular.element("#lprojects > tbody > tr")
        if not row.length
            $scope.ProjectsAll()
        return
    $scope.$watch 'scustomers', ->
        $('.collapsible').collapsible()
        return
    $scope.$watch 'permission', ->
        console.log $scope.permission
        console.log $scope.tadmin
        return
    return
