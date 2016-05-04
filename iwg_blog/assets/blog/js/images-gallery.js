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
            $gallery.carouFredSel({
                responsive: true,
                pagination: {
                    container: $('.images-gallery-paginator', $galleryWrapper)
                },
                auto: {
                    play: false
                },
                swipe: {
                    onTouch: true,
                    onMouse: true,
                    options: {
                        excludedElements:"button, input, select, textarea, .noSwipe"
                    }
                }
            });
        });
    }
});
