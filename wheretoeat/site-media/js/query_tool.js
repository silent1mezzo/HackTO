$(document).ready(function() {
    
    $('#id_search_button').click(function(e){
        $('#id_search_button').attr('disabled', 'disabled');
        e.preventDefault();
        var text = $('#id_q').val();
        var postal_code = $('#id_postal_code').val();
        $('#results').hide();
        $('#error').hide();
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
                   $('#error').show();
               } else {
                   $('#id_company_name').text(data.name);
                   $('#id_street_address').text(data.street_address);
                   $('#id_prov').text(data.province);
                   $('#id_city').text(data.city);
                   $('#id_rank').text(data.relavence_rank);
                   $('#id_distance').text(data.distance);
                   $('#id_weather').text(data.weather_desc);
                   $('#weather_icon').attr("src", data.weather_icon);

                   $('#results').show('drop', {}, 100, function(){
                       var location = new google.maps.LatLng(data.latitude, data.longitude); 
                       var map = new google.maps.Map(document.getElementById('id_map'), {
                           zoom: 14,
                           center: location,
                           mapTypeId: google.maps.MapTypeId.ROADMAP
                       });                       
                       var marker = new google.maps.Marker({
                           position: location,
                           map: map
                       });
                       map.panTo(location);
                   });
               }
           },
           error: function(XMLHttpRequest, textStatus, errorThrown) {
               alert("Um... crap. This wasn't supposed to happen.");
           },
           complete: function() {
               $('#id_search_button').removeAttr('disabled');
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

