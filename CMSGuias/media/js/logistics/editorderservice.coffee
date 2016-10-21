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
        ofac.getData = (options = {}) ->
            $http.get "", params: options
        ofac.getDetails = (options = {}) ->
            $http.get "", params: options
        ofac.getLetter = (options={}) ->
            $http.get "", params: options
        return ofac

    app.controller 'soCtrl', ($scope, $timeout, soFactory) ->
        $scope.projects = []
        $scope.digv = 0
        $scope.dstotal = 0
        $scope.dtotal = 0

        angular.element(document).ready ->
            angular.element(".chosen-select").chosen width: '100%'
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
                    $scope.calc()
                    return
                else
                    Materialize.toast "<i class='fa fa-warning fa-2x amber-text'></i>&nbsp;No hay detalle para mostrar.", 4000
                    return
            return

        $scope.calc = ->
            angular.forEach $scope.details, (obj) ->
                #  console.info obj
                $scope.dtotal += (obj.fields.price * obj.fields.quantity)
                return
            return

        $scope.$watch 'so.sigv', (nw, old) ->
            if nw is true
                $scope.digv = $scope.vigv
            else
                $scope.digv = 0
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