$(document).ready ->
    $(".panel-purchase-order-toggle").hide()
    $("input[name=podt],input[name=podf]").datepicker
        "changeYear": true
        "changeMonth": true
        "showAnim": "slide"
        "dateFormat": "yy-mm-dd"

    $(".new-sector").on "click", openNewSector
    $(document).on "click", ".btn-edit-sector", openUpdateSector
    $(".new-subproject").on "click", openNewSubproyecto
    $(document).on "click", "#accordion > .panel-primary", setSubproject
    $(document).on "click", ".btn-edit-sub", openUpdateSubproject
    $(".btn-responsible").on "click", ->
        $(".mresponsible").modal("show");
    $(".btn-files").on "click", ->
        $(".mfiles").modal("show");
    $(".btn-cuadro").on "click", (evetn) ->
        changeView 23
    $(".btn-list").on "click", (event) ->
        changeView 100
    $(".btn-admin").on "click", ->
        $("[name=administrative]").click()
    $(".btn-opera").on "click", ->
        $("[name=operation]").click()
    $(".btn-upload-files").on "click", uploadFiles
    $(".btn-show-comment").on "click", toggleComment
    $(".btn-message-edit").on "click", showEditComment
    $(".btn-message-del").on "click", showEditComment
    $(".btn-assigned").on "click", assignedResponsible
    $(".btn-approved").on "click", approvedProject
    $(document).on "click", ".btn-del-sub", deleteSubproject
    $(".btn-add-purchase-order-details").on "click", addDetailsPurchase
    $("input[name=podt]").on "change", getPercentIVA
    $(document).on "click", ".btn-edit-pod", showEditDetailsPurchase
    $(document).on "click", ".btn-del-pod", deleteDetailsPurchase
    $(".btn-re-purchase-order").on "click", getListPurchaseOrder
    $(".btn-saved-purchase").on "click", savePurchaseOrder
    $(document).on "click", ".btn-edit-purchase", getEditPurchase
    $(document).on "click", ".btn-del-purchase", deleteOrderPurchase
    $(".btn-details-purchare-order-toggle").click ->
        $btn = $(@)
        $("div.panel-purchase-order-toggle").toggle 600
        , ->
            if $(".panel-purchase-order-toggle").is(":visible")
                $btn.find "span"
                .eq 0
                .removeClass "glyphicon-plus-sign"
                .addClass "glyphicon-minus-sign"
                $btn.find "span"
                .eq 1
                .text "Cancelar"
                $btn.removeClass "text-green"
                .addClass "text-red"
                return
            else
                $btn.find "span"
                .eq 0
                .removeClass "glyphicon-minus-sign"
                .addClass "glyphicon-plus-sign"
                $btn.find "span"
                .eq 1
                .text "Agregar Detalle"
                $btn.removeClass "text-red"
                .addClass "text-green"
                return
            $("input[name=podedit]").val ""
        return
    $("button.btn-add-purchase-order").mouseover ->
        $(@).find "span"
        .removeClass "glyphicon-plus-sign"
        .addClass "glyphicon-plus"
        return
    .mouseout ->
        $(@).find "span"
        .removeClass "glyphicon-plus"
        .addClass "glyphicon-plus-sign"
        return
    .click ->
        $("div.mpurchase").modal "toggle"
        return
    $("#message").focus ->
        $(@).animate
            "height": "102px"
        , 500
        return
    .blur ->
        $(@).animate
            "height": "34px"
        , 500
        return
    $("input[name=poids]").blur (event) ->
        percent = parseFloat(@value)
        if not isNaN(percent)
            @value = percent.toFixed 3
            calAmountPurchaseOrder()
        else
            @value = 0
            $().toastmessage "showWarningToast", "Solo se aceptan Números."
        $(".pods").text("#{@value}%")
        return
    .change (event) ->
        $(".pods").text("#{@value}%")
        calAmountPurchaseOrder()
        return
    treeAdminaandOpera()
    getListPurchaseOrder()
    tinymce.init
        selector: "textarea#message",
        theme: "modern",
        menubar: false,
        statusbar: false,
        plugins: "link contextmenu",
        font_size_style_values : "10px,12px,13px,14px,16px,18px,20px",
        toolbar: "undo redo | styleselect | fontsizeselect |"
    $(".btn-publisher").on "click", publisherCommnet
    $("button.btn-emails").on "click", showAlertStartProject
    $("input[name=mailer-enable]").checkboxpicker()
    .on "change", loadsAccounts
    $("button.btn-gen-responsible").on "click", genKeyConfirmationResponsible
    $("button.btn-gen-approved").on "click", genKeyConfirmationApproved
    $("button.btn-show-loadprices").on "click", showLoadPrices
    $("button[name=upload-prices]").on "click", uploadLoadPrices
    return

