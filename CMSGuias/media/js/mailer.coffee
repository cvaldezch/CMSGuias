initializeBodyMailer = (event) ->
    $("select[name=globalmfor]").chosen
        width: "100%",
        element: "select[name=globalmfor]"
    $("select[name=globalmcc]").chosen
        width: "100%",
        element: "select[name=globalmcc]"
    $("select[name=globalmcco]").chosen
        width: "100%",
        element: "select[name=globalmcco]"
    tinymce.init
            selector: "div[name=globalmbody]",
            height: 200,
            theme: "modern",
            menubar: true,
            statusbar: false,
            paste_as_text: true,
            plugins: "link contextmenu",
            #contextmenu: "paste | code"
            font_size_style_values : "10px,12px,13px,14px,16px,18px,20px",
            toolbar: "undo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | fontsizeselect"
    return

showGlobalEnvelop = (event) ->
    if not $("#mailer").length
        $("footer").append globalTmpMailer
        initializeBodyMailer()
    if $("#mailer").is(":hidden")
        $("#mailer").modal "show"
        if globalMailerData.hasOwnProperty "issue"
            $("input[name=globalmissue]").val globalMailerData.issue.toString()
        else
            $("input[name=globalmissue]").val ""

        if globalMailerData.hasOwnProperty "body"
            #$("input[name=globalmbody]").html globalMailerData.body
            $("iframe#globalmbody_ifr").contents().find("body").html globalMailerData.body
        else
            $("iframe#globalmbody_ifr").contents().find("body").html ""
        if $("select[name=globalmfor]").find("option").length == 0
            getAllCurrentAccounts()
            setTimeout ->
                if globalMailerData.hasOwnProperty("fors")
                    $item = $("select[name=globalmfor]")
                    tmp = "<option value=\"{{ email }}\">{{ email }}</option>"
                    for x in globalMailerData.fors
                        $item.append "<option value=\"#{x}\" selected>#{x}</option>"
                    $item.trigger("chosen:updated")
                    items = ["cc", "cco"]
                    for c in items
                        $item = $("select[name=globalm#{c}]")
                        tmp = "<option value=\"{{ email }}\">{{ email }}</option>"
                        for x in globalMailerData.fors
                            $item.append "<option value=\"#{x}\">#{x}</option>"
                        $item.trigger("chosen:updated")
                    return
            , 200
    else
        $("#mailer").modal "hide"
    return

getAllCurrentAccounts = (event) ->
    data = new Object
    data.allmails = true
    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
    $.post "/json/get/emails/", data, (response) ->
        if response.status
           globalMailerData.fors = response.for
    , "json"
    return

globalMailerData = new Object

mailerLoadsData = ->
    if globalMailerData.hasOwnProperty "fors"
        $("input[name=globalmfor]").val globalMailerData.fors.toString().replace /\,/g, ", "
    else
        $("input[name=globalmfor]").val ""

    if globalMailerData.hasOwnProperty "cc"
        $("input[name=globalmcc]").val globalMailerData.cc.toString().replace /\,/g, ", "
    else
        $("input[name=globalmcc]").val ""

    if globalMailerData.hasOwnProperty "cco"
        $("input[name=globalmcco]").val globalMailerData.cco.toString().replace /\,/g, ", "
    else
        $("input[name=globalmcco]").val ""

    if globalMailerData.hasOwnProperty "issue"
        $("input[name=globalmissue]").val globalMailerData.issue.toString()
    else
        $("input[name=globalmissue]").val ""

    if globalMailerData.hasOwnProperty "body"
        #$("input[name=globalmbody]").html globalMailerData.body
        $("iframe#globalmbody_ifr").contents().find("body").html globalMailerData.body
    else
        $("iframe#globalmbody_ifr").contents().find("body").html ""
    return

