FancypageApp.module('Api', function (Api, FancypageApp, Backbone, Marionette, $, _) {
    "use strict"

    Api.baseUrl = "/api/v2";

    /**
     * Get the CSRF token from the session to submit POST data.
     */
    Api.getCsrfToken = function () {
        var allCookies = document.cookie.split(';'),
            csrfToken = null,
            cookieParts = null;

        if (_.isEmpty(allCookies)) {
            return null;
        }

        _.each(allCookies, function (cookie, index) {
            cookieParts = $.trim(cookie).split('=');

            if (cookieParts[0] == 'csrftoken') {
                csrfToken = cookieParts[1];
            }
        });
        return csrfToken;
    };
});