loadsAccounts = (event) ->
    if $("input[name=mailer-enable]").is(":checked")
        showGlobalEnvelop()
        $("iframe#globalmbody_ifr").contents().find("body").html $("#message_ifr").contents().find("body").html()
        if $("select[name=globalmfor]").find("option").length == 0
            getAllCurrentAccounts()
            setTimeout ->
                if globalMailerData.hasOwnProperty("fors")
                    items = ["for", "cc", "cco"]
                    for c in items
                        $item = $("select[name=globalm#{c}]")
                        tmp = "<option value=\"{{ email }}\">{{ email }}</option>"
                        for x in globalMailerData.fors
                            $item.append "<option value=\"#{x}\">#{x}</option>"
                        $item.trigger("chosen:updated")
                    return
            , 200
    return

showAlertStartProject = (event) ->
    $pro = $("input[name=pro]")
    reason = $("input[name=companyname]").val()
    # getAllCurrentAccounts()
    setTimeout  ->
        ###globalMailerData.fors = "asistente1@icrperusa.com,
                            logistica@icrperusa.com,
                            luis.martinez@icrperusa.com,
                            cvaldezchavez@gmail.com,
                            icr.luisvalencia@gmail.com,
                            almacen@icrperusa.com,
                            armando.atencio@icrperusa.com,
                            steven.paredes@icrperusa.com,
                            danilo.martinez@icrperusa.com,
                            sandra.atencio@icrperusa.com,
                            ssoma1@icrperusa.com"###
        globalMailerData.issue = "Apertura de Proyecto #{$pro.attr "data-name"} - #{$pro.attr "data-customers"}"
        globalMailerData.body = "
        <p><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\">Estimados,</span></p><p style=\"text-align: justify;\" data-mce-style=\"text-align: justify;\"><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\">Para hacerles de su conocimiento que hoy #{new Date().toLocaleDateString() } se realiza la apertura del proyecto <strong>\"#{$pro.attr "data-name"}\"</strong>  con código <strong>\"#{$pro.val()}\"</strong> que se realizara en \"#{$pro.attr "data-address"}\" para el cliente <strong>\"#{$pro.attr "data-customers"}\"</strong>. El proyecto tendrá como fecha de inicio #{$pro.attr "data-star"} y un fecha de termino aproximada para el #{$pro.attr "data-end"}.</span></p><p><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\">#{$(".contact-project").html().trim()}</span></p><p><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\"><strong>Ing. Steven Paredes</strong> asignar supervisor.</span></p><p><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\"><strong>Ejecutado por</strong> : #{reason}</span></p><p><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\"><br data-mce-bogus=\"1\"></span></p><p><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\">Saludos.</span></p><p><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\"><strong>Luis Martinez</strong></span><br /><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\"><strong>#{$("input[name=companyname]").val()}</strong></span><br></p><p><span style=\"font-size: 10pt;\" data-mce-style=\"font-size: 10pt;\"><strong>Telf:</strong> #{$("input[name=companyname]").attr("data-phone")}</span></p><p><br data-mce-bogus=\"1\"></p>
        "
    , 100
    setTimeout ->
        $("input[name=user-email]").val "luis.martinez@icrperusa.com"
        .attr "data-name", "Luis Martinez"
        showGlobalEnvelop()
    , 800
    return

