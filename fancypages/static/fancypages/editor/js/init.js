define(['module', 'jquery', 'cs!monster'], function(module, $, monster) {
    var addStylesheet = function(headElement, url) {
        var doc = headElement[0].ownerDocument;

        if (doc.createStyleSheet) {
            doc.createStyleSheet(url);
        }
        else {
            headElement.append($("<link/>",
                {
                    rel: "stylesheet",
                    href: url,
                    type: "text/css"
                }
            ));
       }
    };

    var run = function(forceBlank) {
        var config = module.config();

        var contents = $('iframe').contents();

        var head = contents.find("head");
        var body = contents.find("body");

        body.css({
            'padding': 0,
            'margin': 0
        });

        addStylesheet(head, config.baseStaticUrl + 'monster/lib/css/ui-lightness/jquery-ui-1.8.20.custom.css');
        addStylesheet(head, config.baseStaticUrl + 'monster/src/css/monster.css');

        var node = $('iframe').contents();

        var data = $.parseJSON($('input#id_data').val());

        if (forceBlank || !data) {
            data = [];
        }

        editor = new monster.Editor(node, data, function(){
            $('form').on('submit', function(event) {
                event.preventDefault();

                editor.render(function(html){
                    $('input#id_html').val(html);
                    var data = $.toJSON(editor.get_data());
                    $('input#id_data').val(data);
                }, $('input#id_template_copy').val());

                $('form').off('submit');
                $('form').submit();
            });
            $('.preview .loading-overlay').delay(500).fadeOut();
            $('form button').delay(500).fadeIn();
        });

    };

    var resetIframe = function(callback) {
        $('.preview .loading-overlay').show();
        var $iframe = $('iframe#previewFrame');
        var handler = function() {
            callback();
            $iframe.off('load', handler);
        };
        $iframe.on('load', handler);
        $iframe[0].src = $iframe[0].src;
    };

    var revert = function() {
        resetIframe(function(){
            run(false);
        });
    };

    var reset = function() {
        resetIframe(function(){
            run(true);
        });
    };

    return {
        run: run,
        revert: revert,
        reset: reset
    };
});
