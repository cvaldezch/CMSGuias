app = angular.module 'SGuideApp', ['ngCookies']
        .config ($httpProvider) ->
            $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
            $httpProvider.defaults.xsrfCookieName = 'csrftoken'
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
            return

app.controller 'SGuideCtrl', ($scope, $http, $cookies, $timeout) ->
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
    $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
    $scope.mat = {}
    angular.element(document).ready ->
        # pickdate
        $('.datepicker').pickadate
            selectMonths: true # Creates a dropdown to control month
            selectYears: 15
            format: 'yyyy-mm-dd'
        $scope.customersList()
        $scope.carrierList()
        $scope.listTemp()
        $scope.brandmodel()
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
    $scope.brandmodel = ->
        $http.get '', params: brandandmodel: true
        .success (response) ->
            if response.status
                $scope.brand = response.brand
                $scope.model = response.model
                $scope.mat.brand = 'BR000'
                $scope.mat.model = 'MO000'
                return
            else
                console.log "No loads brand and model"
                return
        return
    $scope.saveDetalle = ->
        # first get stock
        $code = $(".id-mat")
        data =
            gstock: true
            brand: $scope.mat.brand
            model: $scope.mat.model
        console.log data
        if $code.text()
            data.code = $code.text()
        else
            data.gstock = false
            Materialize.toast "El codigo del material no es correcto", 2000
        if data.gstock
            $http.get '', params: data
            .success (response) ->
                if response.status
                    console.log "stock found"
                    if response.exact.length
                        data =
                            saveMaterial: true
                            materials: $(".id-mat").text()
                            quantity: $scope.mat.quantity
                            brand: $scope.mat.brand
                            model: $scope.mat.model

                        if $scope.mat.obrand isnt ""
                            data.obrand = $scope.mat.obrand
                        if $scope.mat.omodel isnt ""
                            data.omodel = $scope.mat.omodel
                        if data.quantity <= 0 or typeof(data.quantity) is "undefined"
                            Materialize.toast "Cantidad Invalida", 4600
                            data.saveMaterial = false
                        console.log data
                        if data.saveMaterial
                            if response.exact[0].stock >= data.quantity
                                $http
                                    url: ''
                                    data: $.param data
                                    method: 'post'
                                .success (response) ->
                                    if response.status
                                        if $scope.mat.hasOwnProperty 'obrand'
                                            $scope.mat.obrand = ''
                                        if $scope.mat.hasOwnProperty 'omodel'
                                            $scope.mat.omodel = ''
                                        $scope.listTemp()
                                        Materialize.toast 'Guardado OK', 2600
                                        $scope.mat.brand = 'BR000'
                                        $scope.mat.model = 'MO000'
                                        $scope.mat.quantity = 0
                                        return
                                    else
                                        swal "Error", "No se guardo los datos", "error"
                                        return
                                return
                            else
                                swal "Alerta!", "Stock es menor o no existe en el inventario", "warning"
                                return false
                    else
                        # show alternative for user
                        # ...
                        console.log response.list
                        console.log response.stocka
                        return
                else
                    Materialize.toast "No se ha encontrado Stock", 2000
                    return
        return
    $scope.listTemp = ->
        $http.get '', params: listTemp: true
        .success (response) ->
            if response.status
                $scope.list = response.list
                $timeout ->
                    $('.dropdown-button').dropdown()
                , 800
                return
            else
                swal "Error", "no data lista", "error"
                return
        return
    $scope.showEdit = ($event) ->
        $scope.mat.code = $event.currentTarget.parentElement.parentElement.parentElement.parentElement.children[1].innerText
        $timeout ->
            e = $.Event 'keypress', keyCode: 13
            $("[name=code]").trigger e
            return
        , 100
        $timeout ->
            quantity = parseFloat $event.currentTarget.parentElement.parentElement.parentElement.parentElement.children[6].innerText
            $scope.shwaddm = true
            $scope.mat =
                quantity: parseFloat quantity
                brand: $event.currentTarget.dataset.brand
                model: $event.currentTarget.dataset.model
                obrand: $event.currentTarget.dataset.brand
                omodel: $event.currentTarget.dataset.model
            return
        , 300
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
    # function translate
    $scope.getStock = ->

        return
    $scope.validExistGuide = ->
        data =
            valid: true
            guide: $scope.guide
        $http
            url: ''
            method: 'post'
            data: $.param data
        .success (response) ->
            if response.status
                # message guide id exists
                return
        return
    $scope.change = ->
        console.log "this object to change"
        return
    $scope.$watch 'summary', (old, nw) ->
        console.log old, nw
        # if !nw
            # if $scope.mat.hasOwnProperty 'obrand'
            #    $scope.mat.obrand = ''
            # if $scope.mat.hasOwnProperty 'omodel'
            #    $scope.mat.omodel = ''
        return
    # $scope.$watch 'mat.brand', (old, nw) ->
    #     # console.log old, nw
    #     # console.log $scope.mat, "object"
    #     if typeof(nw) isnt "undefined"
    #         console.log nw
    #     return
    return