approvedProject = ->
    data = new Object()
    data.type = "approved"
    #data.admin = $("select[name=admin-approve]").val()
    data.passwd = $("input[name=passwd-approve]").val()
    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
    $().toastmessage "showToast",
        text : "Realmente desea habilitar el proyecto?"
        type : "confirm"
        sticky : true
        buttons : [{value:'No'},{value:'Si'}]
        success : (result) ->
            if result is "Si"
                $.post "", data, (response) ->
                    if response.status
                        location.reload()
                    else
                        $().toastmessage "showWarningToast", "Fallo Transaccion: #{response.raise}"
                , "json"
                return
    return

assignedResponsible = ->
    responsible  = $("select[name=responsible]").val()
    #admin = $("select[name=admin]").val()
    passwd = $("input[name=passwd]").val()
    if responsible? and passwd?
        data = new Object()
        data.responsible = responsible
        #data.admin = admin
        data.passwd = passwd
        data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
        data.type = 'responsible'
        # console.info data
        $.post "", data, (response) ->
            if response.status
                location.reload()
            else
                $().toastmessage "showErrorToast", "El código ingresado es incorrecto: #{response.raise}"
        return
    return

publisherCommnet = ->
    data = new Object()
    data.edit = $("input[name=edit-message]").val()
    data.message = $.trim $("#message_ifr").contents().find("body").html()
    data.status = $("select[name=message-status]").val()
    if data.message is "<p><br data-mce-bogus=\"1\"></p>"
        $().toastmessage "showWarningToast", "No se puede publicar el mensaje, campo vacio."
        return false
    if data.edit ==  ""
        data.type = "add"
    else
        data.type = "edit"
    data.proyecto = $("input[name=pro]").val()
    data.subproyecto = $("input[name=sub]").val()
    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
    $.post "", data, (response) ->
        if response.status
            location.reload()
    return

showEditComment = ->
    if @getAttribute("data-id") isnt ""
        id = @getAttribute("data-id")
        $("#message_ifr").contents().find("body").html $(".comment#{id}").find("div").eq(2).html()
        $("select[message-status]").val @getAttribute("data-status")
        $("input[name=edit-message]").val id
    return

###listComment = ->
    $.getJSON "", "list":"comment", (response) ->
        if response.status
            template = "
            <div class=\"alert alert-{{ status }} comment{{ id }}\">
                <div>
                    {{!editing}}
                    <small>{{ date }} {{ time }}</small>
                </div>
                <div>
                    {{ message }}
                </div>
                <div>
                    <small class=\"pull-right\">{{ charge }}</small>
                </div>
            </div>"
            edit = "<div class=\"btn-group pull-right\">
                        <button type=\"button\" data-toggle=\"dropdown\" class=\"btn btn-xs btn-link text-black dropdown-toggle\"><span class=\"glyphicon glyphicon-collapse-down\"></span></button>
                        <ul role=\"menu\" class=\"dropdown-menu\">
                            <li><a data-status=\"{{ status }}\" data-id=\"{{ id }}\" class=\"btn-message-edit\">Editar</a></li>
                            <li><a data-status=\"{{ status }}\" data-id=\"{{ id }}\" class=\"btn-message-del\">Eliminar</a></li>
                        </ul>
                    </div>"
            $panel = $("div.comment-list > .panel-body")
            $panel.empty()
            dni = $("input[name=dni]").val()
            html = ""
            for x of response.alerts
                if x.empdni == dni
                    template = template.replace "{{!editing}}", edit
                html = html.concat Mustache.to_html template, response.alerts[x]
            console.log html
            $panel.html html
            return
    return###

toggleComment = ->
    $(".panel-comment").find ".panel-body"
    .toggle ->
        if $(@).is ":hidden"
            $(".btn-show-comment").find "span"
            .removeClass "glyphicon-chevron-up"
            .addClass "glyphicon-chevron-down"
            $(".panel-comment").css "height", "1em"
        else
            $(".btn-show-comment").find "span"
            .removeClass "glyphicon-chevron-down"
            .addClass "glyphicon-chevron-up"
            $(".panel-comment").css "height", "23em"
    return

