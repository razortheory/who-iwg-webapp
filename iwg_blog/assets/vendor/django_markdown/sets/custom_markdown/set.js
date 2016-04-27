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
        setTimeout(function(){
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
    onShiftEnter: {keepDefault:false, openWith:'\n\n'},
    markupSet: [
        {name:'First Level Heading', key:'1', placeHolder:'Your title here...', closeWith:function(markItUp) { return miu.markdownTitle(markItUp, '=') } },
        {name:'Second Level Heading', key:'2', placeHolder:'Your title here...', closeWith:function(markItUp) { return miu.markdownTitle(markItUp, '-') } },
        {name:'Heading 3', key:'3', openWith:'### ', placeHolder:'Your title here...' },
        {name:'Heading 4', key:'4', openWith:'#### ', placeHolder:'Your title here...' },
        {name:'Heading 5', key:'5', openWith:'##### ', placeHolder:'Your title here...' },
        {name:'Heading 6', key:'6', openWith:'###### ', placeHolder:'Your title here...' },
        {separator:'---------------' },
        {name:'Bold', key:'B', openWith:'**', closeWith:'**'},
        {name:'Italic', key:'I', openWith:'_', closeWith:'_'},
        {separator:'---------------' },
        {name:'Bulleted List', openWith:'- ' },
        {name:'Numeric List', openWith:function(markItUp) {
            return markItUp.line+'. ';
        }},
        {separator:'---------------' },
        {name:'Picture', key:'P', replaceWith:'![[![Alternative text]!]]([![Url:!:http://]!] "[![Title]!]")'},
        {
            name:'Pictures gallery',
            key:'G',
            openWith: '----images-gallery----\n',
            closeWith: '----------------------\n'
        },
        {
            name:'Embed Video',
            key:'E',
            replaceWith:function(h) {
                var video_width = prompt('Widget width (empty for auto)');
                var video_height = prompt('Widget height (empty for auto)');
                var video_link = prompt('Video link', 'http://');
                var result = '![embed';
                var params = '';
                if (video_width) {
                    params += 'width=' + video_width;
                }
                if (video_height) {
                    if (params){
                        params += '&';
                    }
                    params += 'height=' + video_height;
                }
                if (params){
                    result += '?' + params;
                }
                result += '](' + video_link + ')';
                return result;
            }
        },
        {name:'Link', key:'L', openWith:'[', closeWith:']([![Url:!:http://]!] "[![Title]!]")', placeHolder:'Your text to link here...' },
        {
            name:'Article content preview',
            openWith:'----article-content-preview----\nimage: ',
            closeWith: '\ntext: \ndescription: \nurl: \n-------------------------------\n',
            placeHolder:'Insert image url or tag here...'
        },
        {separator:'---------------'},
        {name:'Quotes', openWith:'> '},
        {name:'Table',
            header:" header ",
            seperator:" ------ ",
            placeholder:" data   ",
            replaceWith:function(h) {
                cols = prompt("How many cols?");
                rows = prompt("How many rows?");
                out = "";
                // header row
                for (c = 0; c < cols; c++) {
                        out += "|"+(h.header||"");
                }
                out += "|\n";
                // seperator
                for (c = 0; c < cols; c++) {
                        out += "|"+(h.seperator||"");
                }
                out += "|\n";
                for (r = 0; r < rows; r++) {
                    for (c = 0; c < cols; c++) {
                        out += "|"+(h.placeholder||"");
                    }
                    out += "|\n";
                }
                return out;
            }
        },
        {separator:'---------------'},
        {name:'Preview', call:'preview', className:"preview"},
        {
            name: 'Fullscreen',
            className: 'markItUpFullScreen',
            call: function () {
                var minimize = function () {
                    var textarea = $('#fullscreen');
                    var caretPosition = getCaretPosition(textarea[0]);
                    $($.markItUp.fullscreenSource).val(textarea.val());
                    setCaretPosition($.markItUp.fullscreenSource, caretPosition);
                    textarea.unbind();
                    setTimeout(function(){
                        $.markItUp({target: $($.markItUp.fullscreenSource)})
                    }, 1);

                    var container = textarea.parents('.markItUp').jqmHide();
                    container.parent().remove();

                    $.markItUp.fullscreen = false;
                };

                if (!$.markItUp.fullscreen) {
                    $.markItUp.fullscreenSource = $.markItUp.focused;
                    var caretPosition = getCaretPosition($.markItUp.fullscreenSource);
                    var origTextarea = $($.markItUp.fullscreenSource);

                    $('body').append('<textarea id="fullscreen"></textarea>');

                    var textarea = $('#fullscreen');
                    $(origTextarea[0].attributes).each(function() {
						if (this.nodeName.indexOf('data-') == 0){
							textarea.attr(this.nodeName, this.nodeValue);
						}
                    });
                    textarea.val(origTextarea.val()).show().markItUp(
                        mySettings, {"previewParserPath": origTextarea.data('preview-parser-url')}
                    );

                    var container = textarea.parents('.markItUp');
                    setTimeout(function(){
                        container.jqm({toTop: true}).jqmShow();
                    }, 0);
                    setCaretPosition(textarea[0], caretPosition);

                    var closeBtn = '<a href="#" class="fullScreenClose">x</a>';
                    $('.markItUpHeader', container).append(closeBtn);

                    $('.fullScreenClose, .jqmOverlay', container).click(function () {
                        minimize();
                        return false;
                    });

                    $.markItUp.fullscreen = true;
                } else {
                    minimize();
                    return false;
                }
            }
        }
    ],
    onTab: {
        keepDefault: false,
        replaceWith: function(h){
            return "\t";
        }
    }
};

// mIu nameSpace to avoid conflict.
miu = {
    markdownTitle: function(markItUp, achar) {
        heading = '';
        n = $.trim(markItUp.selection||markItUp.placeHolder).length;
        // work around bug in python-markdown where header underlines must be at least 3 chars
        if (n < 3) { n = 3; }
        for(i = 0; i < n; i++) {
            heading += achar;
        }
        return '\n'+heading;
    }
};

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

    addEventHandler(window, 'dragenter', function (event) {
        event.preventDefault();
    });

    addEventHandler(window, 'dragover', function (event) {
        event.preventDefault();
    });

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
                    $.markItUp({replaceWith: '![alt_text](' + data.image_file.url + ' "title")\n'});
                },
                error: function (data, textStatus, errorThrown) {
                    console.log('ERRORS: ' + data.statusText);
                }
            });
        }
    });
});