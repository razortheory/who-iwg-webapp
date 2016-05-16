var one_day_ms = 24 * 60 * 60 * 1000;


function autoSaveData(){
    $('[data-autosave]').each(function(){
        var $fullscreen = $('#fullscreen[data-autosave="' + $(this).data('autosave') + '"]');
        if ($fullscreen.length == 0){
            localStorage.setItem($(this).data('autosave'), $(this).val());
        }
        else {
            localStorage.setItem($(this).data('autosave'), $fullscreen.val());
        }
        localStorage.setItem($(this).data('autosave') + '_date', new Date);
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
        var autosave_date = new Date(localStorage.getItem($(this).data('autosave') + '_date'));
        return Boolean(autosave_data) && autosave_data != $(this).val() && new Date - autosave_date < one_day_ms
    }).get().indexOf(true) != -1
}

function enableAutoSaving(){
    return setInterval(function(){
        autoSaveData();
    }, 3000);
}

$(document).ready(function(){
    var autosave_interval;
    if (hasAutoSavedData()){
        $("#dialog-autosave-confirm").dialog({
            resizable: false,
            height: 140,
            modal: true,
            buttons: {
                "Yes": function () {
                    restoreAutoSavedData();
                    clearAutoSavedData();
                    autosave_interval = enableAutoSaving();
                    $(this).dialog("close");
                },
                "No": function () {
                    clearAutoSavedData();
                    autosave_interval = enableAutoSaving();
                    $(this).dialog("close");
                }
            }
        });
    } else {
        autosave_interval = enableAutoSaving();
    }

    $('form').submit(function(){
        if (autosave_interval) {
            clearInterval(autosave_interval);
        }
        clearAutoSavedData();
    });
});