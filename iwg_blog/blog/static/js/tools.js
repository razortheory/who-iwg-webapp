$(document).ready(function() {
    $(window).resize(sizeContent);
    function sizeContent() {
        var sliderHeight = $(window).height()*0.76 + "px";
        $(".js-slider-container").css("height", sliderHeight);
        carouFredSelInit($('.js-slider'), 1, true, '100%', "auto", false, false, 'center', true);
    }
    sizeContent();
    window.setTimeout(sizeContent, 100);

    $("#js-fixed-toggle").on('click', function(e) {
        var $button = $(this),
            $dropdown = $('#js-fixed-toggled-content');
        e.preventDefault();
        $(this).toggleClass('opened');
        $dropdown.toggleClass('active');
        if ( $dropdown.height() <= 0) {
            $dropdown.height($dropdown.find('.fixed-info__body-inner').innerHeight());
        }
        else {
            $dropdown.height(0);
        }
    });
});

function carouFredSelInit (Slider, visible, responsive, width, height, autoplay, circular, align, swipe) {

    if (typeof $().carouFredSel == 'function') {

        // Cache slide navigation
        Slider.each(function(i, iSlider) {

            iSlider = $(iSlider);

            var sliderContainer = iSlider.parents('.js-slider-container'),

                options = { // Common slider options
                    // width: '100%',
                    // height: 'auto',
                    width: width,
                    height: height,
                    items: {
                        visible: visible,
                        // height: '100%',
                        width: 3000
                    },
                    align: align,
                    responsive: responsive,
                    // circular: false,
                    scroll: {
                        items: 1,
                        fx: 'directscroll',
                        duration: 600
                    },
                    auto: {
                        play: autoplay,
                        timeoutDuration: 7000
                    },
                    circular: circular,
                    infinite: false,
                    pagination: {
                        container: sliderContainer.find('.js-slider-pager')
                    },
                    swipe: {
                        onTouch: swipe,
                        onMouse: swipe
                    }
                };

            iSlider.carouFredSel(options);
        });
    }
}
