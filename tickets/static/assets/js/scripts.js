(function(window, undefined) {
    'use strict';

    if(window.location.hash && window.location.hash == '#ticket_modal') {
      $('#ticket_modal').modal('show');
    }

    $('#show_answer').on('click', function(){
        $('#ticket_block').addClass('show-answer');
    })


})(window);