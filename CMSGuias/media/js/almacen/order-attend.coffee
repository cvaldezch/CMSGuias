app = angular.module 'attendApp', ['ngCookies', 'angular.filter']

app.config ($httpProvider) ->
	$httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
	$httpProvider.defaults.xsrfCookieName = 'csrftoken'
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
	return

app.directive 'cinmam', ($parse) ->
	restrict: 'A'
	require: '?ngModel'
	scope: '@'
	link: (scope, element, attrs, ngModel) ->
		element.bind 'change, blur', (event) ->
			if !isNaN(element.context.value) and element.context.value != ""
				val = parseFloat element.context.value
			else
				val = parseFloat attrs.max
			max = parseFloat attrs.max
			min = parseFloat attrs.min
			result = 0
			if val > max
				result = max
			else if val < min
				result = min
			else
				result = val
			if attrs.hasOwnProperty 'ngModel'
				ngModel.$setViewValue result
				ngModel.$render()
				scope.$apply()
				# ngModel.$parses.unshift (value) ->
				# 	ngModel.$setViewValue result
				# 	ngModel.$render()
				# 	return result
				# return
				# scope.$apply ->
				# 	# ngModel.$modelValue = result
				# 	scope.ngModel = result
				# 	return
				return
			else
				element.context.value = result
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
	obj.getStockItem = (options = {}) ->
		$http.get "", params: options
	
	obj

app.factory 'attendFactory', factories

