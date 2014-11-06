$(document).ready ->
    $(".step-two").hide()
    $("input[name=star],input[name=end]").datepicker dateFormat : "yy-mm-dd", showAnim : "slide"
    $("input[name=search]").on "change", changeSearch
    $(".btn-search").on "click", getSearch
    $(document).on "click", ".btn-purchase", openWindow
    $(document).on "click", ".btn-actions", showActions
    $(".btn-edtp").on "click", showEditPurchasae
    $(".btn-back").on "click", showStepOne
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
    return