treeAdminaandOpera = ->
    year = new Date().getFullYear()
    # get year of project

    if $("input[name=sub]").val() == ""
        admin = "/storage/projects/#{year}/#{ $("input[name=pro]").val() }/administrative/"
        opera = "/storage/projects/#{year}/#{ $("input[name=pro]").val() }/operation/"
    else
        admin = "/storage/projects/#{year}/#{ $("input[name=pro]").val() }/#{$("input[name=sub]").val()}/administrative/"
        opera = "/storage/projects/#{year}/#{ $("input[name=pro]").val() }/#{$("input[name=sub]").val()}/operation/"

    fileTree 'filetree_administrative', admin
    fileTree 'filetree_operation', opera
    return

fileTree = (id, path)->
    $("##{ id }").fileTree
        root: path
        script: "/json/get/path/"
        folderEvent: "click"
        expandSpeed: 750
        collapseSpeed: 750
        multiFolder: true
        , (file) ->
            console.log file
            window.open file, "_blank"
    return

setSubproject = (event) ->
    # console.log $(@).attr("data-sub")
    $("input[name=sub]").val($(@).attr("data-sub"))
    if $("input[name=sub]").val() isnt ""
        $(".header-project > .info-sub").remove()
        $(".header-project").append("<p class=\"info-sub\"><strong>Subproyecto :</strong> #{ $(".text-" + $(@).attr("data-sub")).html()} <strong> Codigo :</strong> #{$(@).attr("data-sub")}</p>")
    else
        $("input[name=sub]").val()
        $(".header-project > .info-sub").remove()
    getSectors()
    return

getSectors = ->
    data = new Object()
    data.pro = $("input[name=pro]").val()
    data.sub = $("input[name=sub]").val()
    url = "/sales/projects/sectors/crud/"
    $.getJSON url, data, (response) ->
        if response.status
            if data.sub == ""
                data.sub = "None"
            template = "<article>
                        {{!editable}}
                        <a href=\"/sales/projects/manager/sector/#{data.pro}/#{data.sub}/{{ sector_id }}/\" class=\"text-black\">
                            {{ sector_id }}
                            {{ nomsec }}
                            <small>{{ planoid }}</small>
                        </a>
                        </article>"
            edit = "<button class=\"btn btn-xs text-black btn-link pull-left btn-edit-sector\" value=\"{{ sector_id }}\">
                            <span class=\"glyphicon glyphicon-pencil\"></span>
                                        </button>
                        <button class=\"btn btn-xs text-black btn-link pull-right\" value=\"{{ sector_id }}\">
                            <span class=\"glyphicon glyphicon-trash\"></span>
                                        </button>"
            editable = $("input[name=status-project]").val()
            if editable isnt 'AC'
                template = template.replace "{{!editable}}", edit

            templist = "<li><a href=\"/sales/projects/manager/sector/#{data.pro}/#{data.sub}/{{ sector_id }}/\" class=\"text-black\"><span class=\"glyphicon glyphicon-chevron-right\"></span> {{ nomsec }}</a></li>"
            $list = if data['sub'] is "" then $(".sectorsdefault") else $(".sectors#{data['sub']}")
            # console.log $list
            $sec = $(".all-sectors")
            $sec.empty()
            $list.empty()
            for x of response.list
                $sec.append Mustache.render template, response.list[x]
                $list.append Mustache.render templist, response.list[x]

            equalheight ".all-sectors article"
            return
        else
            $().toastmessage "showErrorToast", "Error, transaction not complete. #{response.raise}"
    return

openNewSector = (event) ->
    pro = $("input[name=pro]").val()
    sub = $("input[name=sub]").val()
    url = "/sales/projects/sectors/crud/?pro=#{pro}&sub=#{sub}&type=new"
    openWindow(url, false)
    return

openUpdateSector = (event) ->
    pro = $("input[name=pro]").val()
    sub = $("input[name=sub]").val()
    sec = @value
    url = "/sales/projects/sectors/crud/?pro=#{pro}&sub=#{sub}&sec=#{sec}&type=update"
    openWindow(url, false)
    return

openNewSubproyecto = (event) ->
    pro = $("input[name=pro]").val()
    url = "/sales/projects/subprojects/crud/?pro=#{pro}&type=new"
    openWindow(url, true)
    return

openUpdateSubproject = (event) ->
    pro = $("input[name=pro]").val()
    sub = @value
    url = "/sales/projects/subprojects/crud/?pro=#{pro}&sub=#{sub}&type=update"
    openWindow(url, true)
    return

