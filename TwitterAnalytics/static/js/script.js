$(document).ready(function() {
    $(".dropdown-menu a").click(function() {
        var language = $(this).attr('id')
        
        $.ajax({    
            url: '/change_language/',
            type: 'GET',
            data: {"lang": language},
            dataType: 'json',
        
            success : function(json) {
               
            },
        
            error : function(xhr, status) {
                console.log('Disculpe, existió un problema al cambiar de idioma');
            },
        })
    })

    $(document).keypress(function(e) {
        if(e.which == 13) {
            e.preventDefault();
            $("#submit-hashtag").click()
        }
    });

   
    $("#btn-per-days-tweets").click(function() {
        if(!$("#days-tweets").hasClass('visible')) {
            $("#days-tweets").addClass('visible')
            $("#hours-tweets").removeClass('visible')
        }
    });

    $("#btn-per-hours-tweets").click(function(){
        if(!$("#hours-tweets").hasClass('visible')) {
            $("#hours-tweets").addClass('visible')
            $("#days-tweets").removeClass('visible')
        }
    });

    $("#btn-per-days-users").click(function(){
        if(!$("#days-users").hasClass('visible')) {
            $("#days-users").addClass('visible')
            $("#hours-users").removeClass('visible')
        }
    });

    $("#btn-per-hours-users").click(function(){
        if(!$("#hours-users").hasClass('visible')) {
            $("#hours-users").addClass('visible')
            $("#days-users").removeClass('visible')
        }
    });
});