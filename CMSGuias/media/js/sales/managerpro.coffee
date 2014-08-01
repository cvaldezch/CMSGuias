$(document).ready ->
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
    treeAdminaandOpera()
    tinymce.init
        selector: "textarea#message",
        theme: "modern",
        menubar: false,
        statusbar: false,
        plugins: "link contextmenu",
        font_size_style_values : "10px,12px,13px,14px,16px,18px,20px",
        toolbar: "undo redo | styleselect | fontsizeselect |"
    $(".btn-publisher").on "click", publisherCommnet
    return

approvedProject = ->
    data = new Object()
    data.type = "approved"
    data.admin = $("select[name=admin-approve]").val()
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
    admin = $("select[name=admin]").val()
    passwd = $("input[name=passwd]").val()
    if responsible? and admin? and passwd?
        data = new Object()
        data.responsible = responsible
        data.admin = admin
        data.passwd = passwd
        data.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val()
        data.type = 'responsible'
        console.info data
        $.post "", data, (response) ->
            if response.status
                location.reload()
            else
                $().toastmessage "", "Transaccion error: #{response.raise}"
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
    if $("input[name=sub]").val() == ""
        admin = "/storage/projects/#{ $("input[name=pro]").val() }/administrative/"
        opera = "/storage/projects/#{ $("input[name=pro]").val() }/operation/"
    else
        admin = "/storage/projects/#{ $("input[name=pro]").val() }/#{$("input[name=sub]").val()}/administrative/"
        opera = "/storage/projects/#{ $("input[name=pro]").val() }/#{$("input[name=sub]").val()}/operation/"

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
            window.open file, "_blank"
    return
setSubproject = (event) ->
    console.log $(@).attr("data-sub")
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
                        <button class=\"btn btn-xs text-black btn-link pull-left btn-edit-sector\" value=\"{{ sector_id }}\">
                            <span class=\"glyphicon glyphicon-pencil\"></span>
                                        </button>
                        <button class=\"btn btn-xs text-black btn-link pull-right\" value=\"{{ sector_id }}\">
                            <span class=\"glyphicon glyphicon-trash\"></span>
                                        </button>
                        <a href=\"/sales/projects/manager/sector/#{data.pro}/#{data.sub}/{{ sector_id }}/\" class=\"text-black\">
                            {{ sector_id }}
                            {{ nomsec }}
                            <small>{{ planoid }}</small>
                        </a>
                        </article>"
            templist = "<li><a href=\"/sales/projects/manager/sector/#{data.pro}/#{data.sub}/{{ sector_id }}/\" class=\"text-black\"><span class=\"glyphicon glyphicon-chevron-right\"></span> {{ nomsec }}</a></li>"
            $list = if data['sub'] is "" then $(".sectorsdefault") else $(".sectors#{data['sub']}")
            console.log $list
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
    openWindow(url)
    return

openUpdateSector = (event) ->
    pro = $("input[name=pro]").val()
    sub = $("input[name=sub]").val()
    sec = @value
    url = "/sales/projects/sectors/crud/?pro=#{pro}&sub=#{sub}&sec=#{sec}&type=update"
    openWindow(url)
    return

openNewSubproyecto = (event) ->
    pro = $("input[name=pro]").val()
    url = "/sales/projects/subprojects/crud/?pro=#{pro}&type=new"
    openWindow(url)
    return

openUpdateSubproject = (event) ->
    pro = $("input[name=pro]").val()
    sub = @value
    url = "/sales/projects/subprojects/crud/?pro=#{pro}&sub=#{sub}&type=update"
    openWindow(url)
    return

openWindow = (url) ->
    win = window.open url, "Popup", "toolbar=no, scrollbars=yes, resizable=no, width=400, height=600"
    interval = window.setInterval ->
        if win == null or win.closed
            window.clearInterval interval
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
        console.log @files[0]
        if @files[0]?
            data.append @name, @files[0]
            return

    data.append "csrfmiddlewaretoken", $("input[name=csrfmiddlewaretoken]").val()
    data.append "type", "files"
    data.append "pro", $("input[name=pro]").val()
    data.append "sub", $("input[name=sub]").val()
    console.log data
    $.ajax
        data : data,
        url : "",
        type : "POST",
        dataType : "json",
        cache : false,
        processData: false,
        contentType: false,
        success : (response) ->
            console.log response
            if response.status
                location.reload()
            else
                $().toastmessage "showErrorToast", "Error al subir los archivos al servidor"
    return