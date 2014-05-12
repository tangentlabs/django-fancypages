var fancypages = fancypages || {};

fancypages.assets = {
    init: function () {
        var uploadProgress = $('#upload-progress');
        $('#fileupload').fileupload({
            dataType: 'json',
            done: function (e, data) {
                if (data.result.success) {
                    $("#fp-asset-gallery").append(data.result.images[0].thumbnailMarkup);
                    uploadProgress.addClass("hide");
                } else {
                    parent.fancypages.partials.messages.error(data.reason);
                }
            },
            progressall: function (e, data) {
                var progress = parseInt(data.loaded / data.total * 100, 10);

                uploadProgress.removeClass("hide");

                $('.bar', uploadProgress).css('width', progress + '%');
            },
            start: function () {
                $('.bar', uploadProgress).css('width', '0%');
            }
        });

        $(document).on('click', "[data-behaviours~=selectable-asset]", function (ev) {
            ev.preventDefault();
            parent.fancypages.editor.setSelectedAsset(
                $(this).data('asset-type'),
                $(this).data('asset-id'),
                //FIXME: this should probably be the actual image url
                $('img', this).attr('src')
            );
        });

    }
};
