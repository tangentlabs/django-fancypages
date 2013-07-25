var fancypages = fancypages || {};

fancypages.eventHandlers = {
    /**
     * Add a new tab to an existing tab block.
     */
    addNewTab: function (ev) {
        ev.preventDefault();

        $.ajax({
            url: $(this).data('action'),
            type: 'POST',
            data: {
                content_type: $(this).data('content-type-id'),
                object_id: $(this).parents('.block').data('block-id')
            },
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", fancypages.getCsrfToken());
            },
            success: function (data) {
                parent.fancypages.editor.reloadPage();
            },
            error: function () {
                parent.fancypages.utils.messages.error(
                    "An error occured trying to add a new tab. Please try it again."
                );
            }
        });
    },

    loadIframeModal: function (ev) {
        var iframeId = $(this).data('iframe-id');
        if (iframeId === undefined) {
            return;
        }

        $(this).parents('.asset-input').addClass('editing');
        var fullscreenModal = $("#fullscreen-modal");
        var iframeHtml = "<iframe id='" + iframeId + "' frameborder='0' width='100%' height='100%'></iframe>";
        $(".modal-body", fullscreenModal).html(iframeHtml);
        fullscreenModal.modal('show');

        var assetManager = $('#' + iframeId),
            modalHeight = fullscreenModal.height() - 100;
        assetManager.attr('src', $(this).data('iframe-src'));

        // Set height of the Asset IFrame
        assetManager.attr('height', modalHeight);
    },

    /**
     * Load and display the content of a modal.
     */
    loadModal: function (ev) {
        var elem = this;
        $.ajax({
            url: $(elem).data('href'),
            type: 'GET',
            data: {
                container: $(elem).data('container-id')
            },
            success: function (data) {
                var target = $($(elem).data('target'));
                target.parents('.modal').modal('show');
                target.html(data.rendered_form);

                // prevent collapse events within the modal from closing the modal
                target.find('#pages-sortable [id*="tree"]').on({
                    hide: function (event) {
                        event.stopPropagation();
                    }
                });
            },
            error: function () {
                fancypages.utils.messages.error("Unable to load list of available blocks.");
            }
        });
    },
    /**
     * Delete a block
     */
    deleteWidget: function (ev) {
        var block = $(this).parents('.block');
        var deleteUrl = '/dashboard/fancypages/block/delete/' + $(block).data('block-id') + "/";

        $.ajax(deleteUrl)
            .done(function (data) {
                var blockWrapper = $('div[id=block_input_wrapper]');
                blockWrapper.after(data);

                $(data).load(function () {
                    $(this).modal('show');
                });
            })
            .error(function () {
                fancypages.utils.messages.error(
                    "An error occured trying to delete a block. Please try it again."
                );
            });
    },
    /**
     * Load block form when edit button is clicked, add slider if a range
     * value is available for the block and scroll to the right position on
     * the page.
     */
    editWidget: function (ev) {
        var block = $(this).closest('.block');
        fancypages.editor.scrollToWidget(block);

        // Add Class to block editing
        $('.block').removeClass('editing');
        block.addClass('editing');

        fancypages.panels.showEditPanel();

        fancypages.editor.loadWidgetForm($(block).data('block-id'), $(block).data('container-name'), {
            success: function () {
                // attach slider to column width slider
                var sliderSelection = $('#id_left_width');
                sliderSelection.after('<div id="left-width-slider"></div>');
                sliderSelection.css('display', 'none');
                var slider = $('#left-width-slider');

                var maxValue = sliderSelection.data('max');
                var minValue = sliderSelection.data('min');

                slider.slider({
                    range: "min",
                    value: sliderSelection.val(),
                    min: minValue,
                    max: (maxValue - 1),
                    slide: function (ev, ui) {
                        var blockId = $(this).parents('form').data('block-id');
                        var previewField = $('#block-' + blockId);
                        var leftColumn = $('.column-left', previewField);

                        leftColumn[0].className = leftColumn[0].className.replace(/span\d+/g, '');
                        leftColumn.addClass('span' + ui.value);

                        var rightColumn = $('.column-right', previewField);
                        rightColumn[0].className = rightColumn[0].className.replace(/span\d+/g, '');
                        rightColumn.addClass('span' + (maxValue - ui.value));

                        sliderSelection.attr('value', ui.value);
                    }
                });
            }
        });
    },
    /**
     * Display form containing block settings in editor panel.
     */
    displayWidgetForm: function (options, data) {
        var blockWrapper = $('div[id=block_input_wrapper]');
        blockWrapper.html(data.rendered_form);
        $('#page-settings').hide();

        fancypages.editor.wysiwyg.init();

        //Init the Select2 plugin for selects in the editor
        $('#editor-panel select').css('width', '100%');
        $('#editor-panel select').select2();

        $('.editor').animate({backgroundColor: "#555"}, 500)
                    .delay(500)
                    .animate({backgroundColor: "#444"}, 500);

        fancypages.editor.updateSize();

        if (options && 'success' in options) {
            options.success();
        }
        return false;
    }
};
