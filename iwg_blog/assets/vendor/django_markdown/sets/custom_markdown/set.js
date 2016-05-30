// -------------------------------------------------------------------
// markItUp!
// -------------------------------------------------------------------
// Copyright (C) 2008 Jay Salvat
// http://markitup.jaysalvat.com/
// -------------------------------------------------------------------
// MarkDown tags example
// http://en.wikipedia.org/wiki/Markdown
// http://daringfireball.net/projects/markdown/
// -------------------------------------------------------------------
// Feel free to add more tags
// -------------------------------------------------------------------

function getCaretPosition(ctrl) {
  var CaretPos = 0;
  // IE Support
  if (document.selection) {
    ctrl.focus();
    var Sel = document.selection.createRange();
    Sel.moveStart('character', -ctrl.value.length);
    CaretPos = Sel.text.length;
  }
  // Firefox support
  else if (ctrl.selectionStart || ctrl.selectionStart == '0')
    CaretPos = ctrl.selectionStart;

  return (CaretPos);
}


function setCaretPosition(ctrl, pos) {
  if (ctrl.setSelectionRange) {
    ctrl.focus();
    setTimeout(function () {
      ctrl.setSelectionRange(pos, pos);
    }, 0)
  }
  else if (ctrl.createTextRange) {
    var range = ctrl.createTextRange();
    range.collapse(true);
    range.moveEnd('character', pos);
    range.moveStart('character', pos);
    range.select();
  }
}

mySettings = {
  onShiftEnter: {keepDefault: false, openWith: '\n\n'},
  markupSet: [
    {
      className: 'mui-h1 icon-h1',
      name: 'First Level Heading',
      key: '1',
      placeHolder: 'Your title here...',
      closeWith: function (markItUp) {
        return miu.markdownTitle(markItUp, '=')
      }
    },
    {
      className: 'mui-h2 icon-h2',
      name: 'Second Level Heading',
      key: '2',
      placeHolder: 'Your title here...',
      closeWith: function (markItUp) {
        return miu.markdownTitle(markItUp, '-')
      }
    },
    {className: 'mui-h3 icon-h3', name: 'Heading 3', key: '3', openWith: '### ', placeHolder: 'Your title here...'},
    {className: 'mui-h4 icon-h4', name: 'Heading 4', key: '4', openWith: '#### ', placeHolder: 'Your title here...'},
    {className: 'mui-h5 icon-h5', name: 'Heading 5', key: '5', openWith: '##### ', placeHolder: 'Your title here...'},
    {className: 'mui-h6 icon-h6', name: 'Heading 6', key: '6', openWith: '###### ', placeHolder: 'Your title here...'},
    {separator: '---------------'},
    {className: 'mui-bold icon-bold', name: 'Bold', key: 'B', openWith: '**', closeWith: '**'},
    {className: 'mui-italic icon-italic', name: 'Italic', key: 'I', openWith: '_', closeWith: '_'},
    {separator: '---------------'},
    {className: 'mui-list-bulleted icon-list_ordered', name: 'Bulleted List', openWith: '- '},
    {
      className: 'mui-list-numeric icon-list_unordered', name: 'Numeric List', openWith: function (markItUp) {
      return markItUp.line + '. ';
    }
    },
    {separator: '---------------'},
    {
      className: 'mui-picture-modal icon-add_image', name: 'Picture', replaceWith: function (h) {
        window.imageModalDialog.dialog("open");
      }
    },
    {
      className: 'mui-picture-gallery icon-add_image_gallery',
      name: 'Pictures gallery',
      key: 'G',
      openWith: '----images-gallery----\ncolumns: 2\n',
      placeHolder: 'Insert your images here'
    },
    {
      className: 'mui-embed icon-add_media',
      name: 'Embed Video',
      key: 'E',
      openWith: '![embed](',
      closeWith: ')\n',
      placeHolder: 'http://'
    },
    {
      className: 'mui-link icon-link',
      name: 'Link',
      key: 'L',
      openWith: '[',
      closeWith: '](http://)',
      placeHolder: 'Your text to link here...'
    },
    {
      className: 'mui-big-link icon-link_article',
      name: 'Big link',
      openWith: '----big-link----\nimage: ',
      closeWith: '\ntext: \ndescription: \nurl: \n',
      placeHolder: 'Insert image url or tag here...'
    },
    {separator: '---------------'},
    {className: 'mui-quotes icon-quote', name: 'Quotes', openWith: '> '},
    {
      className: 'mui-table icon-table',
      name: 'Table',
      replaceWith: function (h) {
        window.gridModalDialog.dialog("open");
      }
    },
    // {separator: '---------------'},
    // {name: 'Preview', call: 'preview', className: "preview"},
    // {
    //   name: 'Fullscreen',
    //   className: 'markItUpFullScreen',
    //   call: function () {
    //     var minimize = function () {
    //       var textarea = $('#fullscreen');
    //       var caretPosition = getCaretPosition(textarea[0]);
    //       $($.markItUp.fullscreenSource).val(textarea.val());
    //       setCaretPosition($.markItUp.fullscreenSource, caretPosition);
    //       textarea.unbind();
    //       setTimeout(function () {
    //         $.markItUp({target: $($.markItUp.fullscreenSource)})
    //       }, 1);
    //
    //       var container = textarea.parents('.markItUp').jqmHide();
    //       container.parent().remove();
    //
    //       $.markItUp.fullscreen = false;
    //     };
    //
    //     if (!$.markItUp.fullscreen) {
    //       $.markItUp.fullscreenSource = $.markItUp.focused;
    //       var caretPosition = getCaretPosition($.markItUp.fullscreenSource);
    //       var origTextarea = $($.markItUp.fullscreenSource);
    //
    //       $('body').append('<textarea id="fullscreen"></textarea>');
    //
    //       var textarea = $('#fullscreen');
    //       $(origTextarea[0].attributes).each(function () {
    //         if (this.nodeName.indexOf('data-') == 0) {
    //           textarea.attr(this.nodeName, this.nodeValue);
    //         }
    //       });
    //
    //       textarea.val(origTextarea.val()).show().markItUp(
    //         mySettings, {"previewParserPath": origTextarea.data('preview-parser-url')}
    //       );
    //
    //       var container = textarea.parents('.markItUp');
    //       setTimeout(function () {
    //         container.jqm({toTop: true}).jqmShow();
    //       }, 0);
    //       setCaretPosition(textarea[0], caretPosition);
    //
    //       var closeBtn = '<a href="#" class="fullScreenClose">x</a>';
    //       $('.markItUpHeader', container).append(closeBtn);
    //
    //       $('.fullScreenClose, .jqmOverlay', container).click(function () {
    //         minimize();
    //         return false;
    //       });
    //
    //       $.markItUp.fullscreen = true;
    //     } else {
    //       minimize();
    //       return false;
    //     }
    //   }
    // }
  ],
  onTab: {
    keepDefault: false,
    replaceWith: function (h) {
      return "\t";
    }
  }
};

