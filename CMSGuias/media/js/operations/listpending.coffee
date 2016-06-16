app = angular.module 'cpApp', ['ngCookies']

app.config ($httpProvider) ->
	$httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
	$httpProvider.defaults.xsrfCookieName = 'csrftoken'
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
	return

app.factory 'cpf', ($http, $cookies) ->
	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
	$http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
	obj = new Object
	obj.getSGroup = (options = {}) ->
		$http.get "", params: options
	obj.getDSector = (options = {}) ->
		$http.get "", params: options
	obj.getData = (options = {}) ->
		$http.get "", params: options
	obj.getDataG = (options = {}) ->
		$http.get "", params: options
	
	obj.getDetails = (options = {}) ->
		$http.get "", params: options
	
	obj

app.controller 'cpC', ($scope, $timeout, cpf) ->
	$scope.selected = {}
	$scope.dg = false
	angular.element(document).ready ->
		# ...
		return
	$scope.getSGroup = ->
		prm =
			'gsgroup': true
		cpf.getSGroup(prm)
		.success (response) ->
			if response.status
				$scope.ds = []
				$scope.sg = response.sg
				$scope.bsearch = 'sgroup'
				angular.element("#mselection").openModal()
				return
			else
				swal "Error", "#{response.raise}", "warning"
				return
		return

	$scope.getDSector = ->
		prm =
			'gdsector': true
		cpf.getDSector(prm)
		.success (response) ->
			if response.status
				$scope.sg = []
				$scope.ds = response.ds
				$scope.bsearch = 'dsector'
				angular.element("#mselection").openModal()
				return
			else
				swal "Error", "#{response.raise}", "warning"
				return
		return

	$scope.getData = ->
		$scope.gdata = []
		prm = new Object
		obj = angular.extend {}, $scope.selected
		console.log obj
		angular.forEach obj, (value, key) ->
			if value is true
				if not prm.hasOwnProperty('keys')
					prm['keys'] = key
				else
					prm['keys'] += ",#{key}"
			return
		prm['searchby'] = $scope.bsearch
		prm['getPendingData'] = true
		cpf.getData(prm)
		.success (response) ->
			if response.status
				$scope.gdata = response.dataset
				angular.element("#mselection").closeModal()
				$scope.dg = false
				return
			else
				swal "Alerta!", "#{response.raise}", "warning"
				return

	$scope.getDataG = ->
		prm =
			'getGlobal': true
		cpf.getDataG(prm)
		.success (response) ->
			if response.status
				$scope.gdata = response.dataset
				$scope.dg = true
				return
			else
				swal "Alerta!", "#{response.raise}", "warning"
				return

	$scope.getDetails = (materials) ->
		prm = new Object
		if $scope.dg is false
			obj = $scope.selected
			angular.forEach obj, (value, key) ->
				if value is true
					if not prm.hasOwnProperty('keys')
						prm['keys'] = key
					else
						prm['keys'] += ",#{key}"
				return
			prm['searchby'] = $scope.bsearch
		prm['materials'] = materials
		prm['getDetails'] = true
		cpf.getDetails(prm)
		.success (response) ->
			console.log response
			if response.status
				$scope.dataDetails = response.data
				angular.element("#mdetails").openModal()
				return
			else
				swal "Alerta!", "#{response.raise}", "warning"
				return
		return

	$scope.test = ->
		console.log $scope.chsec
		return
	
	return
