var animateAdd, goToElement, goTopPage;

goTopPage = function(event) {
  $("html, body").animate({
    scrollTop: 0
  }, "slow");
};

goToElement = function(event, element) {
  $("html, body").animate({
    scrollTop: $("" + element).eq(0).position().top
  }, 800, "swing");
};

animateAdd = function(event) {
  $(this).hover(function() {

    /*.removeClass "btn-success text-black"
    .addClass "btn-default"
     */
    $(this).find("span").eq(0).removeClass("fa-plus-square-0").addClass("fa-plus");

    /*$(@).find "span"
    .eq 1
    .text tfirst
     */
  }, function() {

    /*removeClass "btn-default"
    .addClass "btn-success text-black"
     */
    $(this).find("span").eq(0).removeClass("fa-plus").addClass("fa-plus-square-0");

    /*$(@).find "span"
    .eq 1
    .text tlast
     */
  });
};
