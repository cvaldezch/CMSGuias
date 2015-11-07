getCountryOption = ->
    $.getJSON "/json/country/list/", "type":"option", (response) ->
        if response.status
            template = "<option value=\"{{ country_id }}\">{{ country }}</option>"
            $country = $("select[name=pais]")
            $country.empty()
            for x of response.country
                $country.append Mustache.render template, response.country[x]
            $country.material_select('destroy')
            # $country.attr "data-ng-model", "pais"
        return
    return

getDepartamentOption = ->
    data =
        "type" : "option"
        "country": $("[name=pais]").val()
    $.getJSON "/json/departament/list/", data, (response) ->
        if response.status
            template = "<option value=\"{{ departament_id }}\">{{ departament }}</option>"
            $departament = $("select[name=departamento]")
            $departament.empty()
            for x of response.departament
                $departament.append Mustache.render template, response.departament[x]
            $departament.material_select('destroy')
            # $departament.attr "data-ng-model", "departamento"
        return
    return

getProvinceOption = ->
    data =
        "type" : "option"
        "country": $("select[name=pais]").val()
        "departament": $("select[name=departamento]").val()
    $.getJSON "/json/province/list/", data, (response) ->
        if response.status
            template = "<option value=\"{{ province_id }}\">{{ province }}</option>"
            $province = $("select[name=provincia]")
            $province.empty()
            for x of response.province
                $province.append Mustache.render template, response.province[x]
            $province.material_select('destroy')
            # $province.attr "data-ng-model", "provincia"
        return
    return

getDistrictOption = ->
    data =
        "type" : "option"
        "country": $("select[name=pais]").val()
        "departament": $("select[name=departamento]").val()
        "province": $("select[name=provincia]").val()
    $.getJSON "/json/district/list/", data, (response) ->
        if response.status
            template = "<option value=\"{{ district_id }}\">{{ district }}</option>"
            $district = $("select[name=distrito]")
            $district.empty()
            for x of response.district
                $district.append Mustache.render template, response.district[x]
            $district.material_select('destroy')
            # $district.attr "data-ng-model", "distrito"
        return
    return

$ ->
  getCountryOption()
  $("[name=pais]").on "click", getDepartamentOption
  $("[name=departamento]").on "click", getProvinceOption
  $("[name=provincia]").on "click", getDistrictOption
  return
