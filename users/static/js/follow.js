$(document).ready(function(){
    $(".followBtn").click(function(){
        var serializedData = $(".followForm").serialize();
        let btn = $(this);
        let url = btn.attr('data-url');
        $.ajax({
            url: url,
            data: serializedData,
            type: 'get',
            dataType: 'json',
            success: function(data){
                console.log(data);
                btn.text(data.text)
            }
        })
    });
});