// mIu nameSpace to avoid conflict.
miu = {
  markdownTitle: function (markItUp, achar) {
    heading = '';
    n = $.trim(markItUp.selection || markItUp.placeHolder).length;
    // work around bug in python-markdown where header underlines must be at least 3 chars
    if (n < 3) {
      n = 3;
    }
    for (i = 0; i < n; i++) {
      heading += achar;
    }
    return '\n' + heading;
  }
};

$(document).ready(function () {
  function addEventHandler(obj, evt, handler) {
    if (obj.addEventListener) {
      obj.addEventListener(evt, handler, false);
    } else if (obj.attachEvent) {
      obj.attachEvent('on' + evt, handler);
    } else {
      obj['on' + evt] = handler;
    }
  }

  $(document).on('init.markItUp', function(event){
    $.markItUp.fullscreen = false;

    var textarea = event.target;
    var $markItUp = $(textarea).closest('.markItUp');
    $markItUp.append(
      '<div class="drop-zone">' +
        '<div class="drop-zone_inner">' +
          '<i class="drop-zone_image icon-add_image"> </i>' +
          '<h1 class="drop-zone_text">Drop to upload image</h1>' +
        '</div>' +
      '</div>'
    );

    addEventHandler($markItUp[0], "drop", function (event) {
      console.log('drop', event);

      event.preventDefault();
      event.stopPropagation();

      textarea.focus();

      var files = event.dataTransfer.files;

      var data = new FormData();
      data.append('image_file', files[0]);

      loading_spinner_enabled = true;
      $.ajax({
        url: textarea.getAttribute('data-upload-image-url'),
        type: 'POST',
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function (data, textStatus, jqXHR) {
          $.markItUp({replaceWith: '![alt_text](' + data.image_file.url + ')\n', target: textarea});
          $markItUp.trigger('dragleave');
        },
        error: function (data, textStatus, errorThrown) {
          console.log('ERRORS: ' + data.statusText);
          $markItUp.trigger('dragleave');
        }
      });
    });

    $('body').on('drop', function(event){
      console.log('drop', event);
      event.preventDefault();
      event.stopPropagation();
    });

    var dragOverTimeout;
    $markItUp.on('dragover dragenter', function (event) {
      $markItUp.addClass('dragenter');
      clearTimeout(dragOverTimeout);
      event.preventDefault();
      event.stopPropagation();
    }).on('dragleave', function(){
      clearTimeout(dragOverTimeout);
      dragOverTimeout = setTimeout(function () {$markItUp.removeClass('dragenter')}, 200);
      event.preventDefault();
      event.stopPropagation();
    });
  });
});