openWindow = (url, reload) ->
    win = window.open url, "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600"
    interval = window.setInterval ->
        if win == null or win.closed
            window.clearInterval interval
            if reload
                location.reload()
            else
                getSectors()
            return
    , 1000
    return win;

changeView = (percent) ->
    $(".all-sectors > article").css
        "width" : "#{percent}%"
    equalheight ".all-sectors article"
    return

uploadFiles = (event) ->
    data = new FormData()
    $("input[name=administrative], input[name=operation]").each (index, element) ->
        # valid inputs files is null
        # console.log @files[0]
        if @files[0]?
            data.append @name, @files[0]
            return

    data.append "csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val()
    data.append "type", "files"
    data.append "pro", $("input[name=pro]").val()
    data.append "sub", $("input[name=sub]").val()
    # console.log data
    $.ajax
        data : data,
        url : "",
        type : "POST",
        dataType : "json",
        cache : false,
        processData: false,
        contentType: false,
        success : (response) ->
            # console.log response
            if response.status
                location.reload()
            else
                $().toastmessage "showErrorToast", "Error al subir los archivos al servidor"
    return

deleteSubproject = ->
    del = @
    $().toastmessage "showToast",
        text : "Debe tener en cuenta que al eliminar el Subproyecto (Adicional) este eliminara todos los sectores y materiales que contenga. Desea Eliminar el subproyecto (Adicional)?"
        sticky : true
        type : "confirm"
        buttons : [{value:"Si"}, {value:"No"}]
        success : (result) ->
            if result is "Si"
                data = new Object()
                data.delsub = true
                data.sub = del.value
                data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
                $.post "", data, (response) ->
                    if response.status
                        $().toastmessage "showNoticeToast", "Se a eliminado correctamente."
                        setTimeout ->
                            location.reload()
                        , 2600
                    else
                        $().toastmessage "showErrorToast", "No se a podido eliminar el Subproyecto. #{response.raise}"
                , "json"
            return

    return

calAmountPurchaseOrder = ->
    amount = 0
    $(".table-details-purchase-order > tbody > tr").each (index, element) ->
        $td = $(element).find("td")
        amount += convertNumber $td.eq(6).text()
    $(".pos").text(amount)
    # amount = parseFloat($(".pos").text())
    if isNaN(amount)
        amount = 0
    pdsct = parseFloat $("input[name=poids]").val()
    dsct = ((amount * pdsct) / 100)
    amount = (amount - dsct)
    pigv = $(".povigv").text().split "%"
    pigv = parseInt pigv[0]
    igv = ((amount * pigv) / 100)
    total = (amount + igv)
    dsct = dsct.toFixed 2
    igv = igv.toFixed 2
    total = total.toFixed 2
    $(".pod").text dsct
    $(".poi").text igv
    $(".pot").text total
    getAmountLiteral()
    return

addDetailsPurchase = (event) ->
    data = new Object
    data.desc = $.trim($("input[name=podd").val())
    data.unit = $("select[name=podu]").find("option:selected").text()
    data.date = $("input[name=podf]").val()
    data.quantity = convertNumber $("input[name=podq]").val()
    data.price = convertNumber $("input[name=podp]").val()
    data.amount = data.quantity * data.price
    if data.desc isnt "" and not isNaN(data.price) and not isNaN(data.quantity)
        if $.trim($("input[name=podedit]").val()) isnt ""
            $td = $("tr.pod#{$.trim($("input[name=podedit]").val())} > td")
            $td.eq(1).text $("input[name=podd").val()
            $td.eq(2).text $("select[name=podu]").val()
            $td.eq(3).text $("input[name=podf]").val()
            $td.eq(4).text $("input[name=podq]").val()
            $td.eq(5).text $("input[name=podp]").val()
            $td.eq(6).text (parseFloat($("input[name=podq]").val()) * parseFloat($("input[name=podp]").val()))
            $("input[name=podedit]").val ""
        else
            $tb = $(".table-details-purchase-order > tbody")
            temp = "<tr class=\"pod{{ item }}\">
                    <td>{{ item }}</td>
                    <td>{{ desc }}</td>
                    <td>{{ unit }}</td>
                    <td>{{ date }}</td>
                    <td>{{ quantity }}</td>
                    <td>{{ price }}</td>
                    <td>{{ amount }}</td>
                    <td class=\"text-center\">
                        <button class=\"btn btn-link btn-xs text-primary btn-edit-pod\" value=\"{{ item }}\">
                            <span class=\"glyphicon glyphicon-edit\"></span>
                        </button>
                    </td>
                    <td class=\"text-center\">
                        <button class=\"btn btn-link btn-xs text-red btn-del-pod\" value=\"{{ item }}\">
                            <span class=\"glyphicon glyphicon-trash\"></span>
                        </button>
                    </td>
                    </tr>"
            data.item = $tb.find("tr").length + 1
            $tb.append Mustache.render temp, data
        calAmountPurchaseOrder()
        $(".btn-details-purchare-order-toggle").click()
    else
        $().toastmessage "showWarningToast", "Existen campos vacios!"
    return

