$(document).ready(function() {
    $('#id_search_button').click(function(e){
        e.preventDefault();
        
        var text = $('#id_q').val();
        var postal_code = $('#id_postal_code').val();
        $('#loading').show();
        $.ajax({
           type: "POST",
           url: SEARCH_JSON,
           dataType: "json",
           data: {
               'q' : text,
               'postal_code' : postal_code
           },
           success: function(data, textStatus, XMLHttpRequest){
             $('#result').show();
           },
           error: function(XMLHttpRequest, textStatus, errorThrown) {
               alert('oh shit');
           } 
         });
    });
});

