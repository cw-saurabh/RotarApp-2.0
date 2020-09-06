function updateProgress() {

    let filledCount = 0;
    let totalCount = 0;
    
    $("input").not("input[readonly]").each(function() {
        totalCount += 1;
        var element = $(this);
        if (element.val() != "") {
            filledCount += 1;
        }
    });
    $("select").each(function() {
        totalCount += 1;
        var element = $(this);
        if (element.val() != null) {
            filledCount += 1;
        }
    });
    
    let progress = parseInt(filledCount/totalCount*100);
    $("#bar").css('width',progress.toString()+'%');
    
    
}
