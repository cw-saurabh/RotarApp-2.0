$(document).ready(function(){
    $('.sidenav').sidenav();
    var mq = window.matchMedia("(max-width: 1000px)");
    if (mq.matches) {
        $('.slider').slider(
        {
                'height': 300,
                "indicators": true,
                "duration": 50
        });
    }
    else {
        $('.slider').slider(
        {
                'height':700,
                "indicators" : true,
                "duration" : 50
        });
    }
    var mq = window.matchMedia( "(max-width: 1000px)" );
    if (mq.matches) {
      $('.row').removeClass('flex');
    }

});

$(window).on('load', function () {
    $("#body").removeClass("hideAll");
});