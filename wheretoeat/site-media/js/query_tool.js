$(document).ready(function() {
    $('#id_search_button').click(function(e){
        e.preventDefault();
        
        var text = $('#id_q').val();
        var postal_code = $('#id_postal_code').val();
        $('#result').hide();
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
               $('#loading').hide();
               if (data.status == 'EMPTY') {
                   alert('empty');
               }
               else {
                   $('#id_company_name').text(data.name);
                   $('#id_street_address').text(data.street_address);
                   $('#id_prov').text(data.province);
                   $('#id_city').text(data.city);
                   $('#result').show();
               }
           },
           error: function(XMLHttpRequest, textStatus, errorThrown) {
               alert('oh shit');
           } 
         });
    });
    
    $('.small-input').focus(function(e){
        if($(this).val() == 'What should I eat?'){
            $(this).val('');
        }
    });
    $('.small-input').blur(function(e){
        if($(this).val() == ''){
            $(this).val('What should I eat?');
        }
    });
    $('.small-postal').focus(function(e){
        if($(this).val() == 'M5V 2H5'){
            $(this).val('');
        }
    });
    $('.small-postal').blur(function(e){
        if($(this).val() == ''){
            $(this).val('M5V 2H5');
        }
    });
});

