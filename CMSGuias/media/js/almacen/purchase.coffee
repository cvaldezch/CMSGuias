$(document).ready ->
	$("input[name=start], input[name=end]").datepicker "showAnim" : "slide", "dateFormat" : "yy-mm-dd"
	$("input[name=search]").on "change", changeSearch
	$(".btn-search").on "click", searchPurchase
	$(document).on "click", ".btn-deposit", showDeposit
	$(document).on "click", ".btn-action", showAction
	return

changeSearch = ->
	if @checked
		if  @value is "code"
			$("input[name=code]").attr "disabled", false
			$("input[name=start],input[name=end]").attr "disabled", true
		else if @value is "dates"
			$("input[name=code]").attr "disabled", true
			$("input[name=start],input[name=end]").attr "disabled", false
	return

searchPurchase = ->
	data = new Object()
	$("input[name=search]").each (index, element) ->
		if element.checked
			data.type = element.value
			if element.value is "code"
				data.code =  $("input[name=code]").val()
				return
			else if element.value is "dates"
				data.start = $("input[name=start]").val()
				if $("input[name=end]").val().length is 10
					data.end = $("input[name=end]").val()
				return

	if data.type is "code"
		if data.code.length is 10
			data.pass = true
		else
			data.pass = false
			$().toastmessage "showWarningToast", "No se a ingresado el código."
	else if data.type is "dates"
		if data.start.length is 10
			data.pass = true
		else
			data.pass = false
			$().toastmessage "showWarningToast", "No se han ingresado la fecha a buscar."
	if data.pass
		$.getJSON "", data, (response) ->
			if response.status
				console.log response
				listTemplate response.list
				return
			else
				$().toastmessage "showWarningToast", "Se han encontrado errores. #{response.raise}"
				return
	return

listTemplate = (list)->
	$tb = $("table > tbody")
	$tb.empty()
	if list.length
		template = "<tr>
						<td>{{ item }}</td>
						<td>{{ purchase }}</td>
						<td>{{ reason }}</td>
						<td>{{ document }}</td>
						<td>{{ transfer }}</td>
						<td>
							<button value=\"{{ purchase }}\" data-ruc=\"{{ x.supplier }}\" class=\"btn btn-link btn-xs text-black btn-deposit\"><span class=\"glyphicon glyphicon-credit-card\"></span></button>
						</td>
						<td>
							<button value=\"{{ purchase }}\" data-ruc=\"{{ x.supplier }}\" class=\"btn btn-link btn-xs text-black btn-action\"><span class=\"glyphicon glyphicon-inbox\"></span></button>
						</td>
					</tr>"
		for x of list
			list[x].item = (parseInt(x) + 1)
			$tb.append Mustache.render template, list[x]
	return

showDeposit = ->
	purchase = @value
	supplier = @getAttribute "data-ruc"
	url = "/media/storage/compra/#{purchase}/#{supplier}.pdf"
	window.open(url, "Deposit")
	return

showAction = ->
	$(".maction").modal("toggle")
	return