FancypageApp.module('Api', function (Api, FancypageApp, Backbone, Marionette, $, _) {
    "use strict"

    Api.baseUrl = "/api/v2";

    /**
     * Get the CSRF token from the session to submit POST data.
     */
    Api.getCsrfToken = function () {
        return $.cookie('csrftoken');
    };

    Api.reloadPage = function () {
        $('div[data-behaviours~=loading]').fadeIn(300);
        setTimeout(function () {
            window.location.reload();
        }, 300);
    }
});
