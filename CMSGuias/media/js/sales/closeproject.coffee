do ->
    'use strict'
    app = angular.module 'cpApp', ['ngCookies']

    app.config ($httpProvider) ->
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
        $httpProvider.defaults.xsrfCookieName = 'csrftoken'
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
        return

    cpFactories = ($http, $cookies) ->
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
        $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
        fd = (options={}) ->
            form = new FormData()
            for k, v of options
                form.append k, v
            return form
        obj = new Object()
        obj.getComplete = (options={}) ->
            $http.get "", params: options
        obj.formData = (options={}) ->
            $http.post "", fd(options), transformRequest: angular.identity, headers: 'Content-Type': undefined
        obj.formCross = (uri="", options={}) ->
            $http.jsonp uri, params: options
        return obj
    app.factory 'cpFactory', cpFactories

    app.controller 'cpCtrl', ($rootScope, $scope, $log, cpFactory) ->

        $scope.call = false
        $scope.mstyle = ''
        $scope.ctrl = 
            'storage': false
            'operations': false
            'quality': false
            'accounting': false
            'sales': false

        angular.element(document).ready ->
            $scope.validArea()
            angular.element('.collapsible').collapsible()
            angular.element('.scrollspy').scrollSpy()
            $scope.sComplete()
            return

        $scope.sComplete = ->
            cpFactory.getComplete 'gcomplete': true
            .success (response) ->
                if response.status
                    $scope.sh = response.complete
                    return
                else
                    Materialize.toast "#{response.raise}", 2000
                    $scope.sh = response.complete
                    return
            return

        $scope.validArea = ->
            switch $scope.uarea
                when 'administrator' or 'ventas' or 'logistica'
                    for x of $scope.ctrl
                        $scope.ctrl[x] = true
                when 'operaciones'    
                    $scope.ctrl['operations'] = true
                when 'calidad'
                    $scope.ctrl['quality'] = true
                when 'almacen'
                    $scope.ctrl['storage'] = true
            return

        $scope.storageClosed = ->
            swal
                title: "Realmanete desea Cerrar el Almacén?"
                text: ''
                type: 'warning'
                showCancelButton: true
                confirmButtonText: 'Si!, cerrar'
                confirmButtonColor: "#e82a37"
                closeOnCancel: true
                closeOnConfirm: true
            , (isConfirm) ->
                if isConfirm
                    $log.info "yes closed"
                    cpFactory.formData 'storage': true
                    .success (response) ->
                        if response.status
                            $scope.sComplete()
                            Materialize.toast "<i class='fa fa-check fa-lg green-text'></i>&nbsp;Almacén Cerrado", 4000
                            return
                        else
                            Materialize.toast "<i class='fa fa-times fa-lg red-text'></i>&nbsp;#{repsonse.raise}", 4000
                            return
                    return
                else
                    $scope.$apply ->
                        $scope.closedstorage = false
                        return
                    return
            return
        $scope.letterClosed = ->
            if angular.element("#letterup")[0].files.length is 0
                Materialize.toast "<i class='fa fa-warning amber-text fa-lg'></i> Debe seleccionar por lo menos un archivo.", 4000
                return false
            swal
                title: "Realmanete desea cargar la Carta de Entrega?"
                text: ''
                type: 'warning'
                showCancelButton: true
                confirmButtonText: 'Si!, subir'
                confirmButtonColor: "#f82432"
                closeOnCancel: true
                closeOnConfirm: true
            , (isConfirm) ->
                if isConfirm
                    prm =
                        'operations': true
                        'letter': angular.element("#letterup")[0].files[0]
                    cpFactory.formData prm
                    .success (response) ->
                        if response.status
                            $scope.sComplete()
                            Materialize.toast "<i class='fa fa-check fa-lg green-text'></i>&nbsp;Archivo subido.", 4000
                            return
                        else
                            Materialize.toast "<i class='fa fa-times fa-lg red-text'></i>&nbsp;#{repsonse.raise}", 4000
                            return
                    return
            return
        
        $scope.qualityClosed = ->
            if angular.element("#qualityfile")[0].files.length is 0
                Materialize.toast "<i class='fa fa-warning amber-text fa-lg'></i> Debe seleccionar por lo menos un archivo.", 4000
                return false
            swal
                title: "Realmanete desea cargar los documentos de calidad?"
                text: ''
                type: 'warning'
                showCancelButton: true
                confirmButtonText: 'Si!, subir'
                confirmButtonColor: "#f82432"
                closeOnCancel: true
                closeOnConfirm: true
            , (isConfirm) ->
                if isConfirm
                    prm =
                        'quality': true
                        'documents': angular.element("#qualityfile")[0].files[0]
                    cpFactory.formData prm
                    .success (response) ->
                        if response.status
                            $scope.sComplete()
                            Materialize.toast "<i class='fa fa-check fa-lg green-text'></i>&nbsp;Archivo subido.", 4000
                            return
                        else
                            Materialize.toast "<i class='fa fa-times fa-lg red-text'></i>&nbsp;#{repsonse.raise}", 4000
                            return
                    return
            return
        $scope.accountingClosed = ->
            prm =
                accounting: true
                tinvoice: $scope.acctinvoice
                tiva: $scope.acctiva
                otherin: $scope.acctotherin
                otherout: $scope.acctotherout
                retention: $scope.acctretention
            if angular.element("#accountingfile")[0].files.length > 0
                prm['fileaccounting']= angular.element("#accountingfile")[0].files[0]
            swal
                title: "Realmanete desea cargar los documentos de calidad?"
                text: ''
                type: 'warning'
                showCancelButton: true
                confirmButtonText: 'Si!, subir'
                confirmButtonColor: "#f82432"
                closeOnCancel: true
                closeOnConfirm: true
            , (isConfirm) ->
                if isConfirm
                    cpFactory.formData prm
                    .success (response) ->
                        if response.status
                            $scope.sComplete()
                            Materialize.toast "<i class='fa fa-check fa-lg green-text'></i>&nbsp;Archivo subido.", 4000
                            return
                        else
                            Materialize.toast "<i class='fa fa-times fa-lg red-text'></i>&nbsp;#{repsonse.raise}", 4000
                            return
                    return
            return
        $scope.getPin = ->
            Materialize.toast '<i class="fa fa-cog fa-spin fa-2x"></i>&nbsp;&nbsp;Generando PIN, espere!', 'some', 'lime lighten-1 grey-text text-darken-3 toast-static'
            prm =
                genpin: true
                sales: true
            cpFactory.formData prm
            .success (response) ->
                if response.status
                    setTimeout (->
                        angular.element(".toast-static").remove()
                        Materialize.toast '<i class="fa fa-envelope-o fa-lg"></i>&nbsp Estamos enviando el PIN a su correo.', 'some', 'toast-static'
                        prm =
                            forsb: response.mail
                            issue: "PIN DE CIERRE PROYECTO #{response.pro}"
                            body: """<p><strong><strong>#{response.company} |</strong></strong> Operaciones Frecuentes</p><p>Generar PIN para cierre de proyecto | <strong>#{new Date().toString()}</strong></p><p><strong>PIN:&nbsp;#{response.pin}</strong></p><p><strong>Proyecto:&nbsp;#{response.pro} #{response.name}</strong></p>"""
                            callback: 'JSON_CALLBACK'
                        cpFactory.formCross "http://190.41.246.91:3000/mailer/", prm
                        .success (rescross) ->
                            if rescross.status
                                angular.element(".toast-static").remove()
                                Materialize.toast '<i class="fa fa-paper-plane-o fa-lg"></i>&nbsp; Se a envio correntamente el correo', 4000
                                return
                            else
                                Materialize.toast 'Se ha producido algun error #{rescross}', 7000
                                return
                        return
                    ), 8000
                else
                    Materialize.toast "<i class='fa fa-times fa-lg red-text'></i> #{response.raise}"
                return
            return
        ## cpCtrl
        $scope.$watch 'call', (nw, old) ->
            if nw isnt undefined
                if nw is false
                    $scope.mstyle = 'display': 'hide'
                    return
                else
                    $scope.mstyle = 'display': 'block'
                    return
        $scope.$watch 'closedstorage', (nw, old) ->
            if nw isnt undefined
                if nw is true
                    $scope.storageClosed()
                    return
        return
    return
