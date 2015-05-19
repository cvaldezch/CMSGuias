var getCountryOption, getDepartamentOption, getDistrictOption, getProvinceOption;

getCountryOption = function() {
  $.getJSON("/json/country/list/", {
    "type": "option"
  }, function(response) {
    var $country, template, x;
    if (response.status) {
      template = "<option value=\"{{ country_id }}\">{{ country }}</option>";
      $country = $("select[name=pais]");
      $country.empty();
      for (x in response.country) {
        $country.append(Mustache.render(template, response.country[x]));
      }
    }
  });
};

getDepartamentOption = function() {
  var data;
  data = {
    "type": "option",
    "country": $("[name=pais]").val()
  };
  $.getJSON("/json/departament/list/", data, function(response) {
    var $departament, template, x;
    if (response.status) {
      template = "<option value=\"{{ departament_id }}\">{{ departament }}</option>";
      $departament = $("select[name=departamento]");
      $departament.empty();
      for (x in response.departament) {
        $departament.append(Mustache.render(template, response.departament[x]));
      }
    }
  });
};

getProvinceOption = function() {
  var data;
  data = {
    "type": "option",
    "country": $("select[name=pais]").val(),
    "departament": $("select[name=departamento]").val()
  };
  $.getJSON("/json/province/list/", data, function(response) {
    var $province, template, x;
    if (response.status) {
      template = "<option value=\"{{ province_id }}\">{{ province }}</option>";
      $province = $("select[name=provincia]");
      $province.empty();
      for (x in response.province) {
        $province.append(Mustache.render(template, response.province[x]));
      }
    }
  });
};

getDistrictOption = function() {
  var data;
  data = {
    "type": "option",
    "country": $("select[name=pais]").val(),
    "departament": $("select[name=departamento]").val(),
    "province": $("select[name=provincia]").val()
  };
  $.getJSON("/json/district/list/", data, function(response) {
    var $district, template, x;
    if (response.status) {
      template = "<option value=\"{{ district_id }}\">{{ district }}</option>";
      $district = $("select[name=distrito]");
      $district.empty();
      for (x in response.district) {
        $district.append(Mustache.render(template, response.district[x]));
      }
    }
  });
};

$(function() {
  getCountryOption();
  $("[name=pais]").on("click", getDepartamentOption);
  $("[name=departamento]").on("click", getProvinceOption);
  $("[name=provincia]").on("click", getDistrictOption);
});
