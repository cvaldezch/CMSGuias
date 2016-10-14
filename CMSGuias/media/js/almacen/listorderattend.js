var app = angular.module("appAO", []);
app.config(function ($httpProvider) {
            $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        });
app.controller('CtrlAO', ['$scope','$http', function($scope, $http){
    $scope.orders = [];
    $scope.area = '';
    $scope.cargo = '';
    angular.element(document).ready(function () {
        angular.element(".table-float").floatThead({
            useAbsolutePositioning: false,
            scrollingTop: 50
        });
        var data = {glist: true}
        $http.get("", {params: data}).success(function (response){
            console.log(response);
            if (response.status) {
                $scope.orders = response.list;
                angular.element(".table-float").floatThead('reflow');
            }else{
                swal("Alerta!", "No hay datos para mostrar.", "warning");
            };
        console.log($scope.area);
        });
    });
    $scope.cancelOrder = function ($event) {
        swal({
            title: "Realmente desea anular el pedido?",
            text: "",
            type: "warning",
            showCancelButton: true,
            confirmButtonText: 'Si!, anular',
            confirmButtonColor: "#d9534f",
            closeOnConfirm: true,
            closeOnCancel: true
        }, function(isConfirm){
            if (isConfirm){
                var id = $event.currentTarget.dataset.order;
                data = {"csrfmiddlewaretoken": $("[name=csrfmiddlewaretoken]").val(), "oid": id }
                $.post('/json/post/cancel/orders/', data, function(response) {
                    if (response.status) {
                        location.reload()
                    }else{
                        $().toastmessage("showWarningToast","No se a podido anular el pedido. "+response.raise);
                    };
                });
            }
        });
    };
}]);