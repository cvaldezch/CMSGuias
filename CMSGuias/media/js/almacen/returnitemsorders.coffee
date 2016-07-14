app = angular.module 'rioApp', ['ngCookies']
app.config ($httpProvider) ->
	$httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
	$httpProvider.defaults.xsrfCookieName = 'csrftoken'
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
	return

app.directive 'minandmax', ($parse) ->
	restrict: 'A'
	require: 'ngModel'
	scope: '@'
	link: (scope, element, attrs, ctrl) ->
		element.bind 'change', (event) ->
			# console.log ctrl
			if parseFloat(attrs.$$element[0].value) < parseFloat(attrs.min) or parseFloat(attrs.$$element[0].value) > parseFloat(attrs.max)
				# console.log "inside if"
				Materialize.toast 'El valor no es valido!', 4000
				scope.valid = false
				# element.val("value = " + attrs.max)
				ctrl.$setViewValue parseFloat(attrs.max)
				#scope.model[attrs.ngModel] = parseFloat attrs.max;
				# scope.$apply(->
				# 	ctrl.setViewValue = attrs.max
				# 	return
				# )
				ctrl.$render()
				scope.$apply()
				console.log scope
				# console.log ctrl
			else
				scope.valid = true
			return
		return

app.directive 'status', ($parse) ->
	#restrict: 'A'
	require: 'ngModel'
	#scope: '@'
	link: (scope, element, attrs, ngModel) ->
		# attrs.$observe 'ngModel', (value) -> # Got ng-model bind path here
		# 	scope.$watch value, (newValue) -> # Watch given path for changes
		# 		if newValue is true
		# 			console.log angular.element(document.querySelector("[name='#{attrs.id}']"))
		# 			angular.element(document.querySelector("[name='#{attrs.id}']")).context.value = attrs.max
		# 		else
		# 			angular.element(document.querySelector("[name='#{attrs.id}']")).context.value = 0
		# 		console.log(newValue)
		# 		return
		# 	return
		scope.$watch ->
			# console.log ngModel
			return ngModel.$modelValue
		, (newValue) ->
			el = document.getElementsByName "#{attrs.id}"
			if newValue is true
				angular.forEach el, (val) ->
					# console.log  val
					val.value = val.attributes.max.value
				console.log "change data"
			else
				angular.forEach el, (val) ->
					val.value = 0
					return
			console.log(newValue)
		return
		# scope.$watch attrs.ngModel, (nw, old) ->
		# 	console.log old
		# 	return
		# return

app.directive 'tmandm', ($parse) ->
	link: (scope, element, attrs, ngModel) ->
		element.bind 'change, click', (event) ->
			console.log element
			val = parseFloat element.context.value
			max = parseFloat attrs.max
			min = parseFloat attrs.min
			if val > max
				element.context.value = max
				return
				# console.log element.change()
			if val < min
				element.context.value = min
				return
			# angular.element(element).change()
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
	obj.getNiples = (options = {}) ->
		$http.get '', params: options

	return obj

app.controller 'rioC', ($scope, rioF) ->
	$scope.mat = []
	$scope.quantity = []
	$scope.valid = true
	$scope.showNipple = false
	$scope.vnip = false
	$scope.np = []
	$scope.dnp = []
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
						# console.log obj.pk
						# console.info key
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
		if not $scope.showNipple and not $scope.vnip
			# show nipples
			$scope.getNipples()
			return false
		else
			swal
				title: "Esta seguro?"
				text: "Regresar los materiales a la lista de proyecto."
				type: "input"
				showCancelButton: true
				cancelButtonText: 'No!'
				confirmButtonColor: '#dd6b55'
				confirmButtonText: 'Si!, Retornar'
				showLoaderOnConfirm: true
				closeOnConfirm: false
				animation: "slide-from-top"
				inputPlaceholder: "Observación"
			, (inputValue) ->
				# console.log typeof inputValue
				# console.info inputValue
				if inputValue is false
					# console.warn "value is false"
					return false
				if inputValue is ""
					# console.warn "value is empty"
					swal.showInputError "Nesecitas ingresar una Observación."
					return false
				if inputValue isnt ""
					prm =
						'details': JSON.stringify $scope.datareturn
						'saveReturn': true
						'observation': inputValue
						'nip': new Array()
					angular.forEach $scope.datareturn, (value, keys) ->
						# console.warn value
						el = document.getElementsByName(value.materials)
						# console.error el.length
						if el.length > 0
							tmp = new Array
							angular.forEach el, (val) ->
								# console.info val
								console.log prm['nip']["#{value.materials}"]
								tmp.push
									'id': val.attributes.id.value
									'materials': value.materials
									'quantity': val.value
									'meter': val.attributes.metrado.value
									'type': val.attributes.nip.value
									'import': (parseFloat(val.value) * parseFloat(val.attributes.metrado.value))
								return
							prm['nip'].push({"#{value.materials}": tmp})
							return
					prm['nip'] = JSON.stringify prm['nip']
					rioF.returnList(prm)
					.success (response) ->
						if response.status
							Materialize.toast "Se ha devuelto los materiales seleccionados.", 2800
							setTimeout ->
								location.reload()
							, 2800
							return
						else
							swal "Error!", "#{response.raise}", "error"
							return
					return
				else
					swal.showInputError "Nesecitas ingresar una Observación."
					$scope.sendReturnList()
					return false
		return
	
	$scope.getNipples = ->
		# validate order content nipple
		tmp = new Array
		angular.forEach $scope.mat, (value, key) ->
			if value is true
				angular.forEach $scope.details, (obj, ik) ->
					if obj.pk is key
						tmp.push
							'materials': obj.fields.materiales.pk
							'brand': obj.fields.brand.pk
							'model': obj.fields.model.pk
						return
				return
		prm =
			check: JSON.stringify tmp
			getNipples: true
		rioF.getNiples prm
		.success (response) ->
			$scope.vnip = true
			if response.status is true and response.valid is true
				$scope.gnp = response.gnp
				$scope.showNipple = true
				angular.element("#mnp").openModal()
				return
			else
				$scope.vnip = true
				$scope.showNipple = true
				$scope.sendReturnList()
				Materialize.toast "El pedido no tiene niples registrados", 2600
		return

	$scope.test = ->
		console.log $scope
	return

