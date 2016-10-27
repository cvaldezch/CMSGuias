do ->
    app = angular.module 'cpApp', []
    cpCtrl = ($rootScope, $scope, $log) ->

        $scope.call = false
        $scope.mstyle = ''

        angular.element(document).ready ->
            angular.element('.collapsible').collapsible()
            angular.element('.scrollspy').scrollSpy()
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
        return

    'use strict'
    app.controller 'cpCtrl', cpCtrl
    return
