app = angular.module 'rioApp', ['ngCookies']
app.config ($httpProvider) ->
	$httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
	$httpProvider.defaults.xsrfCookieName = 'csrftoken'
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
	return

app.factory 'rioF', ($http, $cookies) ->
	obj = new Object
	obj.getDetails = (options = {}) ->
		$http.get "", params: options
	
	return obj

app.controller 'rioC', ($scope, rioF) ->
	$scope.mat = []
	angular.element(document).ready ->
		$scope.getDetails()
		return

	$scope.checkall = (mat) ->
		if $scope.all && !$scope.nothing
			$scope.mat[mat] = true
			return true
		else
			$scope.mat[mat] = false
			return false

	$scope.getDetails = ->
		prm =
			'getorder': true
		rioF.getDetails(prm)
		.success (response) ->
			if response.status
				$scope.details = response.details
				return
			else
				swal "Error", "#{response.raise}", "error"
				return
		return

	$scope.returnItems = ->
		console.log $scope.mat
		return
	
	return