controllers = ($scope, $timeout, $q, attendFactory) ->

	$scope.dorders = []
	$scope.vstock = false
	$scope.cstock = new Array()
	$scope.qmax = 0
	$scope.stks = []
	$scope.dguide = new Array()
	$scope.fchk = new Array()
	$scope.nipdetails = new Array()
	angular.element(document).ready ->
		# console.log "angular load success!"
		if $scope.init is true
			$scope.sDetailsOrders()
		return

	$scope.changeAttend = ($index) ->
		console.log "if star process remove #{$index}"
		# console.warn $scope.fchk
		if !$scope.fchk[$index].status
			# $scope.fchk[$index].status = !$scope.fchk[$index].status
			# console.log $scope.fchk[$index].status
			$scope.fchk[$index].quantity = 0
			# console.log $scope.dguide
			# console.log $index
			# console.info $scope.fchk
			angular.forEach $scope.dguide, (obj, index) ->
				m = ($scope.fchk[$index].materials == obj.materials)
				b = ($scope.fchk[$index].brand == obj.brand)
				o = ($scope.fchk[$index].model = obj.model)
				if m and b and o
					console.log obj
					console.warn $scope.fchk[$index]
					$scope.dguide.splice(index, 1)
					console.info $scope.dguide
				return
			$scope.enableGuide()
			# $scope.fchk[$index].status = !$scope.fchk[$index].status
			# $scope.apply()
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
					# angular.element("#itd#{value.fields.materiales.pk}#{value.fields.brand.pk}#{value.fields.model.pk}")
					# angular.forEach $scope.dorders, (val, key) ->
					# 	m = (val.fields.materiales.pk is value.fields.materiales.pk)
					# 	b = (val.fields.brand.pk is value.fields.brand.pk)
					# 	o = (val.fields.model.pk is value.fields.model.pk)
					# 	if m and b and o
					# 		$scope.dorders.splice key, 1
					# 		console.log key
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
						'tag': value.fields.tag
						# 'status': false
					return
				$scope.nTypes = response.types
				# console.table tmp
				$scope.dnip = tmp
				# change input readonly
				angular.forEach $scope.dnip, (object, index) ->
					# change input readonly
					a = angular.element("#q#{object.materials}#{object.brand}#{object.model}")
					
					return
				return
			else
				Materialize.toast "Error #{response.raise}", 3000, 'rounded'
				return
		return

	$scope.chkAll = ->
		selected = ->
			deferred = $q.defer()
			angular.forEach $scope.fchk, (obj, index) ->
				obj.status = $scope.chk
				if !$scope.chk
					$scope.changeAttend index
				return
			return deferred.promise
		selected().then (response) ->
			$scope.enableGuide()
			return
		# angular.forEach angular.element("[name=chk]"), (el) ->
		# 	el.checked = $scope.chk
		# 	return
		return

	validStock = ->
		defer = $q.defer()
		promises = []
		# create array with code materials
		angular.forEach angular.element("[name=chk]"), (el) ->
			# walk items selected
			if angular.element(el).is(":checked")
				promises.push
					materials: el.attributes["data-materials"].value
					name: el.attributes["data-mname"].value
					brand: el.attributes["data-brand"].value
					model: el.attributes["data-model"].value
					nbrand: el.attributes["data-nbrand"].value
					nmodel: el.attributes["data-nmodel"].value
					quantity: el.attributes['data-quantity'].value
				return
		$q.all(promises).then (response) ->
			defer.resolve response
			return
		return defer.promise

	$scope.getStock = ->
		validStock().then (result) ->
			$scope.cstock = result
			$scope.dguide = new Array()
			$scope.stock()
			return
		return

	$scope.stock = ->
		deferred = $q.defer()
		nextStep = ->
			if $scope.cstock.length > 0
				prm = $scope.cstock[0]
				# console.log prm
				prm['gstock'] = true
				attendFactory.getStockItem(prm)
				.success (response) ->
					if response.status
						# show stock item and remove item cstock
						# return false
						$scope.stks = new Array()
						$scope.istock = response.stock
						$scope.qmax = parseFloat prm.quantity
						$scope.gbrand = prm.brand
						$scope.gmodel = prm.model
						$scope.gmaterials = prm.materials
						angular.element("#sd").text "#{prm.name} #{prm.nbrand} #{prm.nmodel}"
						$scope.dstock = 
							'materials': prm.materials
							'brand': prm.brand
							'model': prm.model
						angular.element("#mstock").openModal
							dismissible: false
						console.info prm
						$scope.cstock.splice 0, 1
						console.log $scope.cstock
						deferred.resolve false
						return
					else
						# execute get Stock
						console.log response.raise
						deferred.resolve false
						return
				return
			else
				deferred.resolve true
				return
		nextStep()
		return deferred.promise
	
	# $scope.selectStock = ($event) ->
	# 	# console.log this
	# 	# get materials, brand, model and stock
	# 	# console.log angular.element("#stk#{this.x.fields.materials.pk}#{$scope.dstock['brand']}#{$scope.dstock['model']}")
	# 	stk = angular.element("#stk#{this.x.fields.materials.pk}#{$scope.dstock['brand']}#{$scope.dstock['model']}")
	# 	stk[0].value = this.x.fields.stock
	# 	angular.element("#mstock").closeModal()
	# 	$scope.stock()
	# 	.then (result) ->
	# 		console.warn result
	# 		if result
	# 			Materialize.toast "Complete!", 3000
	# 		else
	# 			console.log "Falta"
	# 	return

	$scope.showNip = (indexsnip) ->
		consulting = ->
			deferred = $q.defer()
			promises = new Array()
			# tmp = new Array()
			angular.forEach $scope.dnip, (obj, index) ->
				mat = ($scope.gmaterials is obj.materials)
				brand = ($scope.gbrand is obj.brand)
				model = ($scope.gmodel is obj.model)
				if mat and brand and model
					promises.push obj
					return
			$q.all(promises).then (response) ->
				deferred.resolve response
				return
			return deferred.promise
		verify = ->
			# console.log "star verify"
			defer = $q.defer()
			# promises = new Array()
			ver = false
			console.error $scope.nipdetails
			angular.forEach $scope.nipdetails, (obj, index) ->
				console.warn obj
				mat = ($scope.gmaterials is obj.materials)
				brand = ($scope.gbrand is obj.brand)
				model = ($scope.gmodel is obj.model)
				console.info mat, brand, model
				if mat and brand and model
					ver = (obj.details.length > 0 ? true : false)
					# console.log ver
				defer.resolve ver
				return
			defer.resolve ver
			# console.log ver
			# console.log "finish verify"
			return defer.promise
		verify().then (response) ->
			# console.log "VERIFY " + response
			$scope.indexshownip = indexsnip
			if response is true
				# get data
				angular.forEach $scope.nipdetails, (obj, index) ->
					mat = ($scope.gmaterials is obj.materials)
					brand = ($scope.gbrand is obj.brand)
					model = ($scope.gmodel is obj.model)
					if mat and brand and model
						$scope.snip = obj.details
						angular.element("#snip").openModal
							dismissible: false
						return
			else
				# execute function consulting
				consulting().then (result) ->
					if result.length > 0
						# show modal
						$scope.snip = result
						angular.element("#snip").openModal
							dismissible: false
						return
				return
		return
	
	$scope.validSelectStock = ->
		# valid item select for stock
		# deferred = $q.defer
		# promise = deferred.promise
		# console.log $scope.stks
		tmp = new Array()
		amount = 0
		angular.forEach $scope.stks, (obj, index) ->
			amount += obj['quantity']
			return
		# console.log amount
		if amount > $scope.qmax
			Materialize.toast "<i class='fa fa-times fa-3x red-text'></i>&nbsp;Cantidad mayor a la requerida.", 6000
		else if amount <= 0
			Materialize.toast "<i class='fa fa-times fa-3x red-text'></i>&nbsp;Cantidad menor que 0.", 6000
		else
			# stk = angular.element("#q#{$scope.gmaterials}#{$scope.gbrand}#{$scope.gmodel}")
			$scope.dguide.push
				'materials': $scope.gmaterials
				'brand': $scope.gbrand
				'model': $scope.gmodel
				'amount': amount
				'details': new Array()
			angular.forEach $scope.dguide, (obj, index) ->
				m = (obj.materials is $scope.gmaterials)
				b = (obj.brand is $scope.gbrand)
				o = (obj.model is $scope.gmodel)
				if m and b and o
					angular.forEach $scope.stks, (stk, i) ->
						if stk.chk is true
							obj.details.push
								'materials': $scope.gmaterials
								'brand': stk.brand
								'model': stk.model
								'quantity': stk.quantity
							return
					return
			angular.forEach $scope.fchk, (obj, index) ->
				m = (obj.materials is $scope.gmaterials)
				b = (obj.brand is $scope.gbrand)
				o = (obj.model is $scope.gmodel)
				if m and b and o
					$scope.fchk[index].quantity = amount
				return
			# console.log stk
			# stk[0].value = amount
			console.info "Nothing generate guide"
			# poner en cero la cantidad
			# console.warn $scope.dguide
			$scope.stock()
			.then (result) ->
				# console.warn result
				if result
					$scope.enableGuide()
					angular.element("#mstock").closeModal()
					Materialize.toast "Completo!", 3000
					return
				else
					console.log "Falta"
					return
		return
	
	$scope.enableGuide = ->
		sd = ->
			defered = $q.defer()
			promises = new Array()
			count = 0
			angular.forEach $scope.dguide, (obj) ->
				# console.log obj
				if obj.amount > 0
					count++
					promises.push count
					return
			$q.all(promises).then (response) ->
				defered.resolve response.length
				return
			return defered.promise
		sd().then (result) ->
			# console.info result
			if result > 0
				$scope.vstock = true
				return
			else
				$scope.vstock = false
				return
		return

	$scope.verifyNip = ->
		console.log "star verify"
		defer = $q.defer()
		promises = new Array()

		for key, obj of $scope.nipdetails
			console.log "check nip obj", key
			console.log obj
			ver = -1
			mat = ($scope.gmaterials is obj.materials)
			brand = ($scope.gbrand is obj.brand)
			model = ($scope.gmodel is obj.model)
			if mat and brand and model
				ver = parseInt key
				promises.push ver
				# return false
			else
				promises.push ver
		
		# angular.forEach $scope.nipdetails, (obj, index) ->
		# 	ver = -1
		# 	mat = ($scope.gmaterials is obj.materials)
		# 	brand = ($scope.gbrand is obj.brand)
		# 	model = ($scope.gmodel is obj.model)
		# 	if mat and brand and model
		# 		ver = index
		# 		promises.push ver
		# 	else
		# 		promises.push ver
		$q.all(promises).then (response) ->
			console.info response
			count = Array.from(new Set(response))
			if count.length >= 1
				if count[0] isnt -1
					defer.resolve count[0]
					return
				else
					defer.resolve count[1]
					return
			else
				defer.resolve -1
				return
		return defer.promise

	$scope.selectNip = ->	
		$scope.verifyNip().then (response) ->
			console.warn response
			amount = 0
			for i, x of $scope.snip
				amount += ((x.meter * x.guide)/100)
			$scope.stks[$scope.indexshownip].quantity = amount
			if response >= 0
				$scope.nipdetails[response].details = $scope.snip
				$scope.snip = new Array()
				angular.element("#snip").closeModal()
				# console.log $scope.nipdetails
				return
			else
				$scope.nipdetails.push
					'materials': $scope.gmaterials
					'brand': $scope.gbrand
					'model': $scope.gmodel
					'details': $scope.snip
				$scope.snip = new Array()
				angular.element("#snip").closeModal()
				# console.log $scope.nipdetails
				return
		return
	
	$scope.setZeroNip = ->
		console.log $scope.snip
		return

	$scope.selectOrderNip = (idx = -1) ->
		if idx is -1
			angular.forEach $scope.snip, (obj, index) ->
				obj.status = $scope.ns
				if !obj.status
					$scope.snip[index].guide = 0
				return
		if idx >= 0
			if !$scope.snip[idx].status
				$scope.snip[idx].guide = 0
		return

app.controller 'attendCtrl', controllers
	