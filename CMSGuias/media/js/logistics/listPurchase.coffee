$(document).ready ->
	$("input[name=star],input[name=end]").datepicker dateFormat : "yy-mm-dd", showAnim : "slide"
	$("input[name=search]").on "change", changeSearch
	$(".btn-search").on "click", getSearch
	$(document).on "click", ".btn-purchase", openWindow
	return

changeSearch = ->
	if @checked
		if @value is "status"
			$("input[name=star],input[name=end],input[name=code]").attr "disabled", true
			$("select[name=status]").attr "disabled", false
			return
		else if @value is "dates"
			$("input[name=star],input[name=end]").attr "disabled", false
			$("select[name=status],input[name=code]").attr "disabled", true
			return
		else if @value is "code"
			$("input[name=star],input[name=end],select[name=status]").attr "disabled", true
			$("input[name=code]").attr "disabled", false
			return
	return

getSearch = ->
	$("input[name=search]").each (index, element) ->
		if element.checked
			data = new Object()
			if element.value is "code"
				if $("input[name=code]").val() isnt ""
					data.code = $("input[name=code]").val()
					data.pass = true
				else
					data.pass = false
					$().toastmessage "showWarningToast", "campo de estado se encuntra vacio."
			else if element.value is "status"
				if $("select[name=status]").val() isnt ""
					data.status = $("select[name=status]").val()
					data.pass = true
				else
					data.pass = false
					$().toastmessage "showWarningToast", "campo de estado se encuntra vacio."
			else if element.value is "dates"
				start = $("input[name=star]").val()
				if start isnt ""
					data.dates = true
					data.start = start
					data.pass = true
				else
					data.pass = false
					$().toastmessage "showWarningToast", "campo de fecha inicio se encuntra vacio."
				end = $("input[name=end]").val()
				if end isnt ""
					data.end = end
			console.log data
			if data.pass
				$.getJSON "", data, (response) ->
					if response.status
						template = "<tr>
										<td>{{ item }}</td>
										<td>{{ purchase }}</td>
										<td>{{ document }}</td>
										<td>{{ transfer }}</td>
										<td>{{ currency }}</td>
										<td><a class=\"text-black\" target=\"_blank\" href=\"/media/{{ deposito }}\"><span class=\"glyphicon glyphicon-file\"></span></a></td>
										<td><button value=\"{{ purchase }}\" class=\"btn btn-xs btn-link text-black btn-purchase\"><span class=\"glyphicon glyphicon-list\"></span></a></td>
									</tr>"
						$tb = $("table > tbody")
						$tb.empty()
						for x of response.list
							response.list[x].item = (parseInt(x) + 1)
							$tb.append Mustache.render template, response.list[x]
						return
			return
	return

openWindow = ->
	window.open("/reports/order/purchase/#{@value}/","_blank")
	return