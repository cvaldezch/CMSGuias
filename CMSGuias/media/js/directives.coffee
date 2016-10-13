# 'use strict'

# directive validate number min and max
valMinandMax = ->
	restrict: 'AE'
	require: '?ngModel'
	scope: '@'
	link: (scope, element, attrs, ngModel) ->
		element.bind 'blur', (event) ->
			console.log "inside event"
			result = 0
			valid = true
			vcurrent = element.val()
			if vcurrent is '' or vcurrent is undefined
				valid = false 
			console.log valid, vcurrent
			if valid
				vcurrent = parseFloat vcurrent		
				min = parseFloat attrs.min
				max = parseFloat attrs.max
				switch
					when vcurrent > max then result = max
					when vcurrent < min then result = min
					else result = vcurrent
				if attrs.hasOwnProperty 'ngModel'
					ngModel.$setViewValue result
					ngModel.$render()
					scope.$apply()
					console.log "change model"
					return
				else
					element.val result
					console.log "change attr"
					return
			else
				if attrs.hasOwnProperty 'ngModel'
					ngModel.$setViewValue result
					ngModel.$render()
					scope.$apply()
					console.log "change model"
					return
				else
					element.val result
					console.log "change attr"
					return
		return
