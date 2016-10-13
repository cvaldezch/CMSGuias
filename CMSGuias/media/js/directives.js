var valMinandMax;

valMinandMax = function() {
  return {
    restrict: 'AE',
    require: '?ngModel',
    scope: '@',
    link: function(scope, element, attrs, ngModel) {
      element.bind('blur', function(event) {
        var max, min, result, valid, vcurrent;
        console.log("inside event");
        result = 0;
        valid = true;
        vcurrent = element.val();
        if (vcurrent === '' || vcurrent === void 0) {
          valid = false;
        }
        console.log(valid, vcurrent);
        if (valid) {
          vcurrent = parseFloat(vcurrent);
          min = parseFloat(attrs.min);
          max = parseFloat(attrs.max);
          switch (false) {
            case !(vcurrent > max):
              result = max;
              break;
            case !(vcurrent < min):
              result = min;
              break;
            default:
              result = vcurrent;
          }
          if (attrs.hasOwnProperty('ngModel')) {
            ngModel.$setViewValue(result);
            ngModel.$render();
            scope.$apply();
            console.log("change model");
          } else {
            element.val(result);
            console.log("change attr");
          }
        } else {
          if (attrs.hasOwnProperty('ngModel')) {
            ngModel.$setViewValue(result);
            ngModel.$render();
            scope.$apply();
            console.log("change model");
          } else {
            element.val(result);
            console.log("change attr");
          }
        }
      });
    }
  };
};
