$(document).ready(function () {
    $(".messageBtn").click(function () {
        var serializedData = $(".messageForm").serialize();
        console.log(serializedData)
        $.ajax({
            url: $("messageForm").data('url'),
            data: serializedData,
            type: 'post',
            dataType: 'json',
            success: function (data) {
                console.log(data);
                $('.messages').load('/users/messages/' + data.message.message_to);
                $('textarea').val('');
            }
        })
    });
});