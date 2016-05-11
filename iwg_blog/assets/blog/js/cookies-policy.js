function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
    }
    return "";
}

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}

var show_cookie_policy = true;
function confirmPrivacyCookie() {
    $('.cookies-policy').fadeOut(500);
    show_cookie_policy = false;
}

$(document).ready(function () {
    var privacy_cookie = getCookie('privacy_cookie');
    if (!privacy_cookie) {
        $('.cookies-policy').addClass('active');

        setCookie('privacy_cookie', 'true', 20 * 365);
    }
    else {
        show_cookie_policy = true;
    }

    window.onscroll = function () {
        if (show_cookie_policy) {
            window.setTimeout(confirmPrivacyCookie, 3000);
        }
    };
});