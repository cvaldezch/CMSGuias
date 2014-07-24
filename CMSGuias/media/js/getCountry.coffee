getCountryOption = ->
    $.getJSON "/json/country/list/", "type":"option", (response) ->
        if response.status
            template = "<option value=\"{{ country_id }}\">{{ country }}</option>"
            $country = $("select[name=pais]")
            $country.empty()
            for x of response.country
                $country.append Mustache.render template, response.country[x]

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

        return
    return