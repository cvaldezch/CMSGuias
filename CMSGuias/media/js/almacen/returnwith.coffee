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
			if RegExp(/[0-9]{3}[-]{1}[0-9]{8}/).test(vl)
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

	angular.element(document).ready ->
		console.log "Document ready"
		return

	$scope.getdetailsGuide = ->
		
		return
	
	$scope.test = ->
		console.log $scope.valid
		console.log $scope.tmpg
		console.log $scope.guide
		return

	$scope.$watch 'guide', (nw, old) ->
		if nw isnt old
			console.log nw
			prm =
				getdetails: true
				guide: nw
			returnFactory.getDetailsGuide prm
			.success (response) ->
				if response.status
					$scope.dguide = response.details
					return
				else
					Materialize.toast "<i class='fa fa-times red fa-2x'></i> No se cargo el detalle del número de guia ", 4000
					return
			return
	return
# (scope, element, attrs) ->
#   element.bind 'keypress', (event) ->.
#       key = event.keyCode
#       console.log key
#       return
#   return