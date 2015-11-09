app = angular.module 'SGuideApp', ['ngCookies']
        .config ($httpProvider) ->
            $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
            $httpProvider.defaults.xsrfCookieName = 'csrftoken'
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
            return

app.controller 'SGuideCtrl', ($scope, $http, $cookies) ->
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
    angular.element(document).ready ->
        # pickdate
        $('.datepicker').pickadate
            selectMonths: true # Creates a dropdown to control month
            selectYears: 15
            format: 'yyyy-mm-dd'
        $scope.customersList()
        $scope.carrierList()
        $scope.listTemp()
        return
    $scope.customersList = ->
        $http.get '', params: customers: true
        .success (response) ->
            if response.status
                $scope.customers = response.customers
                return
            else
                swal "Error", "datos de los clientes. #{response.raise}", "error"
                return
        return
    $scope.carrierList = ->
        $http.get '', params: carrier: true
        .success (response) ->
            if response.status
                $scope.carriers = response.carrier
                return
            else
                swal "Error", "datos de los Transportista. #{response.raise}", "error"
                return
        return
    $scope.detCarriers = ($event) ->
        data =
            tra: $event.currentTarget.value
            detCarrier: true
        $http.get '', params: data
        .success (response) ->
            if response.status
                $scope.drivers = response.driver
                $scope.transports = response.transport
                return
            else
                swal "Error", "datos de los Transportista. #{response.raise}", "error"
                return
        return
    $scope.saveDetalle = ->
        data =
            saveMaterial: true
            materials: $(".id-mat").text()
            quantity: $scope.mat.quantity
            brand: $scope.mat.brand
            model: $scope.mat.model
        if $scope.mat.quantity <= 0
            Materialize.toast "Cantidad Invalida", 3600
            data.saveMaterial = false
        console.log data
        if data.saveMaterial
            $http
                url: ''
                data: $.param data
                method: 'post'
            .success (response) ->
                if response.status
                    $scope.listTemp()
                    Materialize.toast 'Guardado OK', 2600
                    return
                else
                    swal "Error", "No se guardo los datos", "error"
                    return
        return
    $scope.listTemp = ->
        $http.get '', params: listTemp: true
        .success (response) ->
            if response.status
                $scope.list = response.list
                setTimeout ->
                    $('.dropdown-button').dropdown()
                , 800
                return
            else
                swal "Error", "no data lista", "error"
                return
        return
    $scope.showEdit = ($event) ->
        $scope.shwaddm = true
        #$("[name=code]").val $event.currentTarget.parentElement.parentElement.parentElement.parentElement.children[1].innerText
        $scope.mat.code = $event.currentTarget.parentElement.parentElement.parentElement.parentElement.children[1].innerText
        setTimeout ->
            e = $.Event 'keypress', keyCode: 13
            $("[name=code]").trigger e
            return
        , 100
        setTimeout ->
            # $("[name=cantidad]").val $event.currentTarget.parentElement.parentElement.parentElement.parentElement.children[6].innerText
            $scope.mat.quantity = parseFloat $event.currentTarget.parentElement.parentElement.parentElement.parentElement.children[6].innerText
            $scope.mat.brand = $event.currentTarget.dataset.brand
            $scope.mat.model = $event.currentTarget.dataset.model
            # $("[name=brand]").val $event.currentTarget.dataset.brand
            # $("[name=model]").val $event.currentTarget.dataset.model
            return
        , 600
        return
    $scope.delItem = ($event) ->
        text = "#{$event.currentTarget.parentElement.parentElement.parentElement.parentElement.children[2].innerText} #{$event.currentTarget.parentElement.parentElement.parentElement.parentElement.children[3].innerText} #{$event.currentTarget.parentElement.parentElement.parentElement.parentElement.children[4].innerText}"
        swal
            title: "Eliminar Material"
            text: text
            type: 'warning'
            showCancelButton: true
            confirmButtonColor: '#dd6b55'
            confirmButtonText: 'Si!, Eliminar'
            closeOnConfirm: true
            closeOnCancel: true
        , (isConfirm) ->
            if isConfirm
                data =
                    delItem: true
                    materials: $event.currentTarget.parentElement.parentElement.parentElement.parentElement.children[1].innerText
                    brand: $event.currentTarget.dataset.brand
                    model: $event.currentTarget.dataset.model
                $http
                    url: ''
                    data: $.param data
                    method: 'post'
                .success (response) ->
                    if response.status
                        $scope.listTemp()
                        return
                    else
                        swal "Error", "No se a eliminad", "error"
                        return
                return
        return
    return