globalTmpMailer = "
<div class=\"modal fade\" id=\"mailer\">
    <div class=\"modal-dialog\">
        <div class=\"modal-content\">
            <div class=\"modal-body mailer-one\">
                <a data-dismiss=\"modal\" class=\"close\">&times;</a>
                <div class=\"row\">
                    <div class=\"col-md-12\">
                        <div class=\"form-group\">
                            <select name=\"globalmfor\" class=\"chosen-select text-bold globalmfor\" data-placeholder=\"Para\" multiple>

                                </select>
                            <button class=\"btn btn-link close btn-global-copy-mailer\">
                                <span class=\"fa fa-chevron-down\"></span>
                            </button>
                        </div>
                    </div>
                    <div class=\"col-md-12\">
                        <div class=\"form-group panel-copy-mailer hide\">
                            <select name=\"globalmcc\" class=\"chosen-select globalmcc\" data-placeholder=\"Cc\" multiple>
                            </select>
                            <select name=\"globalmcco\" class=\"chosen-select globalmcco\" data-placeholder=\"Cco\" multiple>
                            </select>
                        </div>
                    </div>
                    <div class=\"col-md-12\">
                        <div class=\"form-group\">
                            <input type=\"text\" name=\"globalmissue\" class=\"form-control input-sm text-bold\"  placeholder=\"Asunto\"/ >
                        </div>
                    </div>
                    <div class=\"col-md-12\">
                        <div id=\"globalmbody\" name=\"globalmbody\">
                            Escribe algo ...
                        </div>
                    </div>
                    <div class=\"col-md-12\">
                        <div class=\"row\">
                            <div class=\"col-md-2\">
                                <button class=\"btn btn-primary btn-global-send-envelop\">
                                    <span class=\"fa fa-envelope\"></span>
                                    ENVIAR
                                </button>
                            </div>
                            <div class=\"col-md-4 col-md-offset-6\">
                                <div class=\"input-group\">
                                    <div class=\"input-group-btn\">
                                        <button class=\"btn btn-sm btn-default btn-global-show-mailer-password\">
                                            <span class=\"fa fa-chevron-circle-down\"></span>
                                        </button>
                                    </div>
                                    <div class=\"form-group has-primary\">
                                        <input type=\"password\" class=\"form-control input-sm hide\" name=\"globalPwdMailer\">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class=\"modal-body mailer-two hide\">
                <h2 name=\"mailer-msg\" class=\"text-center\">
                    <span class=\"glyphicon\"></span> <br />
                    <span></span>
                </h2>
            </div>
        </div>
    </div>
</div>
"

showGPwdMailer = (event) ->
    $btn = $(@)
    $in = $("input[name=globalPwdMailer]")
    if $in.is(":visible")
        $btn.find "span"
        .removeClass "fa-chevron-circle-right"
        .addClass "fa-chevron-circle-down"
        $in.addClass "hide"
    else
        $btn.find "span"
        .removeClass "fa-chevron-circle-down"
        .addClass "fa-chevron-circle-right"
        $in.removeClass "hide"
    return

showGCopyMailer = (event) ->
    $btn = $(@)
    $panel = $(".panel-copy-mailer")
    if $panel.is(":visible")
        $btn.find "span"
        .removeClass "fa-chevron-up"
        .addClass "fa-chevron-down"
        $panel.addClass "hide"
    else
        $btn.find "span"
        .removeClass "fa-chevron-down"
        .addClass "fa-chevron-up"
        $panel.removeClass "hide"
    return

