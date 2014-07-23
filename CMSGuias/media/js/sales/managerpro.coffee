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
        console.log response
        if response.status
            template = "<article>
                        <button class=\"btn btn-xs text-black btn-link pull-left btn-edit-sector\" value=\"{{ sector_id }}\">
                            <span class=\"glyphicon glyphicon-pencil\"></span>
                                        </button>
                        <button class=\"btn btn-xs text-black btn-link pull-right\" value=\"{{ sector_id }}\">
                            <span class=\"glyphicon glyphicon-trash\"></span>
                                        </button>
                        <a href=\"\" class=\"text-black\">
                            {{ sector_id }}
                            {{ nomsec }}
                            <small>{{ planoid }}</small>
                        </a>
                        </article>"
            templist = "<li><a href=\"\" class=\"text-black\"><span class=\"glyphicon glyphicon-chevron-right\"></span> {{ nomsec }}</a></li>"
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