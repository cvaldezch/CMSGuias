$(document).ready ->
    $(".btn-save, .panel-pro").hide()
    $(".btn-open > span").mouseenter (event) ->
        event.preventDefault()
        $(@).removeClass "glyphicon-folder-close"
        .addClass "glyphicon-folder-open"
        return
    .mouseout (event) ->
        event.preventDefault()
        $(@).removeClass "glyphicon-folder-open"
        .addClass "glyphicon-folder-close"
        return
    tinymce.init
        selector: "textarea[name=obser]",
        theme: "modern",
        menubar: false,
        statusbar: false,
        plugins: "link contextmenu fullscreen",
        fullpage_default_doctype: "<!DOCTYPE html>",
        font_size_style_values : "10px,12px,13px,14px,16px,18px,20px",
        toolbar1: "styleselect | fontsizeselect | fullscreen |"
        toolbar2: "undo redo | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent |"

    setTimeout ->
        $(document).find("#mceu_2").click (event)->
            if $(@).attr("aria-pressed") is "false" or $(@).attr("aria-pressed") is undefined
                $(".navbar").hide()
            else if $(@).attr("aria-pressed") is "true"
                $(".navbar").show()
            return
        return
    , 2000

    $("[name=pais]").on "click", getDepartamentOption
    $("[name=departamento]").on "click", getProvinceOption
    $("[name=provincia]").on "click", getDistrictOption
    $(".btn-country-refresh").on "click", getCountryOption
    $(".btn-departament-refresh").on "click", getDepartamentOption
    $(".btn-province-refresh").on "click", getProvinceOption
    $(".btn-district-refresh").on "click", getDistrictOption
    $(".btn-add").on "click", showaddProject

    return

showaddProject = (event) ->
    event.preventDefault()
    $btn = $(@)
    $(".panel-pro").toggle ->
        if $(@).is(":hidden")
            $btn.find("span").eq(0).removeClass "glyphicon-remove"
            .addClass "glyphicon-plus"
            $btn.find("span").eq(1).html(" Nuevo Proyecto")
            $(".btn-save").hide()
            return
        else
            $btn.find("span").eq(0).removeClass "glyphicon-plus"
            .addClass "glyphicon-remove"
            $btn.find("span").eq(1).html(" Cancelar")
            $(".btn-save").show()
            return

    return