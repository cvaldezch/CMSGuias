$(document).ready ->
    $(".step-two, .panel-add").hide()
    $("input[name=star],input[name=end]").datepicker dateFormat : "yy-mm-dd", showAnim : "slide"
    $("input[name=search]").on "change", changeSearch
    $(".btn-search").on "click", getSearch
    $(document).on "click", ".btn-purchase", openWindow
    $(document).on "click", ".btn-actions", showActions
    $(".btn-edtp").on "click", showEditPurchasae
    $(".btn-back").on "click", showStepOne
    $("input[name=select]").on "change", changeSelect
    $(".btn-show-add").on "mouseenter mouseleave", animateAdd
    .on "click", showPanelAdd
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
                                        <td><button value=\"{{ purchase }}\" class=\"btn btn-xs btn-link text-black btn-purchase\"><span class=\"glyphicon glyphicon-list\"></span></a>
                                        </td>
                                        <td>
                                            {{!status}}
                                        </td>
                                    </tr>"
                        $tb = $("table > tbody")
                        $tb.empty()
                        for x of response.list
                            if response.list[x].status == 'PE'
                                tmp = template.replace "{{!status}}", "<button class=\"btn btn-xs btn-link text-black btn-actions\" value=\"{{ purchase }}\">
                                                <span class=\"glyphicon glyphicon-ok\"></span>
                                            </button>"
                            else
                                tmp = template
                            response.list[x].item = (parseInt(x) + 1)
                            $tb.append Mustache.render tmp, response.list[x]
                        return
            return
    return

openWindow = ->
    window.open("/reports/order/purchase/#{@value}/","_blank")
    return

showActions = (event) ->
    $(".btn-delp,.btn-edtp").val @value
    $(".mactions").modal "toggle"
    return

showEditPurchasae = (event) ->
    $(".mactions").modal "hide"
    $(".nrop").text @value
    getDataPurchase @value
    $(".step-one").fadeOut 150
    $(".step-two").fadeIn 800
    return

showStepOne = (event) ->
    $(".nrop").text ""
    $(".step-two").fadeOut 150
    $(".step-one").fadeIn 800
    return

getDataPurchase = (purchase) ->
    data = new Object
    data.purchase = purchase
    data.getpurchase = true
    $.getJSON "", data, (response) ->
        if response.status
            $("[name=rucandreason]").text response.reason
            $("input[name=ruc]").val response.supplier
            $("input[name=reason]").val response.reason
            $("input[name=delivery]").val response.space
            $("select[name=document]").val response.document
            $("select[name=payment]").val response.method
            $("select[name=currency]").val response.currency
            $("input[name=transfer]").val response.transfer
            $("input[name=contact]").val response.contact
            $("input.edsct").val response.discount
            $("span.eigv").text "#{response.igv}%"
            $tb = $("table.table-pod > tbody")
            $tb.empty()
            template = "<tr>
                        <td>
                        <input type=\"checkbox\" name=\"mats\" value=\"{{ materials }}\">
                        </td>
                        <td>{{ item }}</td>
                        <td>{{ materials }}</td>
                        <td>{{ name }}</td>
                        <td>{{ meter }}</td>
                        <td>{{ unit }}</td>
                        <td>{{ brand }}</td>
                        <td>{{ model }}</td>
                        <td>{{ quantity }}</td>
                        <td>{{ price }}</td>
                        <td>{{ discount }}</td>
                        <td>{{ amount }}</td>
                        <td>
                            <button class=\"btn btn-xs btn-link text-green\">
                                <span class=\"glyphicon glyphicon-edit\"></span>
                            </button>
                        </td>
                        </tr>"
            for x of response.details
                response.details[x].item = parseInt(x) + 1
                $tb.append Mustache.render template, response.details[x]
            calcAmount()
            return
        else
            $().toastmessage "showWarningToast", "No se han conseguidos los datos. #{response.raise}"
    return

calcAmount = (event) ->
    amount = 0
    $("table.table-pod > tbody > tr").each (index, element) ->
        $td = $(element).find "td"
        amount += convertNumber $td.eq(11).text()
        return
    $(".tamount").text amount.toFixed 2
    dsct = ((amount * convertNumber($("input.edsct").val())) / 100)
    $(".tdsct").text dsct.toFixed 2
    amount = (amount - dsct)
    igv = $("span.eigv").text().split("%")[0]
    igv = (amount * convertNumber(igv) / 100)
    $(".tigv").text igv.toFixed 2
    $(".ttotal").text (amount + igv).toFixed 2
    return

changeSelect = (event) ->
    $("input[name=select]").each (ind, radio)->
        if @checked
            $("input[name=mats]").each (index, element) ->
                element.checked = Boolean parseInt radio.value
                return
            return
    return

showPanelAdd = (event) ->
    btn = @
    $(".panel-add").fadeToggle 600, ->
        if @style.display is 'block'
            $(btn).removeClass "btn-success text-black"
            .addClass "btn-default"
            .find "span"
            .eq 0
            .removeClass "fa-plus-square-o"
            .addClass "fa-times-circle-o"
            $(btn).find "span"
            .eq 1
            .text "Cancelar"
            return
        else
            $(btn).removeClass "btn-default"
            .addClass "btn-success"
            .addClass "text-black"
            .find "span"
            .eq 0
            .removeClass "fa-times-circle-o"
            .addClass "fa-plus-square-o"
            $(btn).find "span"
            .eq 1
            .text "Agregar Material"
            return
    return

addNewMaterialPurchase = (event) ->
    data = new Object
    data.code = $.trim $(".id-mat").text()
    if data.code.length isnt 15
        $().toastmessage "showWarningToast", "Seleccione por lo menos un material para ingresar."
        return false
    data.quantity = convertNumber $("input[name=quantity]").val()
    if isNaN(data.quantity) or data.quantity <= 0
        $().toastmessage "showWarningToast", "La cantidad ingresada debe ser mayor a 0."
        return false
    data.price = convertNumber $("input[name=price]").val()
    if isNaN(data.price) or data.quantity <= 0
        $().toastmessage "showWarningToast", "El precio ingresado debe ser mayor a 0."
        return false
    data.brand = $("select[name=brand]").val()
    data.model = $("select[name=model]").val()
    if data.brand isnt "" and data.model isnt ""
        $().toastmessage "showWarningToast", "Debe de seleccionar una marca y modelo."
        return false
    if $("input[name=gincludegroup]").length and $("input[name=gincludegroup]").is(":checked")
        if tmpObjectDetailsGroupMaterials.details.length
            data.details = tmpObjectDetailsGroupMaterials.details
    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
    $.post "", data, (response) ->
        if response.status
            listDetails()
            return
    return

listDetails = (event) ->
    calcAmount()
    return