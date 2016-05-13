function windowShare(url, winWidth, winHeight) {
  if (!winWidth) {
    winWidth = 500;
  }
  if (!winHeight) {
    winHeight = 350;
  }
  var winTop = (screen.height / 2) - (winHeight / 2);
  var winLeft = (screen.width / 2) - (winWidth / 2);

  window.open(
    updateURLParameter(url, 'nocache', makeid(12)), 'sharer',
    'top=' + winTop + ',left=' + winLeft + ',toolbar=0,status=0,width=' + winWidth + ',height=' + winHeight
  );
}

function fbShare(url, winWidth, winHeight) {
  var window_url = 'http://www.facebook.com/sharer.php?s=100';
  if (!url) {
    url = window.location.href;
  }
  window_url = updateURLParameter(window_url, 'p[url]', encodeURIComponent(url));
  windowShare(window_url, winWidth, winHeight);
}

function twitterShare(url, winWidth, winHeight) {
  var window_url = 'https://twitter.com/share?via=IWG';
  if (!url) {
    url = window.location.href;
  }
  window_url = updateURLParameter(window_url, 'url', encodeURIComponent(url));
  windowShare(window_url, winWidth, winHeight);
}

function googleShare(url, winWidth, winHeight) {
  var window_url = 'https://plus.google.com/share';
  if (!url) {
    url = window.location.href;
  }
  window_url = updateURLParameter(window_url, 'url', encodeURIComponent(url));
  windowShare(window_url, winWidth, winHeight);
}

$(document).ready(function () {
  $('a.fb_sharer').click(function () {
    fbShare(this.href);
    return false;
  });
  $('a.twitter_sharer').click(function () {
    twitterShare(this.href);
    return false;
  });
  $('a.google_sharer').click(function () {
    googleShare(this.href);
    return false;
  });
});
