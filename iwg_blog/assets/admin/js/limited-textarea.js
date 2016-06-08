/*
 * Remained symbols indicator behavior for textarea.
 */
$(function () {
    $('.limited-textarea').each(function (i, e) {
        var $wrapper = $(e),
            $textarea = $wrapper.find('textarea'),
            $counter = $wrapper.find('.counter'),
            maxLength = $textarea.attr('maxlength');

        var updateCounter = function () {
            $counter.html(maxLength - $textarea.val().length);
        }

        $textarea.on('input', updateCounter);
        updateCounter();
    });
});
