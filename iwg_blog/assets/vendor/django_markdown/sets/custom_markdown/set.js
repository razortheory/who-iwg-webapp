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
				var result = '[!embed';
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
		{name:'Preview', call:'preview', className:"preview"}
	]
};

// mIu nameSpace to avoid conflict.
miu = {
	markdownTitle: function(markItUp, achar) {
		heading = '';
		n = jQuery.trim(markItUp.selection||markItUp.placeHolder).length;
		// work around bug in python-markdown where header underlines must be at least 3 chars
		if (n < 3) { n = 3; }
		for(i = 0; i < n; i++) {
			heading += achar;
		}
		return '\n'+heading;
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

	window.ondragenter = function(event){
		event.preventDefault();
	};

	window.ondragover = function(event){
		event.preventDefault();
	};

	var markItUps = document.getElementsByTagName('textarea');
	for (var i=0; i<markItUps.length; i++){
		addEventHandler(markItUps[i], "drop", function (event) {
			if ( event.target.className == "markItUpEditor" ) {
				event = event || window.event;
				if (event.preventDefault) {
					event.preventDefault();
				}

				event.target.focus();

				var files = event.dataTransfer.files;

				var data = new FormData();
				data.append('image_file', files[0]);

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
	}
});