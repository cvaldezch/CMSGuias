app = angular.module 'cpurApp', ['ngCookies']
app.config ($httpProvider) ->
	$httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest'
	$httpProvider.defaults.xsrfCookieName = 'csrftoken'
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
	return

app.factory 'fPuchase', ($http, $cookies) ->
	$http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
	$http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
	obj = new Object
	obj.filterPurchase = (options = {}) ->
		$http.get '', params: options
	obj.filterMaterials = (options = {}) ->
		$http.get '', params: options
	obj.filterHist = (options = {}) ->
		$http.get '', params: options
	
	obj

app.controller 'cPurchase', ($scope, $timeout, fPuchase) ->

	$scope.filterNroPurchase = ->
		if $scope.filpur isnt '' and $scope.filpur.length == 10
			$scope.purchase = []
			prm =
				'byPurchase': true
				'compra': $scope.filpur
			fPuchase.filterPurchase(prm)
			.success (response) ->
				if response.status
					$scope.purchase = response.details
					$scope.purbedside = response.bedside[0]
					return
				else
					swal
						title: "No se ha encontrado datos"
						text: ""
						type: "warning"
						timer: 2600
					return
		return

	$scope.filterMaterialsByYear = ($event) ->
		if $scope.filmat isnt '' and $event.which is 13
			$scope.lsearch = []
			prm =
				'byMaterials': true
				'materials': $scope.filmat
			fPuchase.filterMaterials(prm)
			.success (response) ->
				if response.status
					$scope.resultmat = response.result
					angular.element("#mresult").openModal()
					return
				else
					swal
						title: "No se ha encontrado datos"
						text: ""
						type: "warning"
						timer: 2600
					return
		return

	$scope.getHistotyMat = (mat = '') ->
		prm = {}
		if mat is ''
			mat = $scope.hmat
			prm['year'] = $scope.sbyear
		else
			$scope.hmat = mat

		prm['materiales'] = mat
		prm['getMaterialHist'] = true
		fPuchase.filterHist(prm)
		.success (response) ->
			if response.status
				$scope.resumen = response.resumen
				# $scope.ryear = response.years
				angular.element("#mresult").closeModal()
				if response.hasOwnProperty 'years'
					$scope.syears = response.years
				$scope.sbyear = response.resumen[0].fields.compra.fields.registrado.substr(0, 4)
				return
			else
				swal
					title: "No se ha encontrado datos"
					text: ""
					type: "warning"
					timer: 2600
				return
		return

	$scope.$watch 'fop', (nval) ->
		if nval is true
			$scope.fm = false
			return
	$scope.$watch 'fm', (nval) ->
		if nval is true
			$scope.fop = false
			return
	return
