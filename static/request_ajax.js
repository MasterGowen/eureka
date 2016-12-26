function getAnswers(bid_pk, viewAnswers){
    $.ajax({
        url: "/answers/" + bid_pk,
        success: viewAnswers
    });
}