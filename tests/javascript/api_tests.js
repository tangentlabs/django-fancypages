suite('apiTests', function () {

    suite('apiModule.getCsrfToken', function () {

        test('returns existing CSRF token in cookies', function () {
            document.cookie = "some_cookie=value;csrftoken=thetoken;something=else";
            token = FancypageApp.Api.getCsrfToken();
            assert.equal(token, 'thetoken');
        });

        test('returns undefined if no cookies available', function () {
            document.cookie = '';
            token = FancypageApp.Api.getCsrfToken();
            assert.equal(token, null);
        });

        test('returns undefined if CSRF token not in cookies', function () {
            document.cookie = "some_cookie=value;something=else";
            token = FancypageApp.Api.getCsrfToken();
            assert.equal(token, null);
        });

    });

});
