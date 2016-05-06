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
        if ($dropdown.hasClass('active')) {
            $dropdown.height($dropdown.find('.fixed-info__body-inner').innerHeight());
        }
        else {
            $dropdown.height(0);
        }
    });

    $.slidebars({
        siteClose: true,
        scrollLock: false,
    });
});
$('.search-mobile__button').click(function(){
    var $wrapper = $('.header__search-mobile'),
        $wrapperInner = $('.search-mobile'),
        isOpen = $wrapper.hasClass('search-opened');
    $wrapperInner.toggleClass('search-mobile-opened');
    $wrapper.toggleClass('search-opened')
      .find('.search-mobile__field')[isOpen ? 'blur' : 'focus']();
    return false;
});

// Search
$(function () {
  var $searchInput = $('#id__search-top__field'),
    $searchResultsWrapper = $('#id__search-top-results'),
    $searchResults = $('#id__search-top-results__list'),
    searchItemTemplate = $('#id__search-top-result__template').html();

  $searchInput.on('input', function (e) {
    var searchTerm = $(this).val();
    if (searchTerm.length < 3) {
      $searchResultsWrapper.hide();
      return;
    }

    $.get(SEARCH_URL, params = {
      q: searchTerm,
    })
    .done(function (data) {
      var results = data.data;
      if (results.length) {
        $searchResults.empty();
        for (var i = 0, result; result = results[i]; i++) {
          var itemHtml = searchItemTemplate.replace(/{\s*([a-zA-Z0-9-_]+)\s*}/g, function (_, key) {
            return result[key];
          });
          $searchResults.append(itemHtml);
        }
        $searchResultsWrapper.show();
      } else {
        $searchResultsWrapper.hide();
      }
    });
  });

  var $form = $('.search-top form');
  function onFormFocus(){
    $(this).addClass('active');
    $(this).find('input').trigger('input');
  }
  function onFormBlur(){
    if ($(this).find('input').val().length == 0){
      $(this).removeClass('active');
    }
    $(this).find('.search-top-results').hide();
  }
  $form[0].addEventListener('focus', onFormFocus, true);
  $form[0].addEventListener('blur', onFormBlur, true);
  $('.search-top-results, .search-top__button', $form).on('mousedown', function(event){
    event.preventDefault();
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
                    },
                };

            iSlider.carouFredSel(options);
        });
    }
}
