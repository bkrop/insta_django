$(document).ready(function () {
    $(".likeBtn").click(function () {
        var serializedData = $(".likeForm").serialize();
        let btn = $(this);
        let url = btn.attr('data-url');
        let id = $(this).attr('id');
        let i = btn.children();
        $.ajax({
            url: url,
            data: serializedData,
            type: 'get',
            dataType: 'json',
            success: function (data) {
                console.log(data);
                console.log(i);
                $(`#${id}.counter`).html(data.counter)
                if (data.like === true) {
                    i.removeClass('far fa-heart');
                    i.addClass('fas fa-heart');
                } else {
                    i.removeClass('fas fa-heart');
                    i.addClass('far fa-heart');
                }
            }
        })
    });
});