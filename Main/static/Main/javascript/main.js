$(document).ready(function(){
      
    if($(window).width()>1000)
    {
        $("#data01").html("<p class=\"text-center\">Male");
        $("#data02").html("<p class=\"text-center\">Female");
        $("#data03").html("<p class=\"text-center\">Other");
        $("#data04").html("<p class=\"text-center\">Total");
        $("#data10").html("<p>Members at the beginning of "+month+" <b style=\"color:red\"> *</b>");
        $("#data20").html("<p>Members Added<b style=\"color:red\"> *</b>");
        $("#data30").html("<p>Members Left<b style=\"color:red\"> *</b>");
        $("#data40").html("<p>Prospective<b style=\"color:red\"> *</b>");
        $("#data50").html("<p>Guests (RYE /NGSE /Family)<b style=\"color:red\"> *</b>");
        $("#data60").html("<p>Total");
    }

    $("#reportButton00,#reportButton10,#reportButton20").html("Prev");
    // $("#member1Del,#gbm1Del,#bod1Del,#futureEvent1Del,#event1Del").attr('disabled', true);

});

function AutoFill() {
    var now = new Date();
    var day = ("0" + now.getDate()).slice(-2);
    var month = ("0" + (now.getMonth() + 1)).slice(-2);
    var today1 = now.getFullYear()+"-"+(month)+"-"+(day) ;   
    var today2 = now.getFullYear()+"-"+(month) ;   
    $("input[type=date]").val(today1); 
    $("input[type=text]").val("0"); 
    $("input[type=number]").val(0); 
    $("select").prop('selectedIndex', 0);
    $("#bar").css('width','100%'); 
    $("#reportButton21").attr('disabled', false);  
}