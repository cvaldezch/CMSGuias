$(document).ready ->
    $(".panel-new").hide()
    $("button.btn-top-page").on "click", goTopPage
    $("input[name=searchCode]").on "keyup", searchCode
    $("input[name=searchDesc]").on "keyup", searchDesc
    $(document).on "click", "button[name=btnedit]", showEditMaterials
    $("button.btn-show-new").on "click", showNewMaterials
    $('table').floatThead
        useAbsolutePositioning: false
        scrollingTop: 50
    return

searchCode = (event)->
    key = event.keyCode or event.which
    console.log key
    if key is 13
        data = new Object
        data.searchCode = true
        data.code = $.trim @value
        $.getJSON "", data, (response) ->
            if response.status
                addResultTable response
    return

searchDesc = (event) ->
    data = new Object
    data.searchDesc = true
    data.desc = $.trim @value
    $.getJSON "", data, (response) ->
        if response.status
            addResultTable response
    return

addResultTable = (response) ->
    template = "<tr>
                <td class=\"text-center\">{{ item }}</td>
                <td class=\"text-center\">{{ materials }}</td>
                <td>{{ name }}</td>
                <td>{{ measure }}</td>
                <td class=\"text-center\">{{ unit }}</td>
                <td>{{ finished }}</td>
                <td>{{ area }}</td>
                <td class=\"text-center\">
                    <button value=\"{{ materials }}\" data-des=\"{{ name }}\" data-met=\"{{ measure }}\" data-unit=\"{{ unit }}\" data-acb=\"{{ finished }}\" data-area=\"{{ area }}\" class=\"btn btn-xs btn-link text-black\" name=\"btnedit\">
                        <span class=\"fa fa-edit\"></span>
                    </button>
                </td>
                <td value=\"{{ materials }}\" class=\"text-center\">
                    <button class=\"btn btn-xs btn-link text-red\" name=\"btndel\">
                        <span class=\"fa fa-trash-o\"></span>
                    </button>
                </td>
                </tr>"
    $tb = $("table > tbody")
    $tb.empty()
    for x of response.list
        response.list[x].item = parseInt(x) + 1
        $tb.append Mustache.render template, response.list[x]
    return

showNewMaterials = (event) ->
    $btn = $(@)
    $(".panel-new").toggle "slow", ->
        if @style.display is 'block'
            $btn.removeClass "btn-primary"
            .addClass "btn-default"
            .find "span"
            .eq 0
            .removeClass "fa-plus"
            .addClass "fa-times"
            $btn.find "span"
            .eq 1
            .text "Cancelar"
        else
            $btn.removeClass "btn-default"
            .addClass "btn-primary"
            .find "span"
            .eq 0
            .removeClass "fa-times"
            .addClass "fa-plus"
            $btn.find "span"
            .eq 1
            .text "Numero Material"
            #$('table').floatThead('reflow')
        $('table').floatThead('reflow')
    return

showEditMaterials = (event) ->
    $("input[name=ematnom]").val @getAttribute "data-des"
    $("input[name=ematmed]").val @getAttribute "data-met"
    $("input[name=eunidad]").val @getAttribute "data-unit"
    $("input[name=ematacb]").val @getAttribute "data-acb"
    $("input[name=ematare]").val @getAttribute "data-area"
    $(".meditmat").modal "show"
    return