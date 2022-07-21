(function($) {
    $(function() {
        var selectField = $('#id_apartment_type'),
            verified = $('.abcdefg');

        function toggleVerified(value) {
            if (value === 'X') {
                verified.show();
            } else {
                verified.hide();
            }
        }

        // show/hide on load based on existing value of selectField
        toggleVerified(selectField.val());

        // show/hide on change
        selectField.change(function() {
            toggleVerified($(this).val());
        });
    });
})(django.jQuery);