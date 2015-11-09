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
