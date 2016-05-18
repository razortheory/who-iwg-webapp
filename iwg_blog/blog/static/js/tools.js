$(document).ready(function() {
    $(window).resize(sizeContent);
    function sizeContent() {
        var sliderHeight = $(window).height()*0.76 + "px";
        $(".js-slider-container").css("height", sliderHeight);
    }
    sizeContent();
    window.setTimeout(sizeContent, 100);

    function initSlider() {
        $('.js-slider').bxSlider({
            infiniteLoop: false,
            preloadImages: 'all',
            oneToOneTouch: false,
            preventDefaultSwipeX: false,
            pagerSelector: '.js-slider-pager',
            pagerShortSeparator: ' ',
            buildPager: function (slideIndex) {
                return '<span>' + slideIndex + '</span>'
            },
            controls: false,
        });
    }
    initSlider();

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
    var $form = $('.search-mobile__form'),
        $wrapper = $('.header__search-mobile'),
        $wrapperInner = $('.search-mobile'),
        $input = $wrapper.find('.search-mobile__field')
        isOpen = $wrapperInner.hasClass('search-mobile-opened');

    if (!isOpen || !$input.val()) {
        if (isOpen) {

            $wrapper.animate({
                width: '40px'
            }, {
                duration: 1000,
                start: function () {
                    $input.blur();
                },
                done: function () {
                    $wrapperInner.removeClass('search-mobile-opened');
                },
            });

        } else {

            $wrapper.animate({
                width: ($wrapper.parent().width() - 33) + 'px'
            }, {
                duration: 1000,
                start: function () {
                    $wrapperInner.addClass('search-mobile-opened');
                },
                done: function () {
                    $input.focus();
                }
            });

        }
        return false;
    }
});

// Desktop search
$(function () {
  var $searchInput = $('#id__search-top__field'),
    $searchForm = $('#id_search-top__form'),
    $searchResultsWrapper = $('#id__search-top-results'),
    $searchResults = $('#id__search-top-results__list'),
    searchItemTemplate = $('#id__search-top-result__template').html();

  $searchInput.on('input', function (e) {
    var searchTerm = $(this).val();
    if (searchTerm.length < 3) {
      $searchResultsWrapper.hide();
      return;
    }

    $.get($searchForm.attr('action'), params = {
      q: searchTerm
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

  function onFormFocus(){
    $(this).addClass('active');
    $(this).find('input').trigger('input');
  }
  function onFormBlur(){
    if ($(this).find('input').val().length == 0){
      $(this).removeClass('active');
    }
    $searchResultsWrapper.hide();
  }
  $searchForm[0].addEventListener('focus', onFormFocus, true);
  $searchForm[0].addEventListener('blur', onFormBlur, true);
  $('.search-top-results, .search-top__button', $searchForm).on('mousedown', function(event){
    event.preventDefault();
  });
});
