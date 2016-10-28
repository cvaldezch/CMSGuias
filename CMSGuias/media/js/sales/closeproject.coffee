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
                            Materialize.toast "<i class='fa fa-check fa-lg green-text'></i>&nbps;Almacén Cerrado", 4000
                            return
                        else
                            Materialize.toast "<i class='fa fa-times fa-lg red-text'></i>&nbps;#{repsonse.raise}", 4000
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
                    $log.info "yes closed"
                    prm =
                        'operations': true
                        'letter': angular.element("#letterup")[0].files[0]
                    cpFactory.formData 
                    .success (response) ->
                        if response.status
                            $scope.sComplete()
                            Materialize.toast "<i class='fa fa-check fa-lg green-text'></i>&nbps;Archivo subido.", 4000
                            return
                        else
                            Materialize.toast "<i class='fa fa-times fa-lg red-text'></i>&nbps;#{repsonse.raise}", 4000
                            return
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
