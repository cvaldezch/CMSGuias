$(document).ready ->
	$(".step-second,.step-tree").hide()
	$("input[name=start], input[name=end]").datepicker "showAnim" : "slide", "dateFormat" : "yy-mm-dd"
	$("input[name=search]").on "change", changeSearch
	$(".btn-search").on "click", searchPurchase
	$(document).on "click", ".btn-deposit", showDeposit
	$(document).on "click", ".btn-action", showAction
	$(".btn-ingress").on "click", showIngressInventory
	$(document).on "blur", ".materials", validQuantityBlur
	$(document).on "change", "input[name=mats]", changeCheck
	$("[name=select]").on "change", changeSelect
	$(".btn-generate-note").on "click", loadIngress
	$(".btn-generate").on "click", saveNoteIngress
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
						<td class=\"text-center\">
							<button value=\"{{ purchase }}\" data-ruc=\"{{ x.supplier }}\" class=\"btn btn-link btn-xs text-black btn-deposit\"><span class=\"glyphicon glyphicon-credit-card\"></span></button>
						</td>
						<td class=\"text-center\">
							<a href=\"/reports/order/purchase/{{ purchase }}/\" target=\"_blank\" class=\"btn btn-xs btn-link text-black\"><span class=\"glyphicon glyphicon-eye-open\"></span></a>
						</td>
						<td class=\"text-center\">
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
	$(".maction").modal("show").find("button").val @value
	return

showIngressInventory = (event) ->
	btn = @value
	$.getJSON "", "purchase" : btn, (response) ->
		if response.status
			$(".supplier").html response.head.supplier
			$(".quote").html response.head.quote
			$(".place").html response.head.place
			$(".document").html response.head.document
			$(".payment").html response.head.payment
			$(".currency").html response.head.currency
			$(".register").html response.head.register
			$(".transfer").html response.head.transfer
			$(".contact").html response.head.contact
			$(".performed").html response.head.performed
			# $(".deposit").append "<a target=\"_blank\" class=\"btn btn-warning btn-xs text-black\" href=\"/media/#{response.head.deposit}\"><span class=\"glyphicon glyphicon-cloud-download\"></span></a>"
			template = "<tr><td><input type=\"checkbox\" name=\"mats\" value=\"{{ materials }}\"></td><td>{{ item }}</td><td>{{ materials }}</td><td>{{ name }}</td><td>{{ measure }}</td><td>{{ unit }}</td><td>{{ quantity }}</td><td><input type=\"number\" class=\"form-control input-sm materials\" name=\"{{ materials }}\" value=\"{{ quantity }}\" min=\"1\" max=\"{{ quantity }}\" disabled></td></tr>"
			$tb = $("table.table-ingress > tbody")
			$tb.empty()
			for x of response.details
				response.details[x].item = parseInt(x) + 1
				$tb.append Mustache.render template, response.details[x]

			$(".purchase").html btn
			$("[name=purchase]").val btn
			$(".maction").modal "hide"
			$(".step-first").fadeOut 200
			$(".step-second").fadeIn 600
			return
	return

validQuantityBlur = (event) ->
	min = parseFloat(@getAttribute("min").replace ",",".")
	max = parseFloat(@getAttribute("max").replace ",",".")
	val = parseFloat(@value.replace ",",".")
	if val < min or val > max
		if val < min
			@value = min
		else if val > max
			@value = max
	return

changeCheck = (event) ->
	$mat = $("input[name=#{@value}]")
	if @checked
		$mat.attr "disabled", false
	else
		$mat.attr "disabled", true
	return

changeSelect = (event) ->
	if @checked
		chek = Boolean(parseInt @value)
		$("input[name=mats]").each (index, element) ->
			element.checked = chek
			$(element).change()
			return
	return

loadIngress = (event) ->
	arr = new Array()
	$("input[name=mats]").each (index, element) ->
		if element.checked
			arr.push {"materials": element.value, "quantity": $("input[name=#{element.value}]").val()}
			return
	if arr.length
		$(".mingress").modal "toggle"
	else
		$().toastmessage "showWarningToast", "Seleccione por lo menos un material para hacer el ingreso a almacén."
	return

saveNoteIngress = (response) ->
	data = new Object()
	mats = new Array()
	pass = false
	$("input[name=mats]").each (index, element) ->
		if element.checked
			mats.push {"materials": element.value, "quantity": $("input[name=#{element.value}]").val()}
			return
	data.details = JSON.stringify mats
	$(".mingress > div > div > div.modal-body > div.row").find("input, select").each (index, element) ->
		console.info element
		if element.name isnt "guide"
			if $.trim element.value isnt ""
				data[element.name] = $.trim $(element).val()
				pass = true
				return
			else
				$().toastmessage "showWarningToast", "Campo vacio, #{element.name}"
				pass = false
				return pass
	console.log pass
	if pass
		$().toastmessage "showToast",
			text : "Desea generar una <q>Nota de Ingreso</q> con los materiales seleccionados?"
			sticky : true
			type : "confirm"
			buttons : [{value:"Si"},{value:"No"}]
			success : (result) ->
				if result is "Si"
					data.ingress = true
					data.observation = $("textarea[name=observation]").val()
					data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
					console.warn data
					$.post "", data, (response) ->
						if response.status
							$(".step-second").fadeOut 200
							$(".step-tree").fadeIn 600
							# $().html response.ingress
						else
							$().toastmessage "showWarningToast", "No se a podido generar la Nota de Ingreso."
							return
	return