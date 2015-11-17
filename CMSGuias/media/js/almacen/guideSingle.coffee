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
            min: '0'
            closeOnSelect: true
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
                            console.log response.exact[0].fields
                            if response.exact[0].fields.stock >= data.quantity
                                $scope.exact = []
                                $scope.alternative = []
                                $scope.stkg = []
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
                                $scope.exact = response.exact
                                $scope.alternative = response.list
                                $scope.stkg = response.stocka
                                return false
                    else
                        $scope.alternative = response.list
                        $scope.stkg = response.stocka
                        $scope.exact = response.exact
                        swal "Alerta!", "El Material no cuenta con Stock", "warning"
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
    $scope.validExistGuide = ->
        data =
            valid: true
            code: $scope.guide
        $http
            url: ''
            method: 'post'
            data: $.param data
        .success (response) ->
            if not response.status
                swal "Información!", "El Nro de guia ingresado ya existe!", "info"
                return
        return
    $scope.delallDetails = ->
        swal
            title: "Eliminar Detalle?"
            text: "desea eliminar todo la lista de detalle?"
            type: "warning"
            showCancelButton: true
            confirmButtonText: "Si!, eliminar"
            confirmButtonColor: "#dd6b55"
            closeOnCancel: true
        , (isConfirm) ->
            if isConfirm
                data =
                    delAllDetails: true
                $http
                    url: ''
                    method: 'post'
                    data: $.param data
                .success (response) ->
                    if response.status
                        $scope.listTemp()
                        return
                return
        return
    $scope.refresh = ->
        $scope.customersList()
        $scope.carrierList()
        $scope.listTemp()
        $scope.brandmodel()
        return
    $scope.recycleData = ->
        $scope.customersList()
        $scope.carrierList()
        $scope.listTemp()
        $scope.brandmodel()
        $scope.guide.guide = ''
        $scope.guide.transfer = ''
        $scope.guide.dotarrival = ''
        $scope.guide.driver = ''
        $scope.guide.transport = ''
        $scope.guide.motive = ''
        $scope.guide.observation = ''
        $scope.guide.note = ''
    $scope.saveGuide = ->
        data =
            save: true
            guide: $scope.guide.guide
            tranfer: $scope.guide.transfer
            cliente: $scope.guide.customer
            dotoutput: $scope.guide.dotout
            puntollegada: $scope.guide.dotarrival
            traslado: $scope.guide.transfer
            traruc: $scope.guide.carrier
            condni: $scope.guide.driver
            nropla: $scope.guide.transport
            motive: $scope.guide.motive
            observation: $scope.guide.observation
            note: $scope.guide.note
        for k, v of data
            console.log v, typeof(v)
            if typeof(v) is "undefined"
                console.log k, v
                switch k
                    when 'guide'
                        swal 'Alerta!', 'Nro guia invalida.', 'warning'
                        data.save = false
                        break
                    when 'transfer'
                        swal 'Alerta!', 'Fecha de traslado invalido.', 'warning'
                        data.save = false
                        break
                    when 'cliente'
                        swal 'Alerta!', 'Cliente invalido.', 'warning'
                        data.save = false
                        break
                    when 'dotoutput'
                        swal 'Alerta!', 'Punto de salida invalida.', 'warning'
                        data.save = false
                        break
                    when 'traduc'
                        swal 'Alerta!', 'Transportita invalido.', 'warning'
                        data.save = false
                        break
                    when 'condni'
                        swal 'Alerta!', 'Conductor invalido.', 'warning'
                        data.save = false
                        break
                    when 'nropla'
                        swal 'Alerta!', 'Transporte invalido.','warning'
                        data.save = false
                        break
                    # when 'observation' then break
                    # when 'note' then break
        console.log data
        return
    $scope.$watch 'summary', (old, nw) ->
        console.log old, nw
        return
    # $scope.$watch 'mat.brand', (old, nw) ->
    #     # console.log old, nw
    #     # console.log $scope.mat, "object"
    #     if typeof(nw) isnt "undefined"
    #         console.log nw
    #     return
    return
