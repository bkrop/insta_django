$(document).ready(function () {
    $('.commentBtn').click(function () {
        let serializedData = $(this).closest(".commentForm").serialize();
        let btn = $(this);
        let id = btn.attr('id');
        console.log(serializedData);
        $.ajax({
            url: $(".commentForm").data('url'),
            data: serializedData,
            type: 'post',
            dataType: 'json',
            success: function (data) {
                console.log(data);
                $(`#${id}.commentsSep`).load('/posts/comments/' + data.comment.post);
                $('textarea').val('');
            },
            error: function(textStatus) {
                console.log(textStatus)
            }
        })
    })
})