app = angular.module 'guideApp', ['ngCookies']
		.config ($httpProvider) ->
			$httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
			$httpProvider.defaults.xsrfCookieName = 'csrftoken'
			$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
			return

app.factory 'fGuide', ($http, $cookies, $q) ->
	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
	$http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
	obj = new Object
	obj.getDetails = (options) ->
		$http.get '', params: options	
	obj.getCarrier = (options = {}) ->
		$http.get '/json/get/carries/', params: options
	obj.getTransport = (options) ->
		$http.get "/json/get/list/transport/#{options}/"
	obj.getDriver = (options) ->
		$http.get "/json/get/list/conductor/#{options}/", params: options
	obj.saveGuide = (options = {}) ->
		form = new FormData
		form.append 'puntollegada', options.puntollegada
		form.append 'traslado', options.traslado
		form.append 'traruc_id', options.traruc_id
		form.append 'condni_id', options.condni_id
		form.append	'nropla_id', options.nropla_id
		form.append 'comment', options.comment
		form.append 'nota', options.nota
		form.append 'saveGuide', true
		$http #.post '', form, transformRequest: angular.identity, headers: 'Content-Type': `undefined`
			url: ""
			method: "POST"
			data: form
			transformRequest: angular.identity
			headers: 'Content-Type': `undefined`
	obj

app.controller 'cGuide', ($scope, $timeout, $q, fGuide) ->
	$scope.carrier = ''
	$scope.guide = []
	angular.element(document).ready ->
		angular.element(".datepicker").pickadate
			container: "body"
			closeOnSelect: true
			min: new Date()
			selectMonths: true
			selectYears: 15
			format: "yyyy-mm-dd"
		fGuide.getDetails({'details':true}).success (response) ->
			if response.status
				$scope.details = response.list
				return
		fGuide.getCarrier().success	(response) ->
			if response.status
				$scope.carriers = response.carrier
				return
		fGuide.getTransport($scope.carrier).success (response) ->
			if response.status
				$scope.transports = response.list	
				return
		fGuide.getDriver($scope.carrier).success (response) ->
			if response.status
				$scope.drivers = response.list	
				return
		return

	$scope.getdriversandtransport = ($event) ->
		fGuide.getDriver($scope.guide['traruc_id']).
		success (response) ->
			if response.status
				$scope.drivers = response.list
				return
		fGuide.getTransport($scope.guide['traruc_id']).
		success (response) ->
			if response.status
				$scope.transports = response.list
				return
		return

	$scope.saveGuide = ->
		fGuide.saveGuide($scope.guide).success (response) ->
			if response.status
				$timeout ->
					location.href = '/almacen/list/guide/referral/'
				, 2600
				swal
					title: "Felicidades!"
					text: "Se ha guardado en los cambios."
					type: "success"
					timer: 2600
				return
			else
				swal
					title: 'Error!'
					text: 'No se ha guardo los datos.'
					type: 'error'
				return
		return
	return
