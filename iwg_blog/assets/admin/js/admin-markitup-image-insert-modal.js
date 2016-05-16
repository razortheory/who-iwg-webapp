$(function () {
    function uploadImage() {
        var form = window.imageModalForm;
        var url = form.find('#image-insert-url').val();
        if (url){
            $.markItUp({replaceWith: '![alt_text](' + url + ')\n'});
            window.imageModalDialog.dialog("close");
            return;
        }

        if (form.find('#image-insert-file')[0].files.length == 0){
            window.imageModalDialog.dialog("close");
            return;
        }

        var data = new FormData();
        data.append('image_file', form.find('#image-insert-file')[0].files[0]);

        loading_spinner_enabled = true;
        window.imageModalDialog.dialog("close");

        $.ajax({
            url: $(".markItUpEditor").attr('data-upload-image-url'),
            type: 'POST',
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function (data, textStatus, jqXHR) {
                $.markItUp({replaceWith: '![alt_text](' + data.image_file.url + ')\n'});
            },
            error: function (data, textStatus, errorThrown) {
                console.log('ERRORS: ' + data.statusText);
            }
        });
    }

    window.imageModalDialog = $("#image-insert-form").dialog({
        autoOpen: false,
        height: 180,
        width: 350,
        modal: true,
        buttons: {
            "Add": uploadImage,
            "Cancel": function () {
                window.imageModalDialog.dialog("close");
            }
        },
        close: function () {
            window.imageModalForm[0].reset();
        }
    });

    window.imageModalForm = window.imageModalDialog.find("form").on("submit", function (event) {
        event.preventDefault();
        uploadImage();
    });
});