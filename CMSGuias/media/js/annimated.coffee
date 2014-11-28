goTopPage = (event) ->
    $("html, body").animate
        scrollTop: 0
        , "slow"
    return

goToElement = (event, element) ->
    $("html, body").animate
        scrollTop: $("#{element}").eq(0).position().top
        , 800
        , "swing"
    return

animateAdd = (event) ->
    $(@).hover  ->
        ###.removeClass "btn-success text-black"
        .addClass "btn-default"###
        $(@).find "span"
        .eq 0
        .removeClass "fa-plus-square-0"
        .addClass "fa-plus"
        ###$(@).find "span"
        .eq 1
        .text tfirst###
        return
    , ->
        ###removeClass "btn-default"
        .addClass "btn-success text-black"###
        $(@).find "span"
        .eq 0
        .removeClass "fa-plus"
        .addClass "fa-plus-square-0"
        ###$(@).find "span"
        .eq 1
        .text tlast###
        return
    return