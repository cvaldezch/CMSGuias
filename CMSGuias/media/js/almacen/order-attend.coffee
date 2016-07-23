app = angular.module 'attendApp', ['ngCookies', 'angular.filter']

app.config ($httpProvider) ->
	$httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
	$httpProvider.defaults.xsrfCookieName = 'csrftoken'
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
	return

app.directive 'cinmam', ($parse) ->
	link: (scope, element, attrs, ngModel) ->
		element.bind 'change, blur', (event) ->
			# console.log element
			val = parseFloat element.context.value
			max = parseFloat attrs.max
			min = parseFloat attrs.min
			if val is ""
				element.context.value = max
			if not isNaN(val)
				element.context.value = max
			if val > max
				element.context.value = max
				# console.log element.change()
			if val < min
				element.context.value = min
				return
			# angular.element(element).change()
		return

factories = ($http, $cookies) ->
	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
	$http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
	obj = new Object
	obj.getDetailsOrder = (options = {}) ->
		$http.get "", params: options
	obj.getDetNiples = (options = {}) ->
		$http.get "", params: options
	obj

app.factory 'attendFactory', factories

controllers = ($scope, $timeout, attendFactory) ->

	$scope.dorders = []

	angular.element(document).ready ->
		console.log "angular load success!"
		if $scope.init is true
			$scope.sDetailsOrders()
		return

	$scope.sDetailsOrders = ->
		attendFactory.getDetailsOrder 'details': true
		.success (response) ->
			if response.status
				$timeout ->
					$scope.dorders = response.details
					$scope.getNiple()
					console.log "is execute!!"
				, 80
				return
			else
				console.log "error in data #{response.raise}"
				return
		return
	
	$scope.getDetailsOrder = ->
		attendFactory.getDetailsOrder 'details': true
		.success (response) ->
			if response.status
				$scope.sdetails = response.details
				angular.element("#midetails").openModal()
				return
			else
				Materialize.toast 'No hay datos para mostrar', 3600, 'rounded'
				return
		return

	$scope.getNiple = ->
		attendFactory.getDetNiples 'detailsnip': true
		.success (response) ->
			if response.status
				tmp = new Array()
				angular.forEach response.nip, (value) ->
					# console.log value.fields.materiales
					tmp.push
						'materials': value.fields.materiales.pk
						'name': "#{value.fields.materiales.fields.matnom} #{value.fields.materiales.fields.matmed} #{value.fields.materiales.fields.unidad}"
						'description': "Niple #{response.types[value.fields.tipo]} "
						'brand': value.fields.brand.pk
						'bname': value.fields.brand.fields.brand
						'model': value.fields.model.pk
						'mname': value.fields.model.fields.model
						'tipo': value.fields.tipo
						'meter': value.fields.metrado
						'quantity': value.fields.cantidad
						'send': value.fields.cantshop
						'guide': value.fields.cantguide
					return
				console.table tmp
				$scope.dnip = tmp
				return
			else
				Materialize.toast "Error #{response.raise}", 3000, 'rounded'
				return
		return
	return

app.controller 'attendCtrl', controllers
	