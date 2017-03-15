(function() {
    "use strict";

    // Save the value of one (default) element in the database
    var saveElement = function(event) {
        event.preventDefault();

        var $input = $(this);
        var inputId = $input.attr('id');

        console.log('Saving element ' + inputId + '...');
        $.ajax({
            'url': dataStructureElementUrl,
            'type': 'POST',
            'dataType': 'json',
            'data': {
                'id': inputId,
                'value': $input.is(":checked")
            },
            success: function() {
                console.log('Element ' + inputId + ' saved');
            },
            error: function() {
                console.error('An error occurred when saving element ' + inputId);
            }
        });
    };

    // Save events
    $(document).on('change', 'input:checkbox', saveElement);
})();

