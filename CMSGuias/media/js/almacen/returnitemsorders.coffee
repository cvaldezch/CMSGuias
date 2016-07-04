app = angular.module 'rioApp', ['ngCookies']
app.config ($httpProvider) ->
	$httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
	$httpProvider.defaults.xsrfCookieName = 'csrftoken'
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
	return

app.directive 'minandmax', ($parse) ->
	restrict: 'A'
	require: 'ngModel'
	link: (scope, element, attrs, ctrl) ->
		element.bind 'change', (event) ->
			if parseFloat ctrl.$viewValue < parseFloat attrs.min or parseFloat ctrl.$viewValue > parseFloat attrs.max
				scope.valid = false
				ctrl.$setViewValue attrs.max
				ctrl.$render()
				scope.$apply()
				Materialize.toast 'El valor no es valido!', 4000
			else
				scope.valid = true
			return
		return

app.factory 'rioF', ($http, $cookies) ->
	obj = new Object
	convertForm = (options = {}) ->
		form = new FormData
		angular.forEach options, (val, key) ->
			form.append key, val
			return
		return form
	obj.getDetails = (options = {}) ->
		$http.get "", params: options
	obj.returnList = (options = {}) ->
		$http.post "", convertForm(options), transformRequest: angular.identity, headers: 'Content-Type': undefined
	return obj

app.controller 'rioC', ($scope, rioF) ->
	$scope.mat = []
	$scope.quantity = []
	$scope.valid = true
	angular.element(document).ready ->
		$scope.getDetails()
		return

	$scope.checkall = ->
		angular.forEach $scope.mat, (value, key) ->
			$scope.mat[key] = $scope.selAll.chk
			return
		return

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
		tmp = new Array
		$scope.datareturn = tmp
		angular.forEach $scope.mat, (value, key) ->
			if value is true
				angular.forEach $scope.details, (obj, ik) ->
					if obj.pk is key
						console.log obj.pk
						console.info key
						tmp.push
							'id': obj.pk
							'materials': obj.fields.materiales.pk
							'name': "#{obj.fields.materiales.fields.matnom} #{obj.fields.materiales.fields.matmed}"
							'unit': obj.fields.materiales.fields.unidad
							'brand': obj.fields.brand.fields.brand
							'brand_id': obj.fields.brand.pk
							'model': obj.fields.model.fields.model
							'model_id': obj.fields.model.pk
							'quantity': $scope.quantity[obj.pk]
						return
			return
		$scope.datareturn = tmp
		angular.element("#mview").openModal()
		return

	$scope.sendReturnList = ->
		swal
			title: "Esta seguro?"
			text: "Regresar los materiales a la lista de proyecto."
			type: "warning"
			showCancelButton: true
			confirmButtonColor: '#dd6b55'
			confirmButtonText: 'Si!, Retornar'
			cancelButtonText: 'No!'
			closeOnConfirm: true
		, (isConfirm) ->
			if isConfirm
				prm =
					'details': JSON.stringify $scope.datareturn
					'saveReturn': true
				rioF.returnList(prm)
				.success (response) ->
					if response.status
						Materialize.toast "Se ha devuelto los materiales seleccionados.", 4000
						return
					else
						swal "Error!", "#{response.raise}", "error"
						return
				return
		return
	return

