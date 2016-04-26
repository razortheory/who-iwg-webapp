function autoSaveData(){
    $('[data-autosave]').each(function(){
        var $fullscreen = $('#fullscreen[data-autosave="' + $(this).data('autosave') + '"]');
        if ($fullscreen.length == 0){
            localStorage.setItem($(this).data('autosave'), $(this).val());
        }
        else {
            localStorage.setItem($(this).data('autosave'), $fullscreen.val());
        }
    });
}

function restoreAutoSavedData(){
    $('[data-autosave]').each(function(){
        var autosave_data = localStorage.getItem($(this).data('autosave'));
        if (autosave_data){
            $(this).val(autosave_data);
        }
    });
}

function clearAutoSavedData(){
    $('[data-autosave]').each(function(){
        localStorage.removeItem($(this).data('autosave'));
    });
}

function hasAutoSavedData(){
    return $('[data-autosave]').map(function(){
        var autosave_data = localStorage.getItem($(this).data('autosave'));
        return Boolean(autosave_data) && autosave_data != $(this).val()
    }).get().indexOf(true) != -1
}

$(document).ready(function(){
    if (hasAutoSavedData()){
        $("#dialog-autosave-confirm").dialog({
            resizable: false,
            height: 140,
            modal: true,
            buttons: {
                "Yes": function () {
                    restoreAutoSavedData();
                    clearAutoSavedData();
                    $(this).dialog("close");
                },
                "No": function () {
                    clearAutoSavedData();
                    $(this).dialog("close");
                }
            }
        });
    }

    $('form').submit(clearAutoSavedData);

    setInterval(function(){
        autoSaveData();
    }, 3000);
});