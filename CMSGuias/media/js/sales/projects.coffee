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
    $(".btn-show-group").on "click", showGroup
    $(".btn-show-table").on "click", showTable
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
            $().toastmessage "showWarningToast", "campo vacio #{@name}."
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
                $().toastmessage "showNoticeToast", "Se registro el proyecto #{data['nompro']} correctamente!"
                setTimeout ->
                    location.reload()
                , 2000
            else
                $().toastmessage "showErrorToast", "Error en la transacción #{response.raise}."
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

showGroup = (event) ->
    $("div.panel-second").fadeOut()
    $("div.panel-first").fadeIn()

showTable = (event) ->
    $("div.panel-first").fadeOut()
    $("div.panel-second").fadeIn()
    # $("table").floatThead "reflow"

app = angular.module 'proApp', ['ngSanitize', 'ngCookies']
    .config ($httpProvider) ->
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
        $httpProvider.defaults.xsrfCookieName = 'csrftoken'
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
        return

app.controller 'proCtrl', ($scope, $http, $cookies) ->
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
    $scope.customers = []
    angular.element(document).ready ->
        $scope.listCustomers()
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
        console.log this
        data =
            getProjects: true
            customer: this.x.fields.ruccliente.pk
        console.log data
        $http.get '', params
            .success (response) ->
                if response.status
                    $scope[data.customer] = response
                    return
                else
                    console.log "No data project. #{response.raise}"
                    return
        return
    return
