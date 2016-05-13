$(function () {
    $(".tag-it").each(function (i, e) {
        var options = {
            fieldName: $(e).attr('name'),
            removeConfirmation: true,
            allowSpaces: true,
            caseSensitive: false,
        }

        var autocompleteUrl = $(e).attr('autocomplete-url');
        if (autocompleteUrl) {
            var autocomplete = {
                source: function (request, response) {
                    request.exclude = $(e).tagit('assignedTags');

                    $.ajax({
                        url: autocompleteUrl,
                        data: request,
                        traditional: true,
                        success: response,
                    })
                },
                minLength: 0,
                appendTo: '#' + $(e).attr('id') + ' .tagit-new',
            }
            options.autocomplete = autocomplete;
            options.showAutocompleteOnFocus = true;
        }

        $(e).tagit(options);
    });
});
