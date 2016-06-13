var oldResetLayout = Masonry.prototype._resetLayout;

Masonry.prototype._resetLayout = function () {
  var _this = this;

  for (var i = 0; i < this.items.length; i++) {
    this.items[i].element.style.width = '';
  }

  oldResetLayout.apply(_this);
}


$(document).ready(function () {
  var $galleryWrapper = $('.images-gallery-wrapper');
  var $gallery = $('.images-gallery', $galleryWrapper);
  if (window.innerWidth >= 768) {
    $gallery.each(function (i, e) {
      $(e).find('.images-gallery-item a').attr('rel', 'group' + i);
    });
    $gallery.find('.images-gallery-item a').fancybox({
      closeBtn: false,
      nextClick: true,
      loop: false,
      helpers: {
        overlay: {
          locked: false
        }
      }
    });
    $gallery.masonry({
      itemSelector: '.images-gallery-item',
      percentPosition: true
    });

    $gallery.on('layoutComplete',
      function (event, laidOutItems) {
        // Alignment bottom border based on changing columns size
        var columns = {};

        for (var i = 0; i < laidOutItems.length; i++) {
          var el = laidOutItems[i],
            elLeft = el.position.x,
            elBottom = el.position.y + el.size.height;
          columns[elLeft] = columns[elLeft] || {},

            columns[elLeft].height = elBottom;
          columns[elLeft].width = el.size.width;
        }

        // new height = n / (1/h1 + 1/h2 + ...)
        var newHeight = 0;
        for (key in columns) {
          newHeight += 1 / columns[key].height;
        }
        newHeight = Object.keys(columns).length / newHeight;

        var left = 0;
        for (key in columns) {
          var column = columns[key];
          column.k = newHeight / column.height;

          column.left = left;
          left += column.width * column.k;

          column.top = 0;
        }

        for (var i = 0; i < laidOutItems.length; i++) {
          var el = laidOutItems[i],
            column = columns[el.position.x];
          el.element.style.width = column.width * column.k + 'px';
          el.element.style.left = column.left + 'px';
          el.element.style.top = column.top + 'px';

          column.top += el.size.height * column.k;
        }

        setTimeout(function () {
          $(event.target).css('height', newHeight + 'px');
        }, 0);
      }
    );

    $gallery.imagesLoaded(function () {
      $gallery.masonry('layout');
    });

    $(
      '.article .article__body-incut > figure > img, ' +
      '.article .article__body-incut > img, ' +
      '.article img.article__main-image'
    ).wrap(function () {
      return '<a href="' + this.getAttribute('src') + '"></a>'
    }).parent('a').fancybox({
      closeBtn: false,
      helpers: {
        overlay: {
          locked: false
        }
      }
    });
  }
  else {
    $gallery.imagesLoaded(function () {
      $gallery.bxSlider({
        pager: false,
        controls: true,
        adaptiveHeight: true,
        infiniteLoop: true,
        preloadImages: 'all',
        oneToOneTouch: false,
        preventDefaultSwipeX: false,
        nextText: "",
        prevText: ""
      });
    });
  }
});
