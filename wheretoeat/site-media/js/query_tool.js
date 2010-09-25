$(document).ready(function() {
    $('#id_search_button').click(function(e){
        e.preventDefault();
        
        $.getJSON(SEARCH_JSON, function(data) {
            $('#result').show();
        });
    });
});