getPercentIVA = (event) ->
    data = new Object
    data.percentigv = true
    date = $.trim $("input[name=podt]").val()
    if date isnt ""
        data.year = new Date("#{date} 00:00").getFullYear()

    $.getJSON "/json/general/conf/igv/", data, (response) ->
        if response.status
            $(".povigv").text "#{response.igv}%"
            return
    return

getAmountLiteral = (event) ->
    data = new Object
    data.number = $(".pot").text()
    $.getJSON "/json/convert/number/to/literal/", data, (response) ->
        if response.status
            $(".literal-amount").text "SON: #{response.literal} /100 #{$("select[name=pocu]").find("option:selected").text()}"
            return
    return

showEditDetailsPurchase = (event) ->
    $("input[name=podedit]").val @value
    $td = $("tr.pod#{@value} > td")
    $("input[name=podd").val($td.eq(1).text())
    $("select[name=podu]").val($td.eq(2).text())
    $("input[name=podf]").val($td.eq(3).text())
    $("input[name=podq]").val($td.eq(4).text())
    $("input[name=podp]").val($td.eq(5).text())
    $(".btn-details-purchare-order-toggle").click()
    return

deleteDetailsPurchase = (event) ->
    $tr = $("tr.pod#{@value}")
    $tr.remove()
    $(".table-details-purchase-order > tbody > tr").each (index, element) ->
        $td = $(element).find "td"
        $td.eq(0).text index + 1
        $td.eq(7).find("button").val index + 1
        $td.eq(8).find("button").val index + 1
        return
    calAmountPurchaseOrder()
    return

savePurchaseOrder = (event) ->
    data = new FormData
    data.append "savedPurchase", true
    data.append "nropurchase", $.trim $("input[name=pond]").val()
    data.append "issued", $.trim($("input[name=podt]").val())
    data.append "currency", $("select[name=pocu]").val()
    data.append "document", $("select[name=podc]").val()
    data.append "method", $("select[name=popy]").val()
    if $("input.upfile").get(0).files.length
        data.append "order", $("input.upfile").get(0).files[0]
    data.append "observation", $("textarea[name=obser]").val()
    data.append "dsct", parseFloat $("input[name=poids]").val()
    data.append "igv", parseFloat $(".povigv").text().split("%")[0]
    if $.trim($("input[name=editpurchse]").val()) isnt ""
        data.append "editpurchse", $.trim($("input[name=editpurchse]").val())
    details = new Array
    $(".table-details-purchase-order > tbody > tr").each (index, element) ->
        $td = $(element).find "td"
        details.push
            "description": $td.eq(1).text()
            "unit": $td.eq(2).text()
            "date": $td.eq(3).text()
            "quantity": parseFloat $td.eq(4).text()
            "price": parseFloat $td.eq(5).text()
        return
    data.append "details", JSON.stringify details
    data.append "csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val()
    $.ajax
        url: ""
        data: data
        type: "POST"
        dataType: "json"
        cache : false
        processData: false
        contentType: false
        success: (response) ->
            if response.status
                getListPurchaseOrder()
                $("input[name=editpurchse]").val("")
                $("div.mpurchase").modal "hide"
            else
                $().toastmessage "showWarningToast", "No se a podido Guardar la Orden de compra. #{response.raise}"
    return

