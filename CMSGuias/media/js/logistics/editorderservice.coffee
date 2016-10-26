do ->
    'use strict'
    app = angular.module "soApp", ['ngCookies', 'ngSanitize']

    app.config ($httpProvider) ->
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
        $httpProvider.defaults.xsrfCookieName = 'csrftoken'
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
        return

    app.factory 'soFactory', ($http, $cookies) ->
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
        $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
        ofac = new Object()
        fd = (options={}) ->
            form = new FormData()
            for k,v of options
                form.append k, v
            return form
        ofac.getData = (options = {}) ->
            $http.get "", params: options
        ofac.getDetails = (options = {}) ->
            $http.get "", params: options
        ofac.getLetter = (options={}) ->
            $http.get "", params: options
        ofac.saveOrder = (options={}) ->
            $http.post "", fd(options), transformRequest: angular.identity, headers: 'Content-Type': undefined
        ofac.editDetails = (options={}) ->
            $http.post "", fd(options), transformRequest: angular.identity, headers: 'Content-Type': undefined
        return ofac

    app.controller 'soCtrl', ($scope, $timeout, $q, soFactory) ->
        $scope.projects = []
        $scope.digv = 0
        $scope.dstotal = 0
        $scope.ddsct = 0
        $scope.dsigv = 0
        $scope.dtotal= 0
        $scope.edit = []
        $scope.dels = []

        angular.element(document).ready ->
            angular.element(".modal-trigger").leanModal()
            angular.element(".chosen-select").chosen width: '100%'
            angular.element("#desc").trumbowyg()
            angular.element('.trumbowyg-editor, .trumbowyg-box')
            .css "min-height", "200px"
            .css "margin", "0px auto"
            $scope.loadData()
            return

        $scope.loadData = ->
            prm = load: true
            soFactory.getData(prm)
            .success (response) ->
                if response.status
                    $scope.loadDetails()
                    $scope.so = response.data
                    $scope.projects = response.projects
                    $scope.suppliers = response.supplier
                    $scope.documents = response.document
                    $scope.methods = response.method
                    $scope.currencys = response.currencys
                    $scope.authorizeds = response.authorized
                    $scope.vigv = response.vigv
                    $scope.units = response.unit
                    $timeout ->
                        angular.element(".chosen-select").trigger "chosen:updated"
                    , 800
                else
                    Materialize.toast "<i class='fa fa-warning fa-2x amber-text'></i>&nbsp; No se ha cargado los datos!", 4000
                return
            return

        $scope.loadDetails = ->
            prm = details: true
            soFactory.getDetails prm
            .success (response) ->
                if response.status
                    $scope.details = response.details
                    $timeout ->
                        $scope.calc()
                        return
                    , 600
                    return
                else
                    Materialize.toast "<i class='fa fa-warning fa-2x amber-text'></i>&nbsp;No hay detalle para mostrar.", 4000
                    return
            return

        $scope.calc = ->
            getsubtotal = ->
                defer = $q.defer()
                promises = 0 
                angular.forEach $scope.details, (obj) ->
                    #  console.info obj
                    promises += (obj.fields.price * obj.fields.quantity)
                    return
                defer.resolve promises
                # $q.all([promises]).then (result) ->
                #     defer.resolve result
                #     return
                return defer.promise
            getsubtotal().then (result) ->
                $scope.dstotal = Number(result.toFixed(3))
                # apply discount
                $scope.ddsct = Number((($scope.dstotal * $scope.so.dsct)/100).toFixed(3))
                _stt = Number(($scope.dstotal - $scope.ddsct).toFixed(3))
                # apply igv
                if $scope.so.sigv is true
                    $scope.dsigv = Number((($scope.dstotal * $scope.digv)/100).toFixed(3))
                    _stt += $scope.dsigv
                # get total
                $scope.dtotal = _stt
                return
            return

        $scope.showEdit = (pk, obj) ->
            # console.log pk
            # console.info obj
            angular.element("#desc").trumbowyg 'html', obj.description
            $scope.edit.pk = pk
            $scope.edit.quantity = obj.quantity
            $scope.edit.price = Number(obj.price)
            $scope.edit.unit = obj.unit
            angular.element("#eDetails").openModal()
            return

        $scope.applyDetails = ->
            $scope.edit.description = angular.element("#desc").trumbowyg 'html'
            # prm = $scope.edit
            # prm['editd'] = true
            # soFactory.editDetails(prm)
            # .success (response) ->
            #     if response.status
            #         $scope.loadDetails()
            #         angular.element("#eDetails").closeModal()
            #         return
            #     else
            #         Materialize.toast "<i class='fa fa-times-circle fa-lg'></i>", 3000
            #         return
            if $scope.edit.hasOwnProperty "pk"
                angular.forEach $scope.details, (obj) ->
                    if obj.pk is $scope.edit.pk
                        obj.fields = $scope.edit
                        return
            else 
                # add new item
                $scope.details.push
                    pk: $scope.details.length + 1
                    model: "add"
                    fields: $scope.edit
            $scope.calc()
            $scope.eClean()
            return

        $scope.eClean = ->
            $scope.edit = []
            angular.element("#desc").trumbowyg 'html', ''
            return

        $scope.delItem = (pk) ->
            swal
                title: 'Realmente desea eliminar el item?'
                text: ''
                type: 'warning'
                showCancelButton: true
                closeOnCancel: true
                closeOnConfirm: true
                cancelButtonText: 'No!'
                confirmButtonText: 'Si!, eliminar'
                confirmButtonColor: '#dd6b55'
            , (isConfirm) ->
                if isConfirm
                    angular.forEach $scope.details, (obj, index) ->
                        if obj.pk is pk
                            $scope.dels.push obj.pk 
                            $scope.details.splice index, 1
                            $scope.$apply()
                            Materialize.toast "<i class='fa fa-fire fa-lg red-text'></i>&nbsp;Item eliminado!", 2600
                            $scope.calc()
                            return
                    return
            return

        $scope.saveOrderService = ->
            swal
                title: 'Desea guardar los datos?'
                text: ''
                type: 'warning'
                confirmButtonText: 'Si!, Guardar'
                confirmButtonColor: '#dd6b55'
                cancelButtonText: 'No'
                showCancelButton: true
                closeOnConfirm: true
                closeOnCancel: true
            , (isConfirm) ->
                if isConfirm
                    soFactory.saveOrder()
                    .success (response) ->
                        if response.status
                            Materialize.toast "<i class='fa fa-check fa-lg green-text'></i> &nbsp;Se actualizo correctamente!", 2500
                            $timeout ->
                                location.href = '/logistics/services/orders/'
                                return
                            , 2500
                            return
                        else
                            Materialize.toast "NO se han guardado los datos", 4000
                            return
                    return
            return

        $scope.$watch 'so.dsct', (nw, old) ->
            if nw isnt old
                $scope.calc()
            return

        $scope.$watch 'so.sigv', (nw, old) ->
            if nw isnt undefined
                if nw is true
                    $scope.digv = $scope.vigv
                else
                    $scope.digv = 0
                    $scope.dsigv = 0
                $scope.calc()
            return
        
        $scope.$watch 'so.currency', (nw, old) ->
            if nw isnt undefined
                $scope.lcur = angular.element("#currency option:selected").text()
        
        $scope.$watch 'dtotal', (nw, old) ->
            if nw isnt old
                $scope.dtotal = parseFloat($scope.dtotal).toFixed(2)
                prm =
                    'lnumber': true
                    'number': $scope.dtotal
                soFactory.getLetter(prm)
                .success (response) ->
                    if response.status
                        $scope.letter = response.letter
                        $scope.lcur = angular.element("#currency option:selected").text()
                        return
                return
        return
    return