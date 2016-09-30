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
		element.bind 'keypress', (event) ->
			keycode = event.which or event.keyCode
			console.log keycode
			if (keycode < 48 or keycode > 57) and keycode != 8 and keycode != 45
				console.log "key block", keycode
				event.preventDefault()
				return false
			return
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

		return

app.controller 'ctrlReturnWith', ($scope, $timeout) ->

	$scope.valid = false
	$scope.guide = ''

	angular.element(document).ready ->
		console.log "Document ready"
		return

	$scope.test = ->
		console.log $scope.valid
		console.log $scope.tmpg
		console.log $scope.guide
		return
	return
# (scope, element, attrs) ->
#   element.bind 'keypress', (event) ->.
#       key = event.keyCode
#       console.log key
#       return
#   return