getListPurchaseOrder = (event) ->
    data = new Object
    data.listPurchase = true
    $.getJSON "", data, (response) ->
        if response.status
            template = "<tr>
                        <td>{{ item }}</td>
                        <td>{{ nro }}</td>
                        <td>{{ issued }}</td>
                        <td>{{ document }}</td>
                        <td class=\"text-center\">{{!file}}</td>
                        <td class=\"text-center\">
                            <button class=\"btn btn-link btn-xs text-primary btn-edit-purchase\" value=\"{{ id }}\">
                                <span class=\"glyphicon glyphicon-edit\"></span>
                            </button>
                        </td>
                        <td class=\"text-center\">
                            <button class=\"btn btn-link btn-xs text-red btn-del-purchase\" value=\"{{ id }}\">
                                <span class=\"glyphicon glyphicon-trash\"></span>
                            </button>
                        </td>
                        </tr>"
            $tb = $("table.tpurchase > tbody")
            $tb.empty()
            for x of response.list
                if response.list[x].order isnt ""
                    temp = template.replace "{{!file}}","<a href=\"/media/{{ order }}\" target=\"_blank\"><span class=\"glyphicon glyphicon-file\"></span></a>"
                else
                    temp = template
                response.item = (parseInt(x) + 1)
                $tb.append Mustache.render temp, response.list[x]
            return
        else
            $().toastmessage "showWarningToast", "Error list ordenes de compra. #{response.raise}"
    return

getEditPurchase = (event) ->
    $("input[name=editpurchse]").val @value
    data = new Object
    data.editPurchase = true
    data.pk = @value
    $.getJSON "", data, (response) ->
        if  response.status
            $("input[name=pond]").val(response.nropurchase)
            $("input[name=podt]").val(response.issued)
            $("select[name=pocu]").val(response.currency)
            $("select[name=podc]").val(response.document)
            $("select[name=popy]").val(response.method)
            $("textarea[name=obser]").val(response.observation)
            $("input[name=poids]").val(response.dsct)
            $(".povigv").text("#{response.igv}%")

            $tb = $(".table-details-purchase-order > tbody")
            template = "<tr class=\"pod{{ item }}\">
                    <td>{{ item }}</td>
                    <td>{{ description }}</td>
                    <td>{{ unit }}</td>
                    <td>{{ delivery }}</td>
                    <td>{{ quantity }}</td>
                    <td>{{ price }}</td>
                    <td>{{ amount }}</td>
                    <td class=\"text-center\">
                        <button class=\"btn btn-link btn-xs text-primary btn-edit-pod\" value=\"{{ item }}\">
                            <span class=\"glyphicon glyphicon-edit\"></span>
                        </button>
                    </td>
                    <td class=\"text-center\">
                        <button class=\"btn btn-link btn-xs text-red btn-del-pod\" value=\"{{ item }}\">
                            <span class=\"glyphicon glyphicon-trash\"></span>
                        </button>
                    </td>
                    </tr>"
            $tb.empty()
            for x of response.details
                response.details[x].item = (parseInt(x) + 1)
                $tb.append Mustache.render template, response.details[x]
            calAmountPurchaseOrder()
            $("div.mpurchase").modal "show"
            return
        else
            $().toastmessage "showWarningToast", "No se recupero los datos."
            return
    return

deleteOrderPurchase = (event) ->
    val = @value
    $().toastmessage "showToast",
        text: "Realmente desea eliminar la Orden de Compra?"
        type: "confirm"
        sticky: true
        buttons: [{value:"Si"},{value:"No"}]
        success: (result) ->
            if result is "Si"
                data = new Object
                data.deletePurchase = true
                data.pk = val
                data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
                $.post "", data, (response) ->
                    if response.status
                        getListPurchaseOrder()
                        return
                    else
                        $().toastmessage "showErrorToast", "No se a eliminado la Orden de Compra"
                        return
                , "json"
                return
    return

