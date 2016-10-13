app = angular.module 'appReturnWith', ['ngCookies']

app.config ($httpProvider) ->
	$httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
	$httpProvider.defaults.xsrfCookieName = 'csrftoken'
	$httpProvider.defaults.xsrfHeadername = 'X-CSRFToken'
	return

app.directive 'onlyNumberHyphen', ->
	restrict: 'AE'
	require: '?ngModel'
	link: (scope, element, attrs, ngModel) ->
		element.bind 'keyup', (event) ->
			key = event.which or event.keyCode
			vl = element.val()
			if RegExp(/(?=[0-9]{3}[-]{1}[0-9]{8}).{12}$/).test(vl)
				scope.$apply ->
					scope.valid = true
					return
				if key is 13
					scope.$apply ->
						scope.guide = scope.tmpg
						return
				return
			else
				scope.$apply ->
					scope.valid = false
					return
				return

		element.bind 'keypress', (event) ->
			keycode = event.which or event.keyCode
			console.log keycode
			if (keycode < 48 or keycode > 57) and keycode != 8 and keycode != 45
				console.log "key block", keycode
				event.preventDefault()
				return false
			return
		return

app.directive 'vminmax', valMinandMax

app.factory 'returnFactory', ($http, $cookies) ->
	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
	$http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
	obj = new Object
	formd = (options = {}) ->
		form = new FormData()
		for k, v in options
			form.append k, v
		return form
	obj.getDetailsGuide = (options = {}) ->
		$http.get "", params: options
	
	return obj


app.controller 'ctrlReturnWith', ($scope, $timeout, $q, returnFactory) ->

	$scope.valid = false
	$scope.guide = ''
	$scope.sald = false
	$scope.returns = []
	$scope.chkdet = false

	angular.element(document).ready ->
		console.log "Document ready"
		return

	$scope.returnInventory = ->
		available = ->
			defer = $q.defer()
			promises = new Array
			for x in $scope.returns
				if x.check is true and x.qreturn > 0
					promises.push x
					
			$q.all(promises).then (result) ->
				defer.resolve result
				return
			return defer.promise
		available().then (result) ->
			if result.length > 0
				swal
					title: 'Realmente desea retornar el/los accesorio(s) seleccionado(s)?.'
					text: ''
					type: 'warning'
					confirmButtonColor: '#3085d6'
					confirmButtonText: 'Si! Retornar'
					cancelButtonText: 'No!'
					showCancelButton: true
					closeOnConfirm: true
					closeOnCancel: true
				, (isConfirm) ->
					if isConfirm
						console.log "return"
						return
			else
				Materialize.toast "<i class='fa fa-warning fa-2x amber-text'></i>&nbsp;<spam>Debe de selecionar al menos un item y su cantidad tiene que ser mayor a 0.</spam>", 9000, 'rounded'
			return
		return
	
	$scope.test = ->
		console.log $scope.valid
		console.log $scope.tmpg
		console.log $scope.guide
		return

	$scope.$watch 'guide', (nw, old) ->
		if nw isnt old
			$scope.sald = true
			# console.log nw
			prm =
				getdetails: true
				guide: nw
			returnFactory.getDetailsGuide prm
			.success (response) ->
				if response.status
					$scope.dguide = response.details
					$scope.sguide = response.guide
					$scope.returns = []
					$scope.sald = false
					if response.details.length is 0
						Materialize.toast "<i class=\"fa fa-meh-o fa-2x red-text\"></i>&nbsp;Oops! Noy hay un detalle que coincida con el Nro de Guia ingresado \"#{$scope.tmpg}\" ", 12000, "rounded"
					return
				else
					Materialize.toast "<i class='fa fa-times red-text fa-2x'></i> No se cargo el detalle del número de guia ", 4000
					return
			return

	$scope.$watch 'chkdet', (nw, old) ->
		for x in $scope.returns
			x.check = nw
	return
