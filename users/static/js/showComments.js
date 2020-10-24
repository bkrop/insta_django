$(document).ready(function () {
    $(".showComments").click(function () {
        let btn = $(this);
        let id = $(this).attr('id');
        let div = $(`#${id}.comments`);
        
        console.log(div)
        div.toggle();
    });
});