genKeyConfirmationResponsible = (event) ->
    data = new Object
    $pro = $("input[name=pro]")
    data.genKeyConf = true
    data.email = $("input[name=user-email]").val()
    data.code = $pro.val()
    data.desc = 'responsible'
    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
    $.post "/json/post/key/confirm/", data, (response) ->
        if response.status
            reason = $("input[name=companyname]").val()
            data = new Object
            data.forsb = $("input[name=user-email]").val()
            data.issue = "Código de confirmación"
            data.body = "<p><span style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\" data-mce-style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\">Tu código de confirmación para asignar al responsable es: <strong>#{response.key}</strong>. Ingresa este código en la casilla de verificacion para continuar.</span></p><p>Generado:&nbsp; #{$("input[name=user-email]").attr "data-name"}</p><p>Proyecto:&nbsp; <strong>\"#{$pro.attr "data-name"}\"</strong></p><p>Ejecutado por:&nbsp; <strong>\"#{reason}\"</strong></p><p>Fecha y hora: #{new Date().toString()}</p><p><span data-mce-style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\" style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\">Si no has realizado esta operación o tienes cualquier duda respecto código, puedes comunicarte con nosotros 01 371-0443.</span></p>"
            $.ajax
                url: "http://190.41.246.91:3000/mailer/" #url: "http://127.0.0.1:3000/mailer/"
                type: "GET"
                crossDomain: true
                data: $.param data
                dataType: "jsonp",
                success: (response) ->
                    if response.status
                        $().toastmessage "showNoticeToast", "Se a enviado el código de confirmación."
                    else
                        $().toastmessage "showErrorToast", "No se podido enviar el correo."
        else
            $().toastmessage "showErrorToast", "No se generado el token."
    , "json"
    return

genKeyConfirmationApproved = (event) ->
    data = new Object
    $pro = $("input[name=pro]")
    data.genKeyConf = true
    data.code = $pro.val()
    data.desc = "approved"
    data.email = $("input[name=user-email]").val()
    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
    $.post "/json/post/key/confirm/", data, (response) ->
        if response.status
            reason = $("input[name=companyname]").val()
            data = new Object
            data.forsb = $("input[name=user-email]").val()
            data.issue = "Código de confirmación"
            data.body = "<p><span style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\" data-mce-style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\">Tu código de confirmación para Aprobar el Proyecto es: <strong>#{response.key}</strong>. Ingresa este código en la casilla de verificacion para continuar.</span></p><p>Generado:&nbsp; #{$("input[name=user-email]").attr "data-name"}</p><p>Proyecto:&nbsp; <strong>\"#{$pro.attr "data-name"}\"</strong></p><p>Ejecutado por:&nbsp; <strong>\"#{reason}\"</strong></p><p>Fecha y hora: #{new Date().toString()}</p><p><span data-mce-style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\" style=\"color: rgb(33, 33, 33); font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 19.7999992370605px;\">Si no has realizado esta operación o tienes cualquier duda respecto código, puedes comunicarte con nosotros 01 371-0443.</span></p>"
            $.ajax
                url: "http://190.41.246.91:3000/mailer/" #url: "http://127.0.0.1:3000/mailer/"
                type: "GET"
                crossDomain: true
                data: $.param data
                dataType: "jsonp",
                success: (response) ->
                    if response.status
                        $().toastmessage "showNoticeToast", "Se a enviado el código de confirmación."
                    else
                        $().toastmessage "showErrorToast", "No se podido enviar el correo."
        else
            $().toastmessage "showErrorToast", "No se generado el token."
    , "json"
    return

showLoadPrices = (event) ->
    $("input[name=fileprices]").click()
    return

uploadLoadPrices = (event) ->
    file = $("input[name=fileprices]").get(0)
    if file.files.length
        form = new FormData()
        form.append "prices", file.files[0]
        form.append "loadPrices", true
        form.append "csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val()
        $.ajax
            url: ""
            data: form
            type: "POST"
            dataType: "json"
            cache: false
            contentType: false
            processData: false
            success: (response) ->
                if response.status
                    $().toastmessage "showNoticeToast", "Se a cargado el archivo correctamente."
                    $("#mlprices").modal "hide"
                else
                    $().toastmessage "showWarningToast", "No se a podido subir el archivo. #{response.raise}"
    else
        $().toastmessage "showWarningToast", "Debe de seleccionar por lo menos un archivo."
    return