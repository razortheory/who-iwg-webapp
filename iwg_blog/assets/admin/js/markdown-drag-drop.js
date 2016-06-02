$(document).ready(function () {
  $.markItUp.fullscreen = false;

  function addEventHandler(obj, evt, handler) {
    if (obj.addEventListener) {
      obj.addEventListener(evt, handler, false);
    } else if (obj.attachEvent) {
      obj.attachEvent('on' + evt, handler);
    } else {
      obj['on' + evt] = handler;
    }
  }

  addEventHandler(window, "drop", function (event) {
    if (event.target.className == "markItUpEditor") {
      event = event || window.event;
      if (event.preventDefault) {
        event.preventDefault();
      }

      event.target.focus();

      var files = event.dataTransfer.files;

      var data = new FormData();
      data.append('image_file', files[0]);

      loading_spinner_enabled = true;
      $.ajax({
        url: event.target.getAttribute('data-upload-image-url'),
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
  });
});

// $(document).ready(function(){
//
// });