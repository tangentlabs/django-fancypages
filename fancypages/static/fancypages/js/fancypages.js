var fancypages = {
    apiBaseUrl: "/api/v1/",
    /**
     * Get the CSRF token from the session to submit POST data.
     */
    getCsrfToken: function () {
        var cookies = document.cookie.split(';');
        var csrf_token = null;
        $.each(cookies, function (index, cookie) {
            cookieParts = $.trim(cookie).split('=');
            if (cookieParts[0] == 'csrftoken') {
                csrfToken = cookieParts[1];
            }
        });
        return csrfToken;
    },
    /**
     * Remove the modal for an element.
     */
    removeModal: function (elem) {
        var modalElem = $(elem).parents('#delete-modal');
        modalElem.remove();
    }
};