sendGlobalMailer = (event) ->
    data = new Object
    if $.trim($("select[name=globalmfor]").val()) isnt ""
        data.fors = $("select[name=globalmfor]").val().toString().split ","
        #.split ","
    if $.trim($("select[name=globalmcc]").val()) isnt ""
        data.cc = $("select[name=globalmcc]").val().toString().split ","
        #.split ","
    if $.trim($("select[name=globalmcco]").val()) isnt ""
        data.cco = $("select[name=globalmcco]").val().toString().split ","
        #.split ","
    if $.trim($("input[name=globalmissue]").val()) isnt ""
        data.issue = $("input[name=globalmissue]").val()
    data.body = $("iframe#globalmbody_ifr").contents().find("body").html()
    # validated
    if not data.hasOwnProperty("fors")
        if data.fors.length
            $().toastmessage "showWarningToast", "No se a introducido un destinatario."
            return false
    if not data.hasOwnProperty("issue")
        if data.issue.length
            $().toastmessage "showWarningToast", "No se a introducido un destinatario."
            return false
    if not data.hasOwnProperty("body") or data.body is ""
        $().toastmessage "showWarningToast", "No se a introducido un destinatario."
        return false
    for x in data.fors
        if $.trim(data.fors[x]) isnt ""
            pass = validateEmail data.fors[x]
            if not pass
                $().toastmessage "showWarningToast", "El formato de email no es correcto."
                return pass
    if data.hasOwnProperty("cc")
        if data.cc.length
            data.ccb = data.cc.toString()
            for x in data.cc
                if $.trim(data.cc[x]) isnt ""
                    pass = validateEmail data.cc[x]
                    if not pass
                        return pass
    if data.hasOwnProperty("cco")
        if data.cco.length
            data.ccob = data.cco.toString()
            for x in data.cco
                if $.trim(data.cco[x]) isnt ""
                    pass = validateEmail data.cco[x]
                    if not pass
                        return pass
    data.forsb = data.fors.toString()
    if $("input[name=globalPwdMailer]").is(":visible")
        if $.trim($("input[name=globalPwdMailer]").val()) isnt ""
            data.name = $("input[name=user-email]").attr "data-name"
            data.email = $("input[name=user-email]").val()
            data.pwdmailer = $("input[name=globalPwdMailer]").val()

    $.ajax
        url: "http://190.41.246.91:3000/mailer/" #url: "http://127.0.0.1:3000/mailer/"
        type: "GET"
        crossDomain: true
        data: $.param data
        dataType: "jsonp",
        success: (response) ->
            if response.status
                if response.status
                    $("div.mailer-one").addClass "hide"
                    $("div.mailer-two").removeClass "hide"
                    $("[name=mailer-msg]").addClass "text-success"
                    $("[name=mailer-msg]").find "span"
                    .eq 0
                    .addClass "glyphicon-ok"
                    $("[name=mailer-msg]").find "span"
                    .eq 1
                    .text "Felicidades, se a enviado el correo."
                    setTimeout ->
                        $(".mailer-two").addClass "hide"
                        $(".mailer-one").removeClass "hide"
                        location.reload()
                    , 1600
                else if not response.status
                    $("div.mailer-two").removeClass "hide"
                    $("div.mailer-one").addClass "hide"
                    $("[name=mailer-msg]").addClass "text-danger"
                    $("[name=mailer-msg]").find "span"
                    .eq 0
                    .addClass "glyphicon-remove"
                    $("[name=mailer-msg]").find "span"
                    .eq 1
                    .text "Error al guardar el email"
                    .append "<small>Es posible que el correo se envie mas tarde.</small>"
                    setTimeout ->
                        $(".mailer-two").addClass "hide"
                        $(".mailer-one").removeClass "hide"
                        $("#mailer").modal "hide"
                    , 1600

    data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
    data.saveEmail = true
    $.post "/json/emails/", data, (response) ->
        if response.status
            if $("[name=mailer-enable]").length
                $("[name=mailer-enable]").get(0).checked = false
            $().toastmessage "showNoticeToast", "Email save BBDD"
    , "json"
    return

searchChosenKey = (event) ->
    key = event.keycode or event.which
    if key is 188 or key is 13
        add = $.trim(@value).replace ",",""
        if validateEmail add
            $("select[name=#{@getAttribute "data-element"}]").find "option"
            .each (index, elm) ->
                if elm.text is add
                    return false
            option = "<option value=\"#{add}\">#{add}</option>"
            $("select[name=#{@getAttribute "data-element"}]").append option
            .trigger("chosen:updated")
            @value = add
            $(@)
            .trigger jQuery.Event "keyup", which: 190
            .trigger jQuery.Event "keyup", which: 13
        else
            @value = ""
    return

$(document).on "click", ".btn-global-show-mailer-password", showGPwdMailer
$(document).on "click", ".btn-global-copy-mailer", showGCopyMailer
$(document).on "click", ".btn-global-send-envelop",  sendGlobalMailer
$(document).on "keyup", "input[name=seglobalmfor], input[name=seglobalmcc], input[name=seglobalmcco]", searchChosenKey