$(document).ready(function () {
    var $galleryWrapper = $('.images-gallery-wrapper');
    var $gallery = $('.images-gallery', $galleryWrapper);
    if (window.innerWidth >= 768){
        $gallery.find('.images-gallery-item a').fancybox({
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
        $gallery.imagesLoaded().progress( function() {
          $gallery.masonry('layout');
        });
    }
    else {
        $gallery.imagesLoaded(function(){
            $gallery.bxSlider({
                pager: false,
                controls: false,
                adaptiveHeight: true,
                infiniteLoop: false,
                preloadImages: 'all',
                oneToOneTouch: false,
                preventDefaultSwipeX: false,
            });
        });
